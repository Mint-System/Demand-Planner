# -*- coding: utf-8 -*-
{
    'name': "Demand Planner",

    'summary': """
        Get order proposals for multi-level sub-products.
    """,

    'description': """
        Get order proposals for multi-level sub-products.
    """,

    'author': "Odoo PS",
    'website': "https://www.odoo.com",

    'category': 'Inventory',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['mrp', 'purchase_stock', 'sale_management'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/demand_planner_templates.xml',
        'views/demand_planner_views.xml',
        'views/res_config_settings_views.xml',
        'wizards/product_replenish_views.xml',
    ],
    'qweb': [
        "static/src/xml/listview_refresh.xml",
    ],
    'installable': True,
}
