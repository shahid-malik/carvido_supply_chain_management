from odoo import models, fields,api,_
from odoo.exceptions import AccessError, UserError, ValidationError


class ResPartner(models.Model):
    _inherit = "sale.order"

    expected_shipping_date = fields.Date('Expected Shipping Date')
    expected_delivery_date = fields.Date('Expected Delivery Date')
    batch_no = fields.Integer('Batch Number')
    express = fields.Boolean('Express(Urgent)')
    hide_delivery_btn = fields.Boolean('Delivery Button')


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

    def generate_deliveries(self):
         for rec in self:
            for sale_line in rec.order_line:
                pre_sale_id = self.env['stock.picking'].search([('sale_id', '=', self.id), ('so_line_id', '=',sale_line.id)])
                if not pre_sale_id:
                    picking_type_id = self.env.ref('stock.picking_type_out')
                    dest_location_id = self.env.ref('stock.stock_location_suppliers')
                    location_id = self.env.ref('stock.stock_location_stock')

                    values = {
                        'partner_id': self.partner_id.id,
                        'sale_id': self.id,
                        'so_line_id': sale_line.id,
                        'origin': self.name,
                        'picking_type_id': picking_type_id.id,
                        'scheduled_date': self.date_order,
                        # 'expected_delivery_date': expected_delivery_date,
                        'location_dest_id': dest_location_id.id,
                        'location_id': location_id.id,
                        'move_ids_without_package': [((0, 0, {
                            'product_id': sale_line.product_id.id,
                            'name': '',
                            'quantity_done': 1,
                            'product_uom_qty': sale_line.product_uom_qty,
                            # 'expected_delivery_date': expected_delivery_date,
                            'material_type': sale_line.material_type,
                            'location_dest_id': dest_location_id.id,
                            'location_id': location_id.id,
                        }))]
                    }

                    stock_pick_create = self.env['stock.picking'].create(values)
                    stock_pick_create.write({'state': 'draft'})


            return True


    class StockPickingInherit(models.Model):
        _inherit = 'stock.picking'

        so_line_id = fields.Many2one(comodel_name='sale.order.line')


    
