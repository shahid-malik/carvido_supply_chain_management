from odoo import models, fields


class ResPartner(models.Model):
    _inherit = "sale.order.line"

    express = fields.Char('Express')