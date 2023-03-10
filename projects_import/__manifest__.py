# -*- coding: utf-8 -*-
{
    'name': 'Carvido Data Import ',
    'version': '0.1',
    'development_status': 'Development',
    'category': '',
    'summary': """
    This module provide facility to import projects from bitrix24 directly into odoo.
    Step 1: Export bitrix data
    Step 2: Upload file and select odoo model in which data need to be imported.
    Step 3: Click Import 
    Step 3: Verify data
    """
    ,
    'license': 'Other proprietary',
    'author': 'Shahid Mehmood',
    'website': 'www.mediodconsulting.com',
    'images': [
        '',
    ],
    'application': True,
    'installable': True,
    'auto_install': False,
    'depends': [
        'base',
        'mail',
        'product',
        'website_sale',
        'sale',
        'stock',
        'sale_management',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/template_demo.xml',
        'data/vendor_Products_template_demo.xml',
        'data/north_America_advance_nutrients_product_details.xml',
        'data/send_mail_template.xml',
        'wizards/get_csv.xml',
        'views/vendor_template.xml',
        'views/product_template.xml',
        'views/product_template_inherit.xml',
        'views/quick_book_inherit.xml',
        'views/account_move_inherit.xml',
        'views/sale_order.xml',
        'views/website_templates.xml',
        'views/stock_picking.xml',
    ],
}
