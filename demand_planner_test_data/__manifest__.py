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
    'version': '14.0.1.0.1',

    # any module necessary for this one to work correctly
    'depends': ['demand_planner'],

    'data': [
        'data/mountain_bike/res.partner.csv',
        'data/mountain_bike/product.product.csv',
        'data/mountain_bike/product.supplierinfo.csv',
        'data/mountain_bike/mrp.bom.csv',
        'data/mountain_bike/mrp.bom.line.csv',
        'data/meldeeinheit_pma14/res.partner.csv',
        'data/meldeeinheit_pma14/product.product.csv',
        'data/meldeeinheit_pma14/product.supplierinfo.csv',
        'data/meldeeinheit_pma14/mrp.bom.csv',
        'data/meldeeinheit_pma14/mrp.bom.line.csv'
    ],
}
