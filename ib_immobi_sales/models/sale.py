# -*- coding: utf-8 -*-
# © 2017 Ibrohim Binladin | ibradiiin@gmail.com | +62-838-7190-9782 | http://ibrohimbinladin.wordpress.com
##########################################################################################################
import time
from openerp import SUPERUSER_ID
from openerp.osv import fields, osv
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT


class sale_order_tax_line(osv.osv):
    _name = "sale.order.tax.line"
    _description = "Sale Order Tax"

    def _count_factor(self, cr, uid, ids, name, args, context=None):
        res = {}
        for order_tax in self.browse(cr, uid, ids, context=context):
            res[order_tax.id] = {
                'factor_base': 1.0,
                'factor_tax': 1.0,
            }
            if order_tax.amount <> 0.0:
                factor_tax = order_tax.tax_amount / order_tax.amount
                res[order_tax.id]['factor_tax'] = factor_tax

            if order_tax.base <> 0.0:
                factor_base = order_tax.base_amount / order_tax.base
                res[order_tax.id]['factor_base'] = factor_base

        return res

    _columns = {
        'order_id': fields.many2one('sale.order', 'Sale Order', required=True, ondelete='cascade', select=True),
        'name': fields.char('Tax Description', size=64, required=True),
        'base': fields.float('Base', digits_compute=dp.get_precision('Account')),
        'amount': fields.float('Amount', digits_compute=dp.get_precision('Account')),
        'manual': fields.boolean('Manual'),
        'base_code_id': fields.many2one('account.tax.code', 'Base Code', help="The account basis of the tax declaration."),
        'base_amount': fields.float('Base Code Amount', digits_compute=dp.get_precision('Account')),
        'tax_code_id': fields.many2one('account.tax.code', 'Tax Code', help="The tax basis of the tax declaration."),
        'tax_amount': fields.float('Tax Code Amount', digits_compute=dp.get_precision('Account')),
        'company_id': fields.related('order_id', 'company_id', type='many2one', relation='res.company', string='Company', store=True, readonly=True),
        'factor_base': fields.function(_count_factor, string='Multipication factor for Base code', type='float', multi="all"),
        'factor_tax': fields.function(_count_factor, string='Multipication factor Tax code', type='float', multi="all")
    }

    def base_change(self, cr, uid, ids, base, currency_id=False, company_id=False, date_order=False):
        cur_obj = self.pool.get('res.currency')
        company_currency = False
        factor = 1
        if date_order:
            dto = str(date_order).split(" ")
            date_order = dto[0]
        if ids:
            factor = self.read(cr, uid, ids[0], ['factor_base'])['factor_base']
        if company_id:
            company_currency = self.pool.get('res.company').read(cr, uid, [company_id], ['currency_id'])[0]['currency_id'][0]
        if currency_id and company_currency:
            base = cur_obj.compute(cr, uid, currency_id, company_currency, base*factor, context={'date': date_order or fields.date.context_today(self, cr, uid)}, round=False)
        return {'value': {'base_amount':base}}

    def amount_change(self, cr, uid, ids, amount, currency_id=False, company_id=False, date_order=False):
        cur_obj = self.pool.get('res.currency')
        company_currency = False
        if date_order:
            dto = str(date_order).split(" ")
            date_order = dto[0]
        if company_id:
            company_currency = self.pool.get('res.company').read(cr, uid, [company_id], ['currency_id'])[0]['currency_id'][0]
        if currency_id and company_currency:
            amount = cur_obj.compute(cr, uid, currency_id, company_currency, amount, context={'date': date_order or fields.date.context_today(self, cr, uid)}, round=False)
        tax_rec = self.browse(cr, uid, ids)
        tax_sign = (tax_rec[0].tax_amount / tax_rec[0].amount) if tax_rec and tax_rec[0].amount else 1
        return {'value': {'tax_amount': amount * tax_sign}}

    _defaults = {
        'manual': 1,
        'base_amount': 0.0,
        'tax_amount': 0.0,
    }

    def compute(self, cr, uid, oid, context=None):
        tax_grouped = {}
        tax_obj = self.pool.get('account.tax')
        cur_obj = self.pool.get('res.currency')
        so = self.pool.get('sale.order').browse(cr, uid, oid, context=context)
        cur = so.currency_id
        company_currency = self.pool['res.company'].browse(cr, uid, so.company_id.id).currency_id.id
        date_order = False
        if so.date_order:
            dto = str(so.date_order).split(" ")
            date_order = dto[0]

        for line in so.order_line:
            for tax in tax_obj.compute_all(cr, uid, line.tax_id, (line.price_unit* (1-(line.discount or 0.0)/100.0)), line.product_uom_qty, line.product_id, so.partner_id)['taxes']:
                val={}
                val['order_id'] = so.id
                val['name'] = tax['name']
                val['amount'] = tax['amount']
                val['manual'] = False
                val['base'] = cur_obj.round(cr, uid, cur, tax['price_unit'] * line['product_uom_qty'])

                if tax['base_sign'] or tax['tax_sign']:
                    val['base_code_id'] = tax['base_code_id']
                    val['tax_code_id'] = tax['tax_code_id']
                    val['base_amount'] = cur_obj.compute(cr, uid, so.currency_id.id, company_currency, val['base'] * tax['base_sign'], context={'date': date_order or fields.date.context_today(self, cr, uid, context=context)}, round=False)
                    val['tax_amount'] = cur_obj.compute(cr, uid, so.currency_id.id, company_currency, val['amount'] * tax['tax_sign'], context={'date': date_order or fields.date.context_today(self, cr, uid, context=context)}, round=False)
                else:
                    val['base_code_id'] = tax['ref_base_code_id']
                    val['tax_code_id'] = tax['ref_tax_code_id']
                    val['base_amount'] = cur_obj.compute(cr, uid, so.currency_id.id, company_currency, val['base'] * tax['ref_base_sign'], context={'date': date_order or fields.date.context_today(self, cr, uid, context=context)}, round=False)
                    val['tax_amount'] = cur_obj.compute(cr, uid, so.currency_id.id, company_currency, val['amount'] * tax['ref_tax_sign'], context={'date': date_order or fields.date.context_today(self, cr, uid, context=context)}, round=False)

                key = (val['tax_code_id'], val['base_code_id'])
                if not key in tax_grouped:
                    tax_grouped[key] = val
                else:
                    tax_grouped[key]['amount'] += val['amount']
                    tax_grouped[key]['base'] += val['base']
                    tax_grouped[key]['base_amount'] += val['base_amount']
                    tax_grouped[key]['tax_amount'] += val['tax_amount']

        for t in tax_grouped.values():
            t['base'] = cur_obj.round(cr, uid, cur, t['base'])
            t['amount'] = cur_obj.round(cr, uid, cur, t['amount'])
            t['base_amount'] = cur_obj.round(cr, uid, cur, t['base_amount'])
            t['tax_amount'] = cur_obj.round(cr, uid, cur, t['tax_amount'])
        return tax_grouped

sale_order_tax_line()


class sale_order(osv.osv):
    _inherit = "sale.order"

    def _amount_line_tax(self, cr, uid, line, context=None):
        val = 0.0
        line_obj = self.pool['sale.order.line']
        price = line_obj._calc_line_base_price(cr, uid, line, context=context)
        qty = line_obj._calc_line_quantity(cr, uid, line, context=context)
        for c in self.pool['account.tax'].compute_all(
                cr, uid, line.tax_id, price, qty, line.product_id,
                line.order_id.partner_id)['taxes']:
            val += c.get('amount', 0.0)
        return val

    def _amount_all_wrapper(self, cr, uid, ids, field_name, arg, context=None):
        """ Wrapper because of direct method passing as parameter for function fields """
        return self._amount_all(cr, uid, ids, field_name, arg, context=context)

    def _amount_all(self, cr, uid, ids, field_name, arg, context=None):
        cur_obj = self.pool.get('res.currency')
        items_combo = self.pool.get('product.combo.item')
        res = {}
        for order in self.browse(cr, uid, ids, context=context):
            res[order.id] = {
                'amount_untaxed': 0.0,
                'amount_tax': 0.0,
                'amount_total': 0.0,
                'gross_margin': 0.0,
                'gm_percent': 0.0,
                'gross_profit': 0.0,
                'gp_percent': 0.0,
                'net_profit': 0.0,
                'np_percent': 0.0,
            }
            val = val1 = direct_cost = gm = gm_percent = gp = gp_percent = np = np_percent = indirect_cost = 0.0
            cur = order.pricelist_id.currency_id
            tmpl_ids = []
            for line in order.order_line:
                val1 += line.price_subtotal
                val += self._amount_line_tax(cr, uid, line, context=context)
                if line.product_id and line.product_id.product_tmpl_id:
                    tmpl_ids.append(line.product_id.product_tmpl_id.id)

            combo_ids = items_combo.search(cr, uid, [('product_tmpl_id','in',tuple(tmpl_ids))], context=context) or []
            direct_categ = ('DIRECT COST','Direct Cost','direct cost')
            indirect_categ = ('INDIRECT COST','Indirect Cost','indirect cost')
            for combo in items_combo.browse(cr, uid, combo_ids, context=context):
                cpl_tmpl = combo.product_id.product_tmpl_id
                if cpl_tmpl.categ_id:
                    if cpl_tmpl.categ_id.name in direct_categ:
                        direct_cost += combo.combo_subtotal
                    if cpl_tmpl.categ_id.name in indirect_categ:
                        indirect_cost += combo.combo_subtotal
                    if cpl_tmpl.categ_id.parent_id:
                        if cpl_tmpl.categ_id.parent_id.name in direct_categ:
                            direct_cost += combo.combo_subtotal
                        if cpl_tmpl.categ_id.parent_id.name in indirect_categ:
                            indirect_cost += combo.combo_subtotal

            if order.amount_untaxed > 0:
                gm = order.amount_untaxed - direct_cost
                gm_percent = (gm / order.amount_untaxed) * 100.0
                gp = gm - indirect_cost
                gp_percent = (gp / order.amount_untaxed) * 100.0
                np = gp - order.amount_tax
                np_percent = (np / order.amount_untaxed) * 100.0

            res[order.id]['amount_tax'] = cur_obj.round(cr, uid, cur, val)
            res[order.id]['amount_untaxed'] = cur_obj.round(cr, uid, cur, val1)
            res[order.id]['amount_total'] = res[order.id]['amount_untaxed'] + res[order.id]['amount_tax']
            res[order.id]['gross_margin'] = cur_obj.round(cr, uid, cur, gm)
            res[order.id]['gm_percent'] = cur_obj.round(cr, uid, cur, gm_percent)
            res[order.id]['gross_profit'] = cur_obj.round(cr, uid, cur, gp)
            res[order.id]['gp_percent'] = cur_obj.round(cr, uid, cur, gp_percent)
            res[order.id]['net_profit'] = cur_obj.round(cr, uid, cur, np)
            res[order.id]['np_percent'] = cur_obj.round(cr, uid, cur, np_percent)
        return res

    def _get_order(self, cr, uid, ids, context=None):
        result = {}
        for line in self.pool.get('sale.order.line').browse(cr, uid, ids, context=context):
            result[line.order_id.id] = True
        return result.keys()

    def _get_order_tax(self, cr, uid, ids, context=None):
        result = {}
        for taxline in self.pool.get('sale.order.tax.line').browse(cr, uid, ids, context=context):
            result[taxline.order_id.id] = True
        return result.keys()

    _columns = {
        'sale_tax_line': fields.one2many('sale.order.tax.line', 'order_id', 'Tax Lines', readonly=True,
                    states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}, copy=True),
        'gross_margin': fields.function(_amount_all_wrapper, digits_compute=dp.get_precision('Account'),
            string='Gross Margin',
            store={
                'sale.order': (lambda self, cr, uid, ids, c={}: ids, ['order_line', 'sale_tax_line', 'amount_untaxed'], 20),
                'sale.order.line': (_get_order, ['price_unit', 'tax_id', 'discount', 'product_uom_qty'], 20),
                'sale.order.tax.line': (_get_order_tax, ['amount'], 20),
            }, multi='sums'),
        'gm_percent': fields.function(_amount_all_wrapper, digits_compute=dp.get_precision('Account'),
            string='Gross Margin (Percent)',
            store={
                'sale.order': (lambda self, cr, uid, ids, c={}: ids, ['order_line', 'sale_tax_line', 'amount_untaxed'], 20),
                'sale.order.line': (_get_order, ['price_unit', 'tax_id', 'discount', 'product_uom_qty'], 20),
                'sale.order.tax.line': (_get_order_tax, ['amount'], 20),
            }, multi='sums', help="Gross Margin dalam persentase"),
        'gross_profit': fields.function(_amount_all_wrapper, digits_compute=dp.get_precision('Account'),
            string='Gross Profit',
            store={
                'sale.order': (lambda self, cr, uid, ids, c={}: ids, ['order_line', 'sale_tax_line', 'amount_untaxed'], 20),
                'sale.order.line': (_get_order, ['price_unit', 'tax_id', 'discount', 'product_uom_qty'], 20),
                'sale.order.tax.line': (_get_order_tax, ['amount'], 20),
            }, multi='sums', help="Keuntungan sebelum pajak / keuntungan kotor."),
        'gp_percent': fields.function(_amount_all_wrapper, digits_compute=dp.get_precision('Account'),
            string='Gross Profit (Percent)',
            store={
                'sale.order': (lambda self, cr, uid, ids, c={}: ids, ['order_line', 'sale_tax_line', 'amount_untaxed'], 20),
                'sale.order.line': (_get_order, ['price_unit', 'tax_id', 'discount', 'product_uom_qty'], 20),
                'sale.order.tax.line': (_get_order_tax, ['amount'], 20),
            }, multi='sums'),
        'net_profit': fields.function(_amount_all_wrapper, digits_compute=dp.get_precision('Account'),
            string='Net Profit',
            store={
                'sale.order': (lambda self, cr, uid, ids, c={}: ids, ['order_line','sale_tax_line','amount_untaxed'], 20),
                'sale.order.line': (_get_order, ['price_unit', 'tax_id', 'discount', 'product_uom_qty'], 20),
                'sale.order.tax.line': (_get_order_tax, ['amount'], 20),
            }, multi='sums', help="Keuntungan setelah pajak / keuntungan bersih."),
        'np_percent': fields.function(_amount_all_wrapper, digits_compute=dp.get_precision('Account'),
            string='Net Profit (Percent)',
            store={
                'sale.order': (lambda self, cr, uid, ids, c={}: ids, ['order_line', 'sale_tax_line', 'amount_untaxed'], 20),
                'sale.order.line': (_get_order, ['price_unit', 'tax_id', 'discount', 'product_uom_qty'], 20),
                'sale.order.tax.line': (_get_order_tax, ['amount'], 20),
            }, multi='sums'),
        'amount_untaxed': fields.function(_amount_all_wrapper, digits_compute=dp.get_precision('Account'),
            string='Untaxed Amount',
            store={
                'sale.order': (lambda self, cr, uid, ids, c={}: ids, ['order_line', 'sale_tax_line', 'amount_untaxed'], 20),
                'sale.order.line': (_get_order, ['price_unit', 'tax_id', 'discount', 'product_uom_qty'], 20),
                'sale.order.tax.line': (_get_order_tax, ['amount'], 20),
            }, multi='sums', help="The amount without tax.", track_visibility='always'),
        'amount_tax': fields.function(_amount_all_wrapper, digits_compute=dp.get_precision('Account'),
            string='Taxes',
            store={
                'sale.order': (lambda self, cr, uid, ids, c={}: ids, ['order_line', 'sale_tax_line', 'amount_untaxed'], 20),
                'sale.order.line': (_get_order, ['price_unit', 'tax_id', 'discount', 'product_uom_qty'], 20),
                'sale.order.tax.line': (_get_order_tax, ['amount'], 20),
            }, multi='sums', help="The tax amount."),
        'amount_total': fields.function(_amount_all_wrapper, digits_compute=dp.get_precision('Account'),
            string='Total',
            store={
                'sale.order': (lambda self, cr, uid, ids, c={}: ids, ['order_line', 'sale_tax_line', 'amount_untaxed'], 20),
                'sale.order.line': (_get_order, ['price_unit', 'tax_id', 'discount', 'product_uom_qty'], 20),
                'sale.order.tax.line': (_get_order_tax, ['amount'], 20),
            },multi='sums', help="The total amount."),
        'due_date_quo': fields.date('Due Date Quotation', readonly=True, select=True, copy=False,
            states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}),
        'checked_by': fields.many2one('res.users', 'Checked by', readonly=True, copy=False,
                states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}),
        'approved_by': fields.many2one('res.users', 'Approved by', readonly=True, copy=False,
                states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}),
    }

    def button_calculate_taxes(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        ctx = context.copy()
        sotl_obj = self.pool.get('sale.order.tax.line')
        for id in ids:
            cr.execute("DELETE FROM sale_order_tax_line WHERE order_id=%s AND manual is False", (id,))
            partner = self.browse(cr, uid, id, context=ctx).partner_id
            if partner.lang:
                ctx.update({'lang': partner.lang})
            for taxe in sotl_obj.compute(cr, uid, id, context=ctx).values():
                sotl_obj.create(cr, uid, taxe)
        # Update the stored value (fields.function), so we write to trigger recompute
        self.pool.get('sale.order').write(cr, uid, ids, {'order_line':[]}, context=ctx)
        return True

    def button_dummy(self, cr, uid, ids, context=None):
        self.button_calculate_taxes(cr, uid, ids, context)
        return True

    def create(self, cr, uid, vals, context=None):
        if context is None:
            context = {}
        result = super(sale_order, self).create(cr, uid, vals, context=context)
        if vals.get('order_line',[]) or vals.get('sale_order_tax_line',[]):
            self.button_calculate_taxes(cr, uid, [result], context)
        return result

sale_order()


class sale_order_line(osv.osv):
    _inherit = "sale.order.line"

    def _get_subtotal_percentage(self, cr, uid, ids, field_name, arg, context=None):
        res = dict.fromkeys(ids, 0.0)
        for line in self.browse(cr, uid, ids, context=context):
            res[line.id] = (line.price_subtotal / line.order_id.amount_untaxed)*100.0 if line.order_id.amount_untaxed > 0 else 0.0
        return res

    _columns = {
        'subtotal_percentage': fields.function(_get_subtotal_percentage, type='float', string='Subtotal (Percent)',
                                        digits_compute=dp.get_precision('Account')),
    }

sale_order_line()



