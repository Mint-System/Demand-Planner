# -*- coding: utf-8 -*-
{
    'name': "Demand Planner",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Mint System GmbH",
    'website': "https://www.mint-system.ch",

    'category': 'Manufacturing',
    'version': '14.0.0.0.0',

    # any module necessary for this one to work correctly
    'depends': ['mrp', 'purchase', 'contacts'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
