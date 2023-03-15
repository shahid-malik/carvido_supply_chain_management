# -*- coding: utf-8 -*-
{
    'name': "Carvido Projects Import",

    'summary': """
        """,

    'description': """
        Carvido Supply Chain Management module provide facility to import projects from bitrix24 directly into odoo.
        Manage Projects, Deliveries & Barcode
    """,

    'author': "Mediod Consulting",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Inventory',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'stock', 'sale', 'kanban_stock', 'projects_import'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'data/sale_reminder_mail_template.xml',
        'data/sale_email_cron.xml',
        'views/sale_order.xml',
        'views/product_template.xml',
        'views/stock_picking.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
}
