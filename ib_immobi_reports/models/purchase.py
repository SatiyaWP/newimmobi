# -*- coding: utf-8 -*-
# © 2017 Ibrohim Binladin | ibradiiin@gmail.com | +62-838-7190-9782 | http://ibrohimbinladin.wordpress.com
##########################################################################################################
import amount_to_text_en
import openerp.addons.decimal_precision as dp 
#from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp import models, fields, api
import openerp.addons.jasper_reports as jasper_reports
import openerp.addons.decimal_precision as dp

# BULAN = [(0,''), (1,'Januari'), (2,'Februari'),(3,'Maret'),(4,'April'), (5,'Mei'), (6,'Juni'),
#         (7,'Juli'), (8,'Agustus'), (9,'September'),(10,'Oktober'), (11,'November'), (12,'Desember')]

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    @api.one
    @api.depends('order_line.price_subtotal','order_line.discount_subtotal', 'order_line.taxes_id', 'order_line.discount_method',
                 'order_line.price_unit', 'order_line.product_qty', 'order_line.product_id', 'order_line.subtotal_without_disc')
    def _compute_amount(self):
        self.amount_tax = 0.0
        self.amount_untaxed = sum(line.price_subtotal for line in self.order_line)
        self.amount_discount = sum(line.discount_subtotal for line in self.order_line)
        self.amount_without_discount = sum(line.subtotal_without_disc for line in self.order_line)
        for line in self.order_line:
            new_price_unit = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            new_product_qty = line.product_qty
            if line.discount_method == "fixed":
                new_price_unit = (line.product_qty * line.price_unit) - line.discount
                new_product_qty = 1.0
            taxes = line.taxes_id.compute_all(new_price_unit, new_product_qty,
                                              product=line.product_id, partner=line.order_id.partner_id)
            self.amount_tax += taxes.get('total_included', 0.0) - taxes.get('total', 0.0)
        self.amount_total = self.amount_untaxed + self.amount_tax

    @api.depends('name', 'partner_id.code', 'date_order')
    def _get_complete_number(self):
        for order in self:
            order.item_number = str(order.name)
            if order.partner_id and order.partner_id.code:
                order.item_number += "/" + _(order.partner_id.code)
            if order.date_order:
                exp = str(order.date_order).split(" ")
                seq = str(exp[0]).split("-")
                order.item_number += "/" + _(seq[0])


    amount_to_text = fields.Text('Says [Amount to Text]')
    item_number = fields.Char(compute='_get_complete_number', string='Item Number', store=True)
    amount_untaxed = fields.Float(string='Subtotal', digits=dp.get_precision('Account'),
                store=True, readonly=True, compute='_compute_amount', track_visibility='always', help="Subtotal After Discount")
    amount_discount = fields.Float(string='Discount', digits=dp.get_precision('Account'),
                store=True, readonly=True, compute='_compute_amount', help="Total Discount")
    amount_tax = fields.Float(string='Tax', digits=dp.get_precision('Account'),
                store=True, readonly=True, compute='_compute_amount')
    amount_total = fields.Float(string='Total Order', digits=dp.get_precision('Account'),
                store=True, readonly=True, compute='_compute_amount')
    amount_without_discount = fields.Float(string='Subtotal', digits=dp.get_precision('Account'),
                store=True, readonly=True, compute='_compute_amount', help="Subtotal Before Discount")

    @api.multi
    def button_dummy(self):
        for po in self:
            currency = po.currency_id.name
            text_amount = amount_to_text_en.amount_to_text(po.amount_total, 'en', currency)
            self.write({'amount_to_text': text_amount})
        return True

    @api.multi
    def print_po_immobi(self):
        assert len(self) == 1, 'This option should only be used for a single id at a time.'
        self.write({'state': "bid"})
        datas = {
            'ids': self.ids,
            'model': 'purchase.order',
            'form': self.read()[0],
        }
        return {
            'type': 'ir.actions.report.xml',
            'report_name': "purchase.order.pdf",
            'datas': datas,
            'nodestroy': True
        }

    @api.model
    def _prepare_inv_line(self, account_id, order_line):
        result = super(PurchaseOrder, self)._prepare_inv_line(account_id, order_line)
        result['discount_method'] = order_line.discount_method
        result['discount'] = order_line.discount or 0.0
        return result

    @api.model
    def _prepare_order_line_move(self, order, order_line, picking_id, group_id):
        res = super(PurchaseOrder, self)._prepare_order_line_move(order, order_line, picking_id, group_id)
        for vals in res:
            if order_line.discount_method=='percent':
                vals['price_unit'] = (vals.get('price_unit', 0.0) * (1 - (order_line.discount / 100)))
            elif order_line.discount_method=='fixed':
                vals['price_unit'] = (vals.get('price_unit', 0.0) - (order_line.discount / order_line.product_qty))
        return res

    # def print_po_immobi(self, cr, uid, ids, context=None):
    #     assert len(ids) == 1, 'This option should only be used for a single id at a time.'
    #     context = context or {}
    #     for id in ids:
    #         o = self.pool.get('purchase.order').browse(cr, uid, id, context=context)
    #         order_id = int(o.id) or ids[0]
    #         date_order = str(o.date_order).split(" ")
    #         date = str(date_order[0]).split("-")
    #         po_date = str(date[2]) + " " + str(BULAN[int(date[1])][1]).title() + " " + str(date[0]) + " " + str(date_order[1])
    #     self.signal_workflow(cr, uid, ids, 'send_rfq')
    #     datas = {
    #         'ids': ids,
    #         'model': 'purchase.order',
    #         'form': self.read(cr, uid, ids[0], context=context),
    #         #'order_date': po_date,
    #         #'order_id': order_id,
    #     }
    #     return {
    #         'type': 'ir.actions.report.xml',
    #         'report_name': "purchase.order.pdf",
    #         'datas': datas,
    #         'nodestroy': True
    #     }



class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    @api.one
    @api.depends('price_unit', 'product_qty', 'discount_method', 'discount',
                 'taxes_id', 'product_id', 'order_id.partner_id', 'order_id.currency_id')
    def _compute_amount(self):
        new_quantity = self.product_qty
        new_price_unit = self.price_unit * (1 - (self.discount or 0.0) / 100.0)
        self.discount_subtotal = (self.price_unit * self.product_qty) * ((self.discount or 0.0) / 100.0)
        if self.discount_method=='fixed':
            new_quantity = 1.0
            self.discount_subtotal = self.discount
            new_price_unit = (self.product_qty * self.price_unit) - self.discount
        taxes = self.taxes_id.compute_all(new_price_unit, new_quantity, product=self.product_id,
                                        partner=self.order_id.partner_id)
        pajak = self.taxes_id.compute_all(self.price_unit, self.product_qty, product=self.product_id,
                                          partner=self.order_id.partner_id)
        self.subtotal_without_disc = pajak['total']
        self.price_subtotal = taxes['total']
        if self.order_id:
            self.discount_subtotal = self.order_id.currency_id.round(self.discount_subtotal)
            self.subtotal_without_disc = self.order_id.currency_id.round(self.subtotal_without_disc)
            self.price_subtotal = self.order_id.currency_id.round(self.price_subtotal)


    discount_method = fields.Selection([('fixed', 'Fixed Amount (Rp)'),('percent', 'Percentage (%)')],
                string="Discount Method")  #,default="percent"
    discount = fields.Float(string='Discount', digits_compute=dp.get_precision('Discount'), default=0.0)
    discount_subtotal = fields.Float(string='Subtotal Discount', digits=dp.get_precision('Account'),
                readonly=True, compute='_compute_amount')
    subtotal_without_disc = fields.Float(string='Subtotal Without Discount', digits=dp.get_precision('Account'),
                store=True, readonly=True, compute='_compute_amount')
    price_subtotal = fields.Float(string='Amount', digits=dp.get_precision('Account'),
                store=True, readonly=True, compute='_compute_amount')

    @api.multi
    def onchange_discount(self):
        return {'value': {'discount': 0.0, }}





def purchase_order_report(cr, uid, ids, data, context):
    return {
        'parameters': {
            'title': "PURCHASE ORDER",
            #'order_date': data['order_date'],
            #'order_id': data['order_id'],
        },
    }
jasper_reports.report_jasper(
    'report.purchase.order.pdf',
    'purchase.order',
    parser=purchase_order_report
)

