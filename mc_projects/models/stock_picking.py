# -*- coding: utf-8 -*-

from odoo import models, fields, api

MATERIAL_TYPE_SELECTION = [
    ('express', 'Express'),
    ('individual', 'Individual')
]


class SaleOrderLineInherit(models.Model):
    _inherit = 'stock.move'

    expected_delivery_date = fields.Date('Expected Delivery Date')
    material_type = fields.Selection(MATERIAL_TYPE_SELECTION, string='Material Type')


class SaleOrderInherit(models.Model):
    _inherit = 'stock.picking'

    expected_delivery_date = fields.Date('Expected Delivery Date')
    material_type = fields.Selection(MATERIAL_TYPE_SELECTION, string='Material Type')

