# -*- coding: utf-8 -*-
{
    'name': "mc_projects",

    'summary': """
        """,

    'description': """
        Carvido Supply Chain Management
    """,

    'author': "Mediod Consulting",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Inventory',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'stock', 'sale', 'kanban_stock', 'vendor_product_import'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/sale_order.xml',
        'views/product_template.xml',
        'views/stock_picking.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
}
