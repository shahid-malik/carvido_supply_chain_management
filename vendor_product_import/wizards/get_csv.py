import os
import math
import base64
import datetime
import pandas as pd

from odoo.http import request
from odoo import fields, models

invoice_id = False
customer = False


def is_nan(val):
    try:
        math.isnan(val)
        return True
    except:
        return False


class WizardGetFile(models.TransientModel):
    _name = "mediod.csv.wizard"

    model_choices = [
        ('product', 'Products'),
        ('customer', 'Customer'),
        ('account', 'Chart of Accounts'),
        ('invoice', 'Invoice'),
        ('pricelist', 'Price List'),
        ('saleorder', 'Sale Order')]
    csv_file = fields.Binary('Upload CSV', required=True)
    model_name = fields.Selection(model_choices, 'Model Name')

    def import_csv(self):
        file = base64.b64decode(self.csv_file)
        file_string = file.decode('unicode_escape')
        cur_dir = os.path.dirname(os.path.abspath(__file__))
        file_name = os.path.join(cur_dir, "demofile2.csv")

        with open(file_name, "w", encoding="utf-8") as f:
            f.write(file_string)

        df = pd.read_csv(file_name, error_bad_lines=False)
        for date, row in df.T.items():
            self.import_quickbooks_saleorder_data(row)

    def import_quickbooks_saleorder_data(self, row):
        customer_name = str(row["Bitrix24 KundenID"])
        order_no = str(row["Auftragsnummer"]) if is_nan(row["Auftragsnummer"]) is False else None
        expected_shipping_date = datetime.datetime.strptime(str(row["Auslieferungsdatum"]), "%m/%d/%Y").strftime(
            "%Y-%m-%d") if is_nan(row["Auslieferungsdatum"]) is False else None
        batch_no = float(row["Chargennummer"])
        if math.isnan(row['Chargennummer']):
            batch_no = 0
        expected_delivery_date = datetime.datetime.strptime(str(row["Anlieferungsdatum"]), "%m/%d/%Y").strftime(
            "%Y-%m-%d") if is_nan(row["Anlieferungsdatum"]) is False else None

        partner = self.env['res.partner'].sudo().search([('name', '=', customer_name)])
        if not partner:
            partner = self.env['res.partner'].sudo().create({'name': customer_name})

        sale_id = request.env['sale.order'].search([('name', '=', 'A1532')], limit=1,
                                                   order='id desc')
        if not sale_id:
            sale_order_list = {
                "partner_id": partner.id,
                "name": order_no,
                "expected_shipping_date": expected_shipping_date,
                "batch_no": batch_no,
                "expected_delivery_date": expected_delivery_date,
                "validity_date": expected_delivery_date,
                "date_order": expected_delivery_date,
            }
            sale_id = self.env['sale.order'].create(sale_order_list)
        quantity = float(row["Quantity"])
        if math.isnan(row['Quantity']):
            quantity = 0
        express = str(row["Express"]) if is_nan(row["Express"]) is False else None
        if express == 'X':
            express = None
        product_name = str(row["Produkt ID"]) if is_nan(row["Produkt ID"]) is False else None
        product_tmpl_id = request.env['product.product'].search([('name', '=', product_name)])
        unit_price = float(row["Unit Price"])
        if product_tmpl_id:
            if math.isnan(row['Unit Price']):
                unit_price = product_tmpl_id.base_unit_price
            self.env['sale.order.line'].create({'product_id': product_tmpl_id.id,
                                                'name': product_name,
                                                'product_uom_qty': quantity,
                                                'price_unit': unit_price,
                                                'express': express,
                                                'order_id': sale_id.id,
                                                })
        else:
            product_tmpl_id = self.env['product.product'].create({'name': product_name})
            if math.isnan(row['Unit Price']):
                unit_price = product_tmpl_id.base_unit_price
            self.env['sale.order.line'].create({'product_id': product_tmpl_id.id,
                                                'name': product_name,
                                                'product_uom_qty': quantity,
                                                'price_unit': unit_price,
                                                'express': express,
                                                'order_id': sale_id.id,
                                                })
