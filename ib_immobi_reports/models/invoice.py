# -*- coding: utf-8 -*-
# � 2017 Ibrohim Binladin | ibradiiin@gmail.com | +62-838-7190-9782 | http://ibrohimbinladin.wordpress.com
##########################################################################################################
from openerp.osv import osv
import openerp.addons.decimal_precision as dp
from openerp import models, fields, api
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp

BULAN = [(0,''), (1,'Januari'), (2,'Februari'),(3,'Maret'),(4,'April'), (5,'Mei'), (6,'Juni'),
        (7,'Juli'), (8,'Agustus'), (9,'September'),(10,'Oktober'), (11,'November'), (12,'Desember')]

class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    @api.one
    @api.depends('invoice_line.price_subtotal', 'tax_line.amount', 'invoice_line.discount_subtotal',
                 'invoice_line.subtotal_without_disc')
    def _compute_amount(self):
        self.amount_untaxed = sum(line.price_subtotal for line in self.invoice_line)
        self.amount_discount = sum(line.discount_subtotal for line in self.invoice_line)
        self.amount_without_discount = sum(line.subtotal_without_disc for line in self.invoice_line)
        self.amount_tax = sum(line.amount for line in self.tax_line)
        self.amount_total = self.amount_untaxed + self.amount_tax


    amount_untaxed = fields.Float(string='Subtotal', digits=dp.get_precision('Account'),
                    store=True, readonly=True, compute='_compute_amount', track_visibility='always')
    amount_discount = fields.Float(string='Discount', digits=dp.get_precision('Account'),
                    store=True, readonly=True, compute='_compute_amount')
    amount_tax = fields.Float(string='Tax', digits=dp.get_precision('Account'),
                    store=True, readonly=True, compute='_compute_amount')
    amount_total = fields.Float(string='Total', digits=dp.get_precision('Account'),
                    store=True, readonly=True, compute='_compute_amount')
    amount_without_discount = fields.Float(string='Total', digits=dp.get_precision('Account'),
                    store=True, readonly=True, compute='_compute_amount')


    @api.multi
    def print_invoice_immobi(self):
        assert len(self) == 1, 'This option should only be used for a single id at a time.'
        for inv in self:
            tanggal_indo = str("")
            if inv.date_invoice:
                date = str(inv.date_invoice).split("-")
                tanggal_indo = str(date[2]) + " " + str(BULAN[int(date[1])][1]).title() + " " + str(date[0])
        datas = {
            'ids': self.ids,
            'model': 'account.invoice',
            'form': self.read()[0],
            'invoice_date': tanggal_indo,
        }
        return {
            'type': 'ir.actions.report.xml',
            'report_name': "acc.invoice.pdf",
            'datas': datas,
            'nodestroy': True
        }

    @api.multi
    def print_request_report(self):
        assert len(self) == 1, 'This option should only be used for a single id at a time.'
        report_name = self._context.get('report_type') or str("")
        number = str("")
        employee_id = 0; move_id = 0; ref_advance_id = 0
        for inv in self:
            if (not inv.number) or (not inv.internal_number) or (not inv.move_id):
                raise osv.except_osv(_('Peringatan !!!'), _("Nomor Dokumen kosong (NULL), silahkan klik Validate dan cetak kembali..."))
            if not inv.employee_id:
                raise osv.except_osv(_('Peringatan !!!'), _("Employee ID kosong (NULL) atau data karyawan belum terdefinisi, silahkan cek kembali..."))
            if inv.advance_type=='settlement' and (not inv.reimburse) and (not inv.medical) and (not inv.ref_advance_id):
                raise osv.except_osv(_('Peringatan !!!'), _("Advance Reference kosong (NULL), silahkan cek kembali..."))
            number = str(inv.number)
            employee_id = int(inv.employee_id and inv.employee_id.id)
            move_id = int(inv.move_id and inv.move_id.id)
            ref_advance_id = int(inv.ref_advance_id and inv.ref_advance_id.id)
        datas = {
            'ids': self.ids,
            'model': 'account.invoice',
            'form': self.read()[0],
            'number': number,
            'employee_id': employee_id,
            'move_id': move_id,
            'ref_advance_id': ref_advance_id
        }
        return {
            'type': 'ir.actions.report.xml',
            'report_name': report_name,
            'datas': datas,
            'nodestroy': True
        }


    # def print_invoice_immobi(self, cr, uid, ids, context=None):
    #     assert len(ids) == 1, 'This option should only be used for a single id at a time.'
    #     context = context or {}
    #     for id in ids:
    #         tanggal_indo = ''
    #         inv = self.pool.get('account.invoice').browse(cr, uid, id, context=context)
    #         if inv.date_invoice:
    #             date = str(inv.date_invoice).split("-")
    #             tanggal_indo = str(date[2]) + " " + str(BULAN[int(date[1])][1]).title() + " " + str(date[0])
    #     datas = {
    #         'ids': ids,
    #         'model': 'account.invoice',
    #         'form': self.read(cr, uid, ids[0], context=context),
    #         'invoice_date': tanggal_indo,
    #     }
    #     return {
    #         'type': 'ir.actions.report.xml',
    #         'report_name': "acc.invoice.pdf",
    #         'datas': datas,
    #         'nodestroy': True
    #     }

    # def print_request_report(self, cr, uid, ids, context=None):
    #     assert len(ids) == 1, 'This option should only be used for a single id at a time.'
    #     context = context or {}
    #     report_name = context.get('report_type') or ""
    #     number = _("")
    #     employee_id=0; move_id=0; ref_advance_id=0
    #     for inv in self.browse(cr, uid, ids, context=context):
    #         if (not inv.number) or (not inv.internal_number) or (not inv.move_id):
    #             raise osv.except_osv(_('Peringatan !!!'), _("Nomor Dokumen kosong (NULL), silahkan klik Validate dan cetak kembali..."))
    #         if not inv.employee_id:
    #             raise osv.except_osv(_('Peringatan !!!'), _("Employee ID kosong (NULL) atau data karyawan belum terdefinisi, silahkan cek kembali..."))
    #         if inv.advance_type=='settlement' and (not inv.reimburse) and (not inv.medical) and (not inv.ref_advance_id):
    #             raise osv.except_osv(_('Peringatan !!!'), _("Advance Reference kosong (NULL), silahkan cek kembali..."))
    #         number = str(inv.number)
    #         employee_id = int(inv.employee_id and inv.employee_id.id)
    #         move_id = int(inv.move_id and inv.move_id.id)
    #         ref_advance_id = int(inv.ref_advance_id and inv.ref_advance_id.id)
    #     datas = {
    #         'ids': ids,
    #         'model': 'account.invoice',
    #         'form': self.read(cr, uid, ids[0], context=context),
    #         'number': number,
    #         'employee_id': employee_id,
    #         'move_id': move_id,
    #         'ref_advance_id': ref_advance_id
    #     }
    #     return {
    #         'type': 'ir.actions.report.xml',
    #         'report_name': report_name,
    #         'datas': datas,
    #         'nodestroy': True
    #     }



class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    @api.one
    @api.depends('price_unit', 'discount', 'invoice_line_tax_id', 'quantity', 'discount_method',
                 'product_id', 'invoice_id.partner_id', 'invoice_id.currency_id')
    def _compute_price(self):
        price = self.price_unit * (1 - (self.discount or 0.0) / 100.0)
        product_qty = self.quantity
        discount = (self.price_unit * self.quantity) * ((self.discount or 0.0) / 100.0)
        self.discount_subtotal = self.invoice_id.currency_id.round(discount)
        if self.discount_method == 'fixed':
            price = (self.quantity * self.price_unit) - self.discount
            product_qty = 1.0
            self.discount_subtotal = self.invoice_id.currency_id.round(self.discount)
        taxes = self.invoice_line_tax_id.compute_all(price, product_qty, product=self.product_id, partner=self.invoice_id.partner_id)
        pajak = self.invoice_line_tax_id.compute_all(self.price_unit, self.quantity, product=self.product_id, partner=self.invoice_id.partner_id)
        self.price_subtotal = taxes['total']
        self.subtotal_without_disc = pajak['total']
        if self.invoice_id:
            self.price_subtotal = self.invoice_id.currency_id.round(self.price_subtotal)
            self.subtotal_without_disc = self.invoice_id.currency_id.round(self.subtotal_without_disc)

    @api.model
    def _default_price_unit(self):
        if not self._context.get('check_total'):
            return 0
        total = self._context['check_total']
        for l in self._context.get('invoice_line', []):
            if isinstance(l, (list, tuple)) and len(l) >= 3 and l[2]:
                vals = l[2]
                #price = vals.get('price_unit', 0) * (1 - vals.get('discount', 0) / 100.0)
                total = total - (vals.get('price_unit', 0) * vals.get('quantity'))
                taxes = vals.get('invoice_line_tax_id')
                if taxes and len(taxes[0]) >= 3 and taxes[0][2]:
                    taxes = self.env['account.tax'].browse(taxes[0][2])
                    tax_res = taxes.compute_all(vals.get('price_unit', 0), vals.get('quantity'),
                                                product=vals.get('product_id'), partner=self._context.get('partner_id'))
                    for tax in tax_res['taxes']:
                        total = total - tax['amount']
        return total


    discount_method = fields.Selection([
            ('fixed', 'Fixed Amount (Rp)'),
            ('percent', 'Percentage (%)'),], string="Discount Method")  #default="percent"
    discount = fields.Float(string='Discount', digits=dp.get_precision('Discount'), default=0.0)
    discount_subtotal = fields.Float(string='Subtotal Discount', digits=dp.get_precision('Account'),
            readonly=True, compute='_compute_price')
    subtotal_without_disc = fields.Float(string='Subtotal Without Discount', digits=dp.get_precision('Account'),
            store=True, readonly=True, compute='_compute_price')
    price_subtotal = fields.Float(string='Amount', digits=dp.get_precision('Account'),
            store=True, readonly=True, compute='_compute_price')

    @api.multi
    def onchange_discount(self):
        return {'value': {'discount': 0.0, }}




class AccountInvoiceTax(models.Model):
    _inherit = "account.invoice.tax"

    @api.v8
    def compute(self, invoice):
        tax_grouped = {}
        currency = invoice.currency_id.with_context(date=invoice.date_invoice or fields.Date.context_today(invoice))
        company_currency = invoice.company_id.currency_id
        for line in invoice.invoice_line:
            price_unit = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            product_qty = line.quantity
            if line.discount_method == "fixed":
                price_unit = (line.quantity * line.price_unit) - line.discount
                product_qty = 1.0
            taxes = line.invoice_line_tax_id.compute_all(price_unit, product_qty,
                    line.product_id, invoice.partner_id)['taxes']
            for tax in taxes:
                val = {
                    'invoice_id': invoice.id,
                    'name': tax['name'],
                    'amount': tax['amount'],
                    'manual': False,
                    'sequence': tax['sequence'],
                    'base': currency.round(tax['price_unit'] * line['quantity']),
                }
                if invoice.type in ('out_invoice', 'in_invoice'):
                    val['base_code_id'] = tax['base_code_id']
                    val['tax_code_id'] = tax['tax_code_id']
                    val['base_amount'] = currency.compute(val['base'] * tax['base_sign'], company_currency, round=False)
                    val['tax_amount'] = currency.compute(val['amount'] * tax['tax_sign'], company_currency, round=False)
                    val['account_id'] = tax['account_collected_id'] or line.account_id.id
                    val['account_analytic_id'] = tax['account_analytic_collected_id']
                else:
                    val['base_code_id'] = tax['ref_base_code_id']
                    val['tax_code_id'] = tax['ref_tax_code_id']
                    val['base_amount'] = currency.compute(val['base'] * tax['ref_base_sign'], company_currency,
                                                          round=False)
                    val['tax_amount'] = currency.compute(val['amount'] * tax['ref_tax_sign'], company_currency,
                                                         round=False)
                    val['account_id'] = tax['account_paid_id'] or line.account_id.id
                    val['account_analytic_id'] = tax['account_analytic_paid_id']

                # If the taxes generate moves on the same financial account as the invoice line
                # and no default analytic account is defined at the tax level, propagate the
                # analytic account from the invoice line to the tax line. This is necessary
                # in situations were (part of) the taxes cannot be reclaimed,
                # to ensure the tax move is allocated to the proper analytic account.
                if not val.get('account_analytic_id') and line.account_analytic_id and val[
                    'account_id'] == line.account_id.id:
                    val['account_analytic_id'] = line.account_analytic_id.id

                key = (val['tax_code_id'], val['base_code_id'], val['account_id'])
                if not key in tax_grouped:
                    tax_grouped[key] = val
                else:
                    tax_grouped[key]['base'] += val['base']
                    tax_grouped[key]['amount'] += val['amount']
                    tax_grouped[key]['base_amount'] += val['base_amount']
                    tax_grouped[key]['tax_amount'] += val['tax_amount']

        for t in tax_grouped.values():
            t['base'] = currency.round(t['base'])
            t['amount'] = currency.round(t['amount'])
            t['base_amount'] = currency.round(t['base_amount'])
            t['tax_amount'] = currency.round(t['tax_amount'])

        return tax_grouped


