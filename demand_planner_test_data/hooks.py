from odoo.tools import convert_file

def import_csv_data(cr, registry):
    """Import CSV data as it is faster than xml and because we can't use
    noupdate anymore with csv"""
    filenames = [
        'data/mountain_bike/convert/res.partner.csv',
        'data/mountain_bike/convert/product.product.csv',
        'data/mountain_bike/convert/product.supplierinfo.csv',
        # 'data/mountain_bike/convert/mrp.bom.csv',
        # 'data/mountain_bike/convert/mrp.bom.line.csv'
    ]
    for filename in filenames:
        convert_file(
            cr, 'demand_planner_test_data', filename,
            None, mode='init', kind='data'
        )

def post_init(cr, registry):
    import_csv_data(cr, registry)