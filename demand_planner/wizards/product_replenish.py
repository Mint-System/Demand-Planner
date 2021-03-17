from odoo import _, api, fields, models


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

    def _prepare_run_values(self):
        values = super()._prepare_run_values()
        if self._context.get('active_model') == 'demand.planner' and self.seller_id:
            values['supplierinfo_name'] = self.seller_id
        return values
