# -*- coding: utf-8 -*-

from odoo import _
from odoo import models, fields, api


MATERIAL_TYPE_SELECTION = [
    ('express', 'Express'),
    ('individual', 'Individual')
]


class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    name = fields.Char(string="", readonly=False)
    display_name = fields.Char(string="", readonly=False)
    material_type = fields.Selection(MATERIAL_TYPE_SELECTION, string='Material Type')

    @api.model
    def create(self, vals):
        sale_order_sequence = self.env['ir.sequence'].next_by_code('seq.sale.order') or _('New')
        sale_order_sequence = sale_order_sequence.replace("S", "A")
        if vals:
            vals['name'] = sale_order_sequence

        # for line in self:
        #     line.expected_delivery_date = self.expected_delivery_date
        #

        return super(SaleOrderInherit, self).create(vals)

    # @api.onchange('expected_delivery_date')
    # def _onchange_expected_delivery_date(self):
    #     for line in self:
    #         line.expected_delivery_date = self.expected_delivery_date
    #     return


class SaleOrderLineInherit(models.Model):
    _inherit = 'sale.order.line'

    expected_delivery_date = fields.Date('Expected Delivery Date')
    material_type = fields.Selection(MATERIAL_TYPE_SELECTION, string='Material Type')
