# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    # Fields declarations
    is_calculate_theoretical_order = fields.Boolean(string='Calculate Theoretical Order',
                                                    config_parameter='demand_planner.is_calculate_theoretical_order')
    product_category_id = fields.Many2one('product.category', string='Product Category',
                                          config_parameter='demand_planner.product_category_id',
                                          help="Calculate demand only for products assigned to this category.")
    days_starting_planner = fields.Integer(config_parameter='demand_planner.days_starting_planner', default=0)
    days_ending_planner = fields.Integer(config_parameter='demand_planner.days_ending_planner', default=90)
