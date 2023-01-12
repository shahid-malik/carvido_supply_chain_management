# -*- coding: utf-8 -*-
from odoo import models, fields, api

class productTemplate(models.Model):
    _inherit = 'product.template'

    part_number = fields.Char(string="Part No/Name")
    rfid_code = fields.Integer('RFID Code')
    length = fields.Float('Length')
    width = fields.Float('Width')
    thickness = fields.Float('Thickness')
    weight = fields.Float('Weight')
    area = fields.Float('Area')
    remarks = fields.Text('Remarks')
    basic_material = fields.Char('Basic material')
    surface_bottom = fields.Char('Surface bottom')
    surface_top = fields.Char('Surface top')
    designation = fields.Char('Designation')
    supplier = fields.Many2one('res.partner','Supplier')
    abs_edge = fields.Char('ABS edge')
