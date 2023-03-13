from odoo import models, fields, api, _
from odoo.exceptions import AccessError, UserError, ValidationError


class SaleOrderInherited(models.Model):
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
                pre_sale_id = self.env['stock.picking'].search(
                    [('sale_id', '=', self.id), ('so_line_id', '=', sale_line.id)])
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


class SaleOrderLineInherit(models.Model):
    _inherit = 'sale.order.line'

    def _action_launch_stock_rule(self, previous_product_uom_qty=False):
        # res = super(SaleOrderLineInherit, self)._action_launch_stock_rule()
        standard_product_ids = []
        individual_product_ids = []
        for rec in self:
            if rec.product_id.supplier.id is False:
                raise ValidationError("Product has no Supplier which is mandatory!")
            if 'A1532' in rec.product_id.name:
                standard_product_ids.append(rec.product_id.id)
            else:
                individual_product_ids.append(rec.product_id.id)
            pre_stock_id = self.env['stock.picking'].search([('sale_id', '=', self.order_id.id)])
            if rec.product_id.id in individual_product_ids:
                if pre_stock_id:
                    for stock in pre_stock_id:
                        if stock.partner_id.id == rec.product_id.supplier.id and stock.product_id.id in individual_product_ids:
                            values = {
                                'product_id': rec.product_id.id,
                                'name': '',
                                'origin': rec.order_id.name,
                                'quantity_done': 1,
                                'picking_id': stock.id,
                                'product_uom_qty': rec.product_uom_qty,
                                # 'expected_delivery_date': expected_delivery_date,
                                'material_type': rec.material_type,
                                'location_dest_id': dest_location_id.id,
                                'location_id': location_id.id
                            }
                            stock_move_create = self.env['stock.move'].create(values)
                            stock.update({
                                'sale_id': rec.order_id.id,
                            })
                        else:
                            picking_type_id = self.env.ref('stock.picking_type_out')
                            dest_location_id = self.env.ref('stock.stock_location_suppliers')
                            location_id = self.env.ref('stock.stock_location_stock')

                            values = {
                                'partner_id': rec.product_id.supplier.id,
                                'sale_id': rec.order_id.id,
                                # 'so_line_id': sale_line.id,
                                'origin': rec.order_id.name,
                                'picking_type_id': picking_type_id.id,
                                'scheduled_date': rec.order_id.date_order,
                                # 'expected_delivery_date': expected_delivery_date,
                                'location_dest_id': dest_location_id.id,
                                'location_id': location_id.id,
                                'move_ids_without_package': [((0, 0, {
                                    'product_id': rec.product_id.id,
                                    'name': '',
                                    'origin': rec.order_id.name,
                                    'quantity_done': 1,
                                    'product_uom_qty': rec.product_uom_qty,
                                    # 'expected_delivery_date': expected_delivery_date,
                                    'material_type': rec.material_type,
                                    'location_dest_id': dest_location_id.id,
                                    'location_id': location_id.id,
                                }))]
                            }
                            if values['partner_id']:
                                stock_pick_create = self.env['stock.picking'].create(values)
                else:
                    picking_type_id = self.env.ref('stock.picking_type_out')
                    dest_location_id = self.env.ref('stock.stock_location_suppliers')
                    location_id = self.env.ref('stock.stock_location_stock')

                    values = {
                        'partner_id': rec.product_id.supplier.id,
                        'sale_id': rec.order_id.id,
                        # 'so_line_id': sale_line.id,
                        'origin': rec.order_id.name,
                        'picking_type_id': picking_type_id.id,
                        'scheduled_date': rec.order_id.date_order,
                        # 'expected_delivery_date': expected_delivery_date,
                        'location_dest_id': dest_location_id.id,
                        'location_id': location_id.id,
                        'move_ids_without_package': [((0, 0, {
                            'product_id': rec.product_id.id,
                            'name': '',
                            'origin': rec.order_id.name,
                            'quantity_done': 1,
                            'product_uom_qty': rec.product_uom_qty,
                            # 'expected_delivery_date': expected_delivery_date,
                            'material_type': rec.material_type,
                            'location_dest_id': dest_location_id.id,
                            'location_id': location_id.id,
                        }))]
                    }
                    if values['partner_id']:
                        stock_pick_create = self.env['stock.picking'].create(values)
            else:
                if pre_stock_id:
                    for stock in pre_stock_id:
                        if stock.product_id.id in standard_product_ids:
                            values = {
                                'product_id': rec.product_id.id,
                                'name': '',
                                'origin': rec.order_id.name,
                                'quantity_done': 1,
                                'picking_id': stock.id,
                                'product_uom_qty': rec.product_uom_qty,
                                # 'expected_delivery_date': expected_delivery_date,
                                'material_type': rec.material_type,
                                'location_dest_id': dest_location_id.id,
                                'location_id': location_id.id
                            }
                            stock_move_create = self.env['stock.move'].create(values)
                            stock.update({
                                'sale_id': rec.order_id.id,
                            })
                        elif rec.product_id.id not in standard_product_ids:
                            picking_type_id = self.env.ref('stock.picking_type_out')
                            dest_location_id = self.env.ref('stock.stock_location_suppliers')
                            location_id = self.env.ref('stock.stock_location_stock')

                            values = {
                                'partner_id': rec.order_id.partner_id.id,
                                'sale_id': rec.order_id.id,
                                # 'so_line_id': sale_line.id,
                                'origin': rec.order_id.name,
                                'picking_type_id': picking_type_id.id,
                                'scheduled_date': rec.order_id.date_order,
                                # 'expected_delivery_date': expected_delivery_date,
                                'location_dest_id': dest_location_id.id,
                                'location_id': location_id.id,
                                'move_ids_without_package': [((0, 0, {
                                    'product_id': rec.product_id.id,
                                    'name': '',
                                    'origin': rec.order_id.name,
                                    'quantity_done': 1,
                                    'product_uom_qty': rec.product_uom_qty,
                                    # 'expected_delivery_date': expected_delivery_date,
                                    'material_type': rec.material_type,
                                    'location_dest_id': dest_location_id.id,
                                    'location_id': location_id.id,
                                }))]
                            }
                            if values['partner_id']:
                                stock_pick_create = self.env['stock.picking'].create(values)
                else:
                    picking_type_id = self.env.ref('stock.picking_type_out')
                    dest_location_id = self.env.ref('stock.stock_location_suppliers')
                    location_id = self.env.ref('stock.stock_location_stock')

                    values = {
                        'partner_id': rec.order_id.partner_id.id,
                        'sale_id': rec.order_id.id,
                        'origin': rec.order_id.name,
                        'picking_type_id': picking_type_id.id,
                        'scheduled_date': rec.order_id.date_order,
                        'location_dest_id': dest_location_id.id,
                        'location_id': location_id.id,
                        'move_ids_without_package': [((0, 0, {
                            'product_id': rec.product_id.id,
                            'name': '',
                            'origin': rec.order_id.name,
                            'quantity_done': 1,
                            'product_uom_qty': rec.product_uom_qty,
                            # 'expected_delivery_date': expected_delivery_date,
                            'material_type': rec.material_type,
                            'location_dest_id': dest_location_id.id,
                            'location_id': location_id.id,
                        }))]
                    }
                    if values['partner_id']:
                        stock_pick_create = self.env['stock.picking'].create(values)
                        stock.update({
                            'sale_id': rec.order_id.id,
                        })
        return True
