# -*- coding: utf-8 -*-
# © 2017 Ibrohim Binladin | ibradiiin@gmail.com | +62-838-7190-9782 | http://ibrohimbinladin.wordpress.com
##########################################################################################################
from openerp.osv import fields, osv
import openerp.addons.decimal_precision as dp

class item_combo_product_info(osv.osv_memory):
    _name = "combo.product.info"
    _description = "Bill of Quantity Details"
    _columns = {
        'order_line_id': fields.many2one('sale.order.line', 'Sale Order Line', readonly=True),
        'items_combo_line': fields.one2many('combo.product.info.line', 'combo_info_id',
                'Bill of Quantity Details', readonly=True)
    }
    _defaults = {
        'order_line_id': lambda self, cr, uid, ctx: ctx.get('active_id', False)
    }

    def onchange_order_line_id(self, cr, uid, ids, order_line_id, context=None):
        oline = self.pool.get('sale.order.line').browse(cr, uid, order_line_id)
        items_combo_line = []
        if oline.product_id and oline.product_id.product_tmpl_id:
            for cpl in oline.product_id.product_tmpl_id.combo_product_line:
                items_combo_line.append([0, 0, {
                    'product_id': cpl.product_id and cpl.product_id.id or False,
                    'quantity': cpl.quantity or 0.0,
                    'uom_id': cpl.uom_id and cpl.uom_id.id or False,
                    'categ_id': cpl.product_id and cpl.product_id.product_tmpl_id and cpl.product_id.product_tmpl_id.categ_id.id or False,
                    'percent': (cpl.combo_subtotal / oline.price_subtotal) * 100.0,
                    }])
        return {'value': {
            'items_combo_line': items_combo_line,
        }}

item_combo_product_info()


class item_combo_product_info_line(osv.osv_memory):
    _name = "combo.product.info.line"
    _description = "BoQ Details"
    _columns = {
        'combo_info_id': fields.many2one('combo.product.info', 'Items of Combo Product'),
        'product_id': fields.many2one('product.product', 'Product'),
        'quantity': fields.float('Quantity', digits_compute=dp.get_precision('Stock Weight')),
        'uom_id': fields.many2one('product.uom', 'Unit of Measure '),
        'categ_id': fields.many2one('product.category', 'Internal Category'),
        'percent': fields.float('Percentage', digits_compute=dp.get_precision('Account')),
    }

item_combo_product_info_line()
