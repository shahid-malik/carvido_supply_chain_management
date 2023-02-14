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
        sale_orders = self.env['sale.order'].sudo().search([('state', '=', 'draft')])
        for rec in sale_orders:
            current_date = datetime.date.today().strftime('%Y-%m-%d')
            current_day_date = datetime.datetime.strptime(current_date, '%Y-%m-%d').date()
            shipping_date = rec.expected_shipping_date
            two_days_before_date = shipping_date - datetime.timedelta(days=14)
            if two_days_before_date == current_day_date:
                template_id = self.env.ref('mc_projects.sale_confirm_due_reminder_mail')
                self.env['mail.template'].browse(template_id.id).with_context(email_to=rec.partner_id.email).send_mail(
                    rec.id, force_send=True)


class SaleOrderLineInherit(models.Model):
    _inherit = 'sale.order.line'

    expected_delivery_date = fields.Date('Expected Delivery Date')
    material_type = fields.Selection(MATERIAL_TYPE_SELECTION, string='Material Type')
