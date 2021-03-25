# -*- coding: utf-8 -*-
{
    'name': "Demand Planner Testdata",

    'summary': """
        Load test data sets for Demand Planner.
    """,

    'description': """
        Load test data sets for Demand Planner.
    """,

    'author': "Odoo PS",
    'website': "https://www.odoo.com",

    'category': 'Inventory',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['demand_planner'],

    # Load csv data once module is installed
    'post_init_hook': 'post_init',
}
