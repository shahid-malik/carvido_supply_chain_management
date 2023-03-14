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
        customer_name = str(row["customer_id"])
        order_no = str(row["order_number"]) if is_nan(row["order_number"]) is False else None
        expected_shipping_date = datetime.datetime.strptime(str(row["expected_shipping_date_out"]), "%d/%m/%Y").strftime(
            "%Y-%m-%d") if is_nan(row["expected_shipping_date_out"]) is False else None
        batch_no = float(row["batch_number"])
        if math.isnan(row['batch_number']):
            batch_no = 0
        expected_delivery_date = datetime.datetime.strptime(str(row["expected_delivery_date_in"]), "%d/%m/%Y").strftime(
            "%Y-%m-%d") if is_nan(row["expected_delivery_date_in"]) is False else None

        partner = self.env['res.partner'].sudo().search([('name', '=', customer_name)])
        if not partner:
            partner = self.env['res.partner'].sudo().create({'name': customer_name})

        sale_id = request.env['sale.order'].search([('name', '=', order_no)], limit=1, order='id desc')
        if not sale_id:
            sale_order_dict = {
                "partner_id": partner.id,
                "name": order_no,
                "expected_shipping_date": expected_shipping_date,
                "batch_no": batch_no,
                "expected_delivery_date": expected_delivery_date,
                "validity_date": expected_delivery_date,
                "date_order": expected_delivery_date,
            }
            sale_id = self.env['sale.order'].create(sale_order_dict)
            sale_id.update({'name': order_no})

        quantity = float(row["quantity"])
        if math.isnan(row['quantity']):
            quantity = 0
        material_type = str(row["express"]) if is_nan(row["express"]) is False else None
        # TODO note for waqas
        # Instead fo having express field, Material type field will be used to store express or individual,
        # I change the code, validate your
        if material_type == 'X':
            material_type = "individual"
        else:
            material_type = "express"
        product_name = str(row["product_id"]) if is_nan(row["product_id"]) is False else None
        product_tmpl_id = request.env['product.product'].search([('name', '=', product_name)])
        unit_price = 0.0
        if product_tmpl_id:
            try:
                if math.isnan(row['unit_price']):
                    unit_price = product_tmpl_id.base_unit_price
            except:
                pass

            sale_line = self.env['sale.order.line'].create({'product_id': product_tmpl_id.id,
                                                            'name': product_name,
                                                            'product_uom_qty': quantity,
                                                            'price_unit': unit_price,
                                                            'expected_delivery_date': expected_delivery_date,
                                                            'material_type': material_type,
                                                            'order_id': sale_id.id,
                                                            })
            picking_type_id = self.env.ref('stock.picking_type_out')
            dest_location_id = self.env.ref('stock.stock_location_suppliers')
            location_id = self.env.ref('stock.stock_location_stock')

            values = {
                'partner_id': sale_id.partner_id.id,
                'sale_id': sale_id.id,
                'origin': sale_id.name,
                'picking_type_id': picking_type_id.id,
                'scheduled_date': sale_id.date_order,
                'expected_delivery_date': expected_delivery_date,
                'location_dest_id': dest_location_id.id,
                'location_id': location_id.id,
                'move_ids_without_package': [((0, 0, {
                    'product_id': sale_line.product_id.id,
                    'name': '',
                    'quantity_done': 1,
                    'product_uom_qty': sale_line.product_uom_qty,
                    'expected_delivery_date': expected_delivery_date,
                    'material_type': sale_line.material_type,
                    'location_dest_id': dest_location_id.id,
                    'location_id': location_id.id,
                }))]
            }

            stock_pick_create = self.env['stock.picking'].create(values)
            stock_pick_create.write({'state': 'draft'})
        else:
            product_tmpl_id = self.env['product.product'].create({'name': product_name, 'base_unit_price': 0.0 })
            unit_price = 0.0
            try:
                if math.isnan(row['unit_price']):
                    unit_price = product_tmpl_id.base_unit_price
            except:
                pass
            sale_line = self.env['sale.order.line'].create({'product_id': product_tmpl_id.id,
                                                            'name': product_name,
                                                            'product_uom_qty': quantity,
                                                            'price_unit': unit_price,
                                                            'expected_delivery_date': expected_delivery_date,
                                                            'material_type': material_type,
                                                            'order_id': sale_id.id,
                                                            })
            picking_type_id = self.env.ref('stock.picking_type_out')
            dest_location_id = self.env.ref('stock.stock_location_suppliers')
            location_id = self.env.ref('stock.stock_location_stock')

            values = {
                'partner_id': sale_id.partner_id.id,
                'sale_id': sale_id.id,
                'origin': sale_id.name,
                'picking_type_id': picking_type_id.id,
                'scheduled_date': sale_id.date_order,
                'expected_delivery_date': expected_delivery_date,
                'location_dest_id': dest_location_id.id,
                'location_id': location_id.id,
                'move_ids_without_package': [((0, 0, {
                    'product_id': sale_line.product_id.id,
                    'name': '',
                    'quantity_done': 1,
                    'product_uom_qty': sale_line.product_uom_qty,
                    'expected_delivery_date': expected_delivery_date,
                    'material_type': sale_line.material_type,
                    'location_dest_id': dest_location_id.id,
                    'location_id': location_id.id,
                }))]
            }

            stock_pick_create = self.env['stock.picking'].create(values)
            stock_pick_create.write({'state': 'draft'})
