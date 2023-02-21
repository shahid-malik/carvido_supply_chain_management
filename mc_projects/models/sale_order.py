# -*- coding: utf-8 -*-

from odoo import _
from odoo import models, fields, api
import datetime

MATERIAL_TYPE_SELECTION = [
    ('express', 'Express'),
    ('individual', 'Individual')
]


class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    name = fields.Char(string="", readonly=False)
    display_name = fields.Char(string="", readonly=False)
    send_quotation_date = fields.Date('Send Quotation Email Date')
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

    def _cron_sale_confirm_email_reminder(self):
        current_date = datetime.date.today().strftime('%Y-%m-%d')
        current_day_date = datetime.datetime.strptime(current_date, '%Y-%m-%d').date()
        draft_sale_orders = self.env['sale.order'].sudo().search([('state', '=', 'draft')])
        if draft_sale_orders:
            for rec in draft_sale_orders:
                shipping_date = rec.expected_shipping_date
                if shipping_date:
                    forteen_days_before_date = shipping_date - datetime.timedelta(days=14)
                    if forteen_days_before_date == current_day_date:
                        template_id = self.env.ref('mc_projects.sale_confirm_due_reminder_mail')
                        self.env['mail.template'].browse(template_id.id).with_context(email_to=rec.partner_id.email).send_mail(
                            rec.id, force_send=True)

        sent_sale_orders = self.env['sale.order'].sudo().search([('state', '=', 'sent')])
        if sent_sale_orders:
            for rec in sent_sale_orders:
                mail_delivery_date = rec.send_quotation_date
                if mail_delivery_date:
                    two_days_after_delivery_date = mail_delivery_date + datetime.timedelta(days=2)
                    if two_days_after_delivery_date == current_day_date:
                        sale_quot = rec.action_quotation_send()
                        sale_quot_id = sale_quot.get('context').get('default_res_id')
                        mail = self.env['mail.compose.message'].sudo().search([('res_id', '=', sale_quot_id)])[-1]
                        mail.action_send_mail()
                        mail_mail = self.env['mail.mail'].sudo().search([])[0]
                        mail_mail.send()

class SaleOrderLineInherit(models.Model):
    _inherit = 'sale.order.line'

    expected_delivery_date = fields.Date('Expected Delivery Date')
    material_type = fields.Selection(MATERIAL_TYPE_SELECTION, string='Material Type')
