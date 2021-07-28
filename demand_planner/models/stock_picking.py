# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models

class PickingType(models.Model):
    _inherit = 'stock.picking.type'

    is_demand_planner = fields.Boolean('Calculate demand for manufacturing orders')