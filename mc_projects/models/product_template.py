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
    supplier = fields.Many2one('res.partner', 'Supplier')
    abs_edge = fields.Char('ABS edge')

    coating_below = fields.Char('Coating Below')
    coating_top = fields.Char('Coating Top')
    varnish_below = fields.Char('Varnish Below')
    varnish_top = fields.Char('Varnish Top')
    angle = fields.Char('Mitre/Angle')
    contour_milling = fields.Char('Contour milling')
    constructors = fields.Char('Constructor')

    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        stage_ids = self.env['stage.stage'].search([])
        return stage_ids

    picking_type = fields.Many2one('stock.picking', group_expand='_read_group_stage_ids')
