from odoo import models, fields, api, _
from odoo.exceptions import AccessError, UserError, ValidationError


class StockPickingInherit(models.Model):
    _inherit = 'stock.picking'

    so_line_id = fields.Many2one(comodel_name='sale.order.line')

    def send_email_for_date(self):
        for rec in self:
            template_id = self.env.ref('projects_import.delivery_mail_template')
            self.env['mail.template'].browse(template_id.id).with_context(
                email_to=rec.partner_id.email).send_mail(rec.id, force_send=True)
