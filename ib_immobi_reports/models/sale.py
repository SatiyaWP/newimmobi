# -*- coding: utf-8 -*-
# © 2017 Ibrohim Binladin | ibradiiin@gmail.com | +62-838-7190-9782 | http://ibrohimbinladin.wordpress.com
##########################################################################################################
from openerp.osv import fields, osv
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp

BULAN = [(0,''), (1,'Januari'), (2,'Februari'),(3,'Maret'),(4,'April'), (5,'Mei'), (6,'Juni'),
        (7,'Juli'), (8,'Agustus'), (9,'September'),(10,'Oktober'), (11,'November'), (12,'Desember')]


class ResPartner(osv.osv):
    _inherit="res.partner"
    _columns = {
        'code': fields.char('Partner Code', copy=False),
    }



class sale_order(osv.osv):
    _inherit = "sale.order"

    def _amount_total_cost(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for order in self.browse(cr, uid, ids, context=context):
            cur = order.pricelist_id.currency_id or False
            total_cost = 0.0
            for line in order.order_line:
                total_cost += line.subtotal_cost
            res[order.id] = self.pool.get('res.currency').round(cr, uid, cur, total_cost)
        return res

    def _get_order(self, cr, uid, ids, context=None):
        result = {}
        for line in self.pool.get('sale.order.line').browse(cr, uid, ids, context=context):
            result[line.order_id.id] = True
        return result.keys()

    _columns = {
        'grand_total_cost': fields.function(_amount_total_cost,
                digits_compute=dp.get_precision('Account'), string='Total Cost',
                store={
                    'sale.order': (lambda self, cr, uid, ids, c={}: ids, ['order_line'], 10),
                    'sale.order.line': (_get_order, ['purchase_price', 'product_uom_qty'], 10),}),
    }

    def print_so_immobi(self, cr, uid, ids, context=None):
        assert len(ids) == 1, 'This option should only be used for a single id at a time.'
        context = context or {}
        report_name = context.get('report_name')
        for id in ids:
            o = self.pool.get('sale.order').browse(cr, uid, id, context=context)
            odate = str(o.date_order).split(" ")
            date = str(odate[0]).split("-")
            date_indo = str(date[2]) + " " + str(BULAN[int(date[1])][1]).title() + " " + str(date[0]) + " " + str(odate[1])
            order_id = int(o.id) or ids[0]
        self.signal_workflow(cr, uid, ids, 'quotation_sent')

        datas = {
            'ids': ids,
            'model': 'sale.order',
            'form': self.read(cr, uid, ids[0], context=context),
            'order_id': order_id,
            'order_date': date_indo,
        }

        return {
            'type': 'ir.actions.report.xml',
            'report_name': report_name,     #"sales.order.pdf",
            'datas': datas,
            'nodestroy': True
        }


    def print_boq_immobi(self, cr, uid, ids, context=None):
        assert len(ids) == 1, 'This option should only be used for a single id at a time.'
        context = context or {}
        for id in ids:
            o = self.pool.get('sale.order').browse(cr, uid, id, context=context)
            order_id = int(o.id) or ids[0]

        datas = {
            'ids': ids,
            'model': 'sale.order',
            'form': self.read(cr, uid, ids[0], context=context),
            'order_id': order_id,
            'subdir_report': "/home/odoo/custom_addons/immobi/ib_immobi_reports/report/",
        }

        return {
            'type': 'ir.actions.report.xml',
            'report_name': "boq2.pdf", #"boq.pdf",
            'datas': datas,
            'nodestroy': True
        }



class sale_order_line(osv.osv):
    _inherit = "sale.order.line"

    def _subtotal_cost_price(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        context = context or {}
        for line in self.browse(cr, uid, ids, context=context):
            cur = line.order_id.pricelist_id.currency_id
            res[line.id] = self.pool.get('res.currency').round(cr, uid, cur, (line.product_uom_qty * line.purchase_price))
        return res

    _columns = {
        'subtotal_cost': fields.function(_subtotal_cost_price, string='Subtotal Cost',
                digits_compute=dp.get_precision('Product Price')),
    }




