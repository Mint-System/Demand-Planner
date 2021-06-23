from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools.misc import clean_context

class ProductReplenish(models.TransientModel):
    _inherit = 'product.replenish'

    seller_id = fields.Many2one('res.partner', string="Vendor")

    @api.onchange('product_tmpl_id')
    def _onchange_vendors(self):
        seller_ids = self.mapped('product_tmpl_id.seller_ids.name.id')
        return {
            'domain': {
                'seller_id': [
                    ('id', 'in', seller_ids)
                ]}
        }

    # To change the name and origin as Demand Planner from Manual Replenishment
    def launch_replenishment(self):
        if self._context.get('active_model') == 'demand.planner':
            uom_reference = self.product_id.uom_id
            self.quantity = self.product_uom_id._compute_quantity(self.quantity, uom_reference)
            try:
                self.env['procurement.group'].with_context(clean_context(self.env.context)).run([
                    self.env['procurement.group'].Procurement(
                        self.product_id,
                        self.quantity,
                        uom_reference,
                        self.warehouse_id.lot_stock_id,  # Location
                        _("Demand Planner"),  # Name --> Modified
                        _("Demand Planner"),  # Origin --> Modified
                        self.warehouse_id.company_id,
                        self._prepare_run_values()  # Values
                    )
                ])
            except UserError as error:
                raise UserError(error)
        else:
            super().launch_replenishment()

    def _prepare_run_values(self):
        values = super()._prepare_run_values()
        if self._context.get('active_model') == 'demand.planner' and self.seller_id:
            values['supplierinfo_name'] = self.seller_id
        return values
