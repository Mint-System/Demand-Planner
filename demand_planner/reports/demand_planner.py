# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import timedelta
from odoo import fields, models


class DemandPlanner(models.Model):
    _name = 'demand.planner'
    _description = 'Demand Planner'

    product_id = fields.Many2one('product.product', 'Product')
    proposed_order_date = fields.Date("Proposed Order Date")
    delivery_order = fields.Many2one('stock.picking')
    delivery_order_date = fields.Date('Delivery Date')
    qty = fields.Float("Quantity")

    def action_replenish(self):
        return {
            'name': "Product Replanish",
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'product.replenish',
            'view_id': self.env.ref('demand_planner.view_product_replenish_inherit_demand_planner').id,
            'target': 'new',
            'context': {'default_product_id': self.product_id.id, 'default_quantity': self.qty, 'default_route_ids': self.product_id.route_ids.ids},
        }

    def _get_bom(self, bom=False, product_id=False, line_qty=False, line_id=False, level=False):
        bom_quantity = line_qty
        if line_id:
            current_line = self.env['mrp.bom.line'].browse(int(line_id))
            bom_quantity = current_line.product_uom_id._compute_quantity(line_qty, bom.product_uom_id)
        # Display bom components for current selected product variant
        if product_id:
            product = self.env['product.product'].browse(int(product_id))
        else:
            product = bom.product_id or bom.product_tmpl_id.product_variant_id
        lines = {
            'product_id': product.id,
            'bom': bom.id,
            'bom_qty': bom_quantity,
            'bom_prod_name': product.display_name,
            'delay': product.produce_delay,
            'level': level or 0,
            'qty_available': product.qty_available
        }
        lines['components'] = self._get_bom_lines(bom, bom_quantity, product, line_id, level)
        return lines

    def _get_bom_lines(self, bom, bom_quantity, product, line_id, level):
        components = []
        for line in bom.bom_line_ids:
            line_quantity = (bom_quantity / (bom.product_qty or 1.0)) * line.product_qty
            if line._skip_bom_line(product):
                continue
            delay = 0
            if line.child_bom_id.id:
                delay = line.product_id.produce_delay
            else:
                delay = line.product_id.seller_ids[0].delay if line.product_id.seller_ids else 0
            components.append({
                'prod_id': line.product_id.id,
                'prod_name': line.product_id.display_name,
                'prod_qty': line_quantity,
                'delay': delay,
                'parent_id': product.id,
                'line_id': line.id,
                'level': level or 0,
                'child_bom': line.child_bom_id.id,
                'phantom_bom': line.child_bom_id and line.child_bom_id.type == 'phantom' or False,
                'qty_available': line.product_id.qty_available
            })
        return components

    def _get_pdf_line(self, bom_id, product_id=False, qty=1, child_bom_ids=[], unfolded=False):

        def get_sub_lines(bom, product_id, line_qty, line_id, level):
            data = self._get_bom(bom=bom, product_id=product_id.id, line_qty=line_qty, line_id=line_id, level=level)
            bom_lines = data['components']
            lines = {}
            for bom_line in bom_lines:
                line_product_id = bom_line['prod_id']
                # TOCHECK: what happends if the same product is used inside sub BoMs ?
                if not lines.get(line_product_id):
                    lines[line_product_id] = {
                        'name': bom_line['prod_name'],
                        'type': 'bom',
                        'parent_id': bom_line['parent_id'],
                        'quantity': bom_line['prod_qty'],
                        'level': bom_line['level'],
                        'child_bom': bom_line['child_bom'],
                        'prod_id': bom_line['prod_id'],
                        'delay': bom_line['delay'],
                        'qty_available': bom_line['qty_available'],
                        'parent_qty': data['bom_qty'],
                    }
                if bom_line['child_bom'] and (unfolded or bom_line['child_bom'] in child_bom_ids):
                    line = self.env['mrp.bom.line'].browse(bom_line['line_id'])
                    lines.update(get_sub_lines(line.child_bom_id, line.product_id, bom_line['prod_qty'], line, level + 1))
            return lines

        bom = self.env['mrp.bom'].browse(bom_id)
        product = bom.product_tmpl_id.product_variant_id
        data = self._get_bom(bom=bom, product_id=product.id, line_qty=qty)
        pdf_lines = get_sub_lines(bom, product, qty, False, 1)
        data['lines'] = pdf_lines
        del data['components']
        return data

    def _get_pickings(self):
        # Add order by on deliveries date
        ICP = self.env['ir.config_parameter'].sudo()
        res_max_days = int(ICP.get_param('demand_planner.days_ending_planner', 0))
        res_min_days = int(ICP.get_param('demand_planner.days_starting_planner', 0))
        date_today = fields.Date.today()
        max_date = date_today + timedelta(days=res_max_days)
        min_date = date_today + timedelta(days=res_min_days)
        return self.env['stock.picking'].search([
            ('state', 'not in', ('cancel', 'draft', 'done')),
            ('picking_type_id.code', '=', 'outgoing'),
            ('sale_id', '!=', False),
            ('scheduled_date', '<=', max_date),
            ('scheduled_date', '>=', min_date),
            ('company_id', '=', self.env.company.id),
        ])

    def _prepare_bom_structure_with_delivery_process(self):
        deliveries = self._get_pickings()
        delivery_process = []
        products = {}  # To store the products BOM structure [ Bike, Table ]
        for delivery in deliveries:
            sale = delivery.sale_id
            delivery_date = sale.commitment_date or delivery.scheduled_date
            # Process the products in deliveries
            for saleline in delivery.sale_id.order_line:
                main_product = saleline.product_id
                # Check for bom, if multiple found take the latest created bom
                bom = main_product.bom_ids and main_product.bom_ids[-1]
                if bom:
                    delivery_process.append({
                        'delivery_id': delivery.id,
                        'delivery_date': delivery_date,
                        'sale_qty': saleline.product_uom_qty,
                        'product': main_product.id,
                    })
                # Process only if the product is not found in products dict
                if main_product.id not in products:
                    # Ignore products without BoM as such data will have pickings and reflects on the stock
                    if bom:
                        bom_lines = self._get_pdf_line(bom.id, False, 1, [], True)
                        # Store the bom_lines in products dict
                        products[main_product.id] = bom_lines
        return products, delivery_process

    def _get_forecasted_stock(self, product_id, date, line_data):
        # Find the product and date in forecast
        forecast_report = self.env['report.stock.quantity'].read_group(
                [('date', '=', date),
                 ('product_id', '=', product_id),
                 ('state', '=', 'forecast'),
                 ('company_id', '=', self.env.company.id)],
                ['product_qty', 'date', 'product_id', 'state'],
                ['date:day', 'product_id', 'state'],
                lazy=False)
        # Return forecasted quantity or None [ None -> Use Stock Quantity or 0]
        forecasted_qty = forecast_report[0]['product_qty'] if forecast_report else 0
        return {'forecasted_qty': forecasted_qty, 'qty_available': line_data['qty_available']}

    def get_data(self):
        # Remove all data from demand planner
        self.env.cr.execute('''
            DELETE FROM demand_planner
        ''')
        products, delivery_process = self._prepare_bom_structure_with_delivery_process()
        demanded_stock = {}
        demand_planner_data = []
        for delivery in delivery_process:
            prodid = delivery['product']
            data = products[prodid]
            sale_qty = delivery['sale_qty']
            demand_planner_data.append({
                'proposed_order_date': delivery['delivery_date'] - timedelta(data['delay']),
                'product_id': prodid,
                'delivery_order': delivery['delivery_id'],
                'delivery_order_date': delivery['delivery_date'],
                'qty': sale_qty,
            })
            main_bom_delay = data['delay']
            bom_lines_dict = data['lines']
            for bom_product_id, values in bom_lines_dict.items():
                line_level = values.get('level')
                line_delay = main_bom_delay + values['delay']
                parent_id = values.get('parent_id')
                # iterated through all the parents(except main) of line and find the total delay to produce the product
                while line_level != 1:
                    parent_line = bom_lines_dict.get(parent_id, {})
                    parent_delay = parent_line.get('delay', 0)
                    line_delay += parent_delay
                    parent_id = parent_line.get('parent_id')
                    line_level -= 1
                line_proposed_date = delivery['delivery_date'] - timedelta(line_delay)
                required_qty = sale_qty * values['quantity']
                stock_on_hand_data = self._get_forecasted_stock(values['prod_id'], line_proposed_date, values)
                forecasted_qty = stock_on_hand_data['forecasted_qty'] or stock_on_hand_data['qty_available']
                if forecasted_qty <= 0:
                    forecasted_qty = 0
                else:
                    forecasted_qty -= demanded_stock.get(bom_product_id, 0)

                # Check with what is on hand
                to_order_qty = 0
                if required_qty > forecasted_qty:
                    to_order_qty = required_qty - forecasted_qty
                    demand_planner_data.append({
                        'proposed_order_date': line_proposed_date,
                        'product_id': values['prod_id'],
                        'delivery_order': delivery['delivery_id'],
                        'delivery_order_date': delivery['delivery_date'],
                        'qty': to_order_qty,
                    })
                # we prepare local dict per product to have current stock of ordered quantity
                remaining_qty = required_qty - to_order_qty
                if bom_product_id in demanded_stock:
                    demanded_stock[bom_product_id] += remaining_qty - forecasted_qty
                else:
                    demanded_stock[bom_product_id] = remaining_qty

        # Create Entry in demand planner
        return self.create(demand_planner_data)
