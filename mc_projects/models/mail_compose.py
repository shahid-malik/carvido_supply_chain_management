# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
import datetime


class MailComposeMessage(models.TransientModel):
    _inherit = 'mail.compose.message'

    def action_send_mail(self):
        res = super().action_send_mail()
        if self.model == 'sale.order':
            sale_order = self.env['sale.order'].search([('name', '=', self.record_name)], limit=1)
            if sale_order.state == 'sent':
                current_date = datetime.date.today().strftime('%Y-%m-%d')
                current_day_date = datetime.datetime.strptime(current_date, '%Y-%m-%d').date()
                sale_order.send_quotation_date = current_day_date
        return res
