from odoo import models, fields


class ResPartner(models.Model):
    _inherit = "sale.order"

    expected_shipping_date = fields.Date('Expected Shipping Date')
    expected_delivery_date = fields.Date('Expected Delivery Date')
    batch_no = fields.Integer('Batch Number')