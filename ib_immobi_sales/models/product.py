# -*- coding: utf-8 -*-
# © 2017 Ibrohim Binladin | ibradiiin@gmail.com | +62-838-7190-9782 | http://ibrohimbinladin.wordpress.com
##########################################################################################################
from collections import Counter
from openerp.osv import fields, osv
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp


class items_combo_product(osv.osv):
    _name = "product.combo.item"
    _description = "Bill of Quantity (BoQ)"

    def _amount_combo_product(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        cur_obj = self.pool.get('res.currency')
        context = context or {}
        for combo in self.browse(cr, uid, ids, context=context):
            curr = combo.product_tmpl_id and combo.product_tmpl_id.company_id and combo.product_tmpl_id.company_id.currency_id
            res[combo.id] = { 'combo_subtotal': 0.0, }
            price = combo.product_id and combo.product_id.standard_price or 0.0
            total_line = total = (combo.quantity or 0.0) * price
            if (combo.product_id.product_tmpl_id.uom_po_id.id != combo.product_id.product_tmpl_id.uom_id.id):
                if combo.product_id.product_tmpl_id.uom_po_id.uom_type=='bigger':
                    total = total_line * (1 / combo.product_id.product_tmpl_id.uom_po_id.factor)
                elif combo.product_id.product_tmpl_id.uom_po_id.uom_type=='smaller':
                    total = total_line / combo.product_id.product_tmpl_id.uom_po_id.factor
            res[combo.id]['subtotal_line'] = cur_obj.round(cr, uid, curr, total_line)
            res[combo.id]['combo_subtotal'] = cur_obj.round(cr, uid, curr, total)
        return res

    def _get_product_category(self, cr, uid, ids, name, arg, context=None):
        res = {}
        if context is None:
            context = {}
        for ol in self.browse(cr, uid, ids, context=context):
            product = self.pool.get('product.product').browse(cr, uid, ol.product_id.id, context=context)
            res[ol.id] = product.categ_id and product.categ_id.id
        return res

    # def _get_ratio_uom_purchase(self, cr, uid, ids, name, arg, context=None):
    #     res = {}
    #     if context is None:
    #         context = {}
    #     for ol in self.browse(cr, uid, ids, context=context):
    #         product_tmpl = self.pool.get('product.template').browse(cr, uid, ol.product_tmpl_id.id, context=context)
    #         if product_tmpl.uom_po_id:  #and product_tmpl.uom_po_id.factor<>1
    #             if product_tmpl.uom_po_id.uom_type == 'smaller':
    #                 res[ol.id] = product_tmpl.uom_po_id.factor
    #             elif product_tmpl.uom_po_id.uom_type == 'bigger':
    #                 res[ol.id] = (1 / product_tmpl.uom_po_id.factor)
    #             else:
    #                 res[ol.id] = 0.0
    #     return res

    _columns = {
        'product_tmpl_id': fields.many2one('product.template', 'Product Template',
                            required=True, ondelete='cascade'),
        'product_id': fields.many2one('product.product', 'Product', domain=[('purchase_ok', '=', True)],
                            required=True, ondelete='restrict'),
        'quantity': fields.float('Quantity', digits_compute=dp.get_precision('Stock Weight'),
                        required=True),
        'uom_id': fields.many2one('product.uom', 'Unit of Measure ', required=True),
        'combo_subtotal': fields.function(_amount_combo_product, string='Total Price',
                    digits_compute=dp.get_precision('Account'), multi='sums', store=True),
        'categ_id': fields.function(_get_product_category, type='many2one', relation='product.category',
                    string='Category'),
        'subtotal_line': fields.function(_amount_combo_product, string='Subtotal',
                    digits_compute=dp.get_precision('Account'), multi='sums', store=True),
        'ratio_purchase': fields.float('Ratio UoM Purchase', digits_compute=dp.get_precision('Product Price')),
        # 'ratio_purchase': fields.function(_get_ratio_uom_purchase, type='float',
        #             digits_compute=dp.get_precision('Product Price'), string='Ratio UoM Purchase'),
    }
    _defaults = {
        'ratio_purchase': 1,
    }

    def onchange_product_id(self, cr, uid, ids, pid, context=None):
        if not pid:
            return {}
        values = {}
        product = self.pool.get('product.product').browse(cr, uid, pid, context=context)
        uom_id = product.product_tmpl_id and product.product_tmpl_id.uom_po_id and product.product_tmpl_id.uom_po_id.id
        if uom_id:
            ratio_purchase = 0.0
            if product.product_tmpl_id.uom_po_id.uom_type == 'smaller':
                ratio_purchase = product.product_tmpl_id.uom_po_id.factor
            elif product.product_tmpl_id.uom_po_id.uom_type == 'bigger':
                ratio_purchase = 1/ product.product_tmpl_id.uom_po_id.factor
            values.update({'uom_id': uom_id, 'ratio_purchase': ratio_purchase})
        return {'value':values}



class ProductTemplate(osv.osv):
    _inherit = 'product.template'

    def _calculate_cost_price(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        context = context or {}
        for pt in self.browse(cr, uid, ids, context=context):
            cur = pt.company_id.currency_id
            val = sum([cpl.combo_subtotal for cpl in pt.combo_product_line]) or 1.0
            res[pt.id] = self.pool.get('res.currency').round(cr, uid, cur, val)
        return res

    def _get_combo(self, cr, uid, ids, context=None):
        result = {}
        for combo in self.pool.get('product.combo.item').browse(cr, uid, ids, context=context):
            result[combo.product_tmpl_id.id] = True
        return result.keys()

    _columns = {
        'combo_product_line': fields.one2many('product.combo.item', 'product_tmpl_id', 'Bill of Quantity (BoQ)'),
        'combo_ok': fields.boolean('Combo Product', help="Beri tanda cek/centang jika Produk ini termasuk Item Paket / Combo."),
        'cost_price_silent': fields.function(_calculate_cost_price,
            digits_compute=dp.get_precision('Product Price'), string='Cost Price',
            store={
                'product.template': (lambda self, cr, uid, ids, c={}: ids, ['combo_product_line','standard_price'], 10),
                'product.combo.item': (_get_combo, ['quantity','product_id'], 10),
            }),
    }

    _defaults = {
        'combo_ok': False,
    }

    def create(self, cr, uid, vals, context=None):
        if context is None:
            context = {}
        #product_template_id = super(ProductTemplate, self).create(cr, uid, vals, context=context)
        combo_pid = []
        if vals.get('combo_product_line', []):
            for cpl in vals['combo_product_line']:
                combo_pid.append(cpl[2]['product_id'])

        cek_combo_line = Counter(combo_pid)
        for key, val in cek_combo_line.items():
            if (val > 1) and (key in combo_pid):
                product = self.pool.get('product.product').browse(cr, uid, key, context=context)
                raise osv.except_osv(_("Warning!!!"),
                                     _("Invalid combo product.\nYou are not allowed to input more than one same product in a combo product.\nPlease check again...\n(%s)") %
                                     (product.name_template,))

        return super(ProductTemplate, self).create(cr, uid, vals, context=context)

    def _check_combo_product(self, cr, uid, ids, context=None):
        for obj in self.browse(cr, uid, ids, context=context):
            cr.execute('select product_id, count(product_id) as total'
                       ' from product_combo_item where product_tmpl_id=%s group by product_id', (obj.id,))
            for line in cr.dictfetchall():
                if line['total'] > 1:
                    product = self.pool.get('product.product').browse(cr, uid, line['product_id'], context=context)
                    raise osv.except_osv(_('Warning!!!'),
                                _("Invalid combo product.\nYou are not allowed to input more than one same product in a combo product.\nPlease check again...\n(%s)") %
                                (product.name_template,))
        return True

    def write(self, cr, uid, ids, vals, context=None):
        res = super(ProductTemplate, self).write(cr, uid, ids, vals, context=context)
        if ('combo_product_line' in vals) or vals.get('combo_ok'):
            self._check_combo_product(cr, uid, ids, context=context)
        return res
        #return super(ProductTemplate, self).write(cr, uid, ids, vals, context=context)

    def button_calculate_boq(self, cr, uid, ids, context=None):
        return True



class product_product(osv.osv):
    _inherit = "product.product"

    def button_calculate_boq(self, cr, uid, ids, context=None):
        products = self.browse(cr, uid, ids, context=context)
        return self.pool.get("product.template")._price_get(cr, uid, products, context=context)


