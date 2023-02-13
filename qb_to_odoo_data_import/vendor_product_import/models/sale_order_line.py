from odoo import models, fields


class ResPartner(models.Model):
    _inherit = "sale.order.line"

    express = fields.Boolean('Express')
    expected_delivery_date = fields.Date('Expected Delivery Date')