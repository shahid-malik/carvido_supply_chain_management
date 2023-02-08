# -*- coding: utf-8 -*-

from odoo import _
from odoo import models, fields, api


class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    name = fields.Char(string="", readonly=False)

    @api.model
    def create(self, vals):
        sale_order_sequence = self.env['ir.sequence'].next_by_code('seq.sale.order') or _('New')
        sale_order_sequence = sale_order_sequence.replace("S", "A")
        if vals:
            vals['name'] = sale_order_sequence
            return super(SaleOrderInherit, self).create(vals)