from odoo import models, fields,api


class ResPartner(models.Model):
    _inherit = "sale.order"

    expected_shipping_date = fields.Date('Expected Shipping Date')
    expected_delivery_date = fields.Date('Expected Delivery Date')
    batch_no = fields.Integer('Batch Number')
    express = fields.Boolean('Express(Urgent)')

    @api.onchange('expected_delivery_date')
    def onchange_expected_delivery_date(self):
        self.order_line.expected_delivery_date = self.expected_delivery_date

    @api.onchange('order_line')
    def onchange_order_line(self):
        if len(self.order_line) > 1:
            self.order_line[-1].price_unit = 0
            if self.expected_delivery_date:
                self.order_line[-1].expected_delivery_date = self.expected_delivery_date
        else:
            self.order_line.price_unit = 0
            if self.expected_delivery_date:
                self.order_line.expected_delivery_date = self.expected_delivery_date