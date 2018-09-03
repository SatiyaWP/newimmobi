from openerp import api, _
from openerp import fields as Fields
from openerp.osv import osv, fields, orm
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT
import openerp.addons.decimal_precision as dp
from openerp.exceptions import except_orm, Warning, RedirectWarning
import time

class res_company(orm.Model):
    _inherit = 'res.company'
    _columns = {
        'advance_journal_id': fields.many2one('account.journal', 'Advance journal',
            help="Journal used for request of advance amounts to be paid"),
        'settlement_journal_id': fields.many2one('account.journal', 'Settlement journal',
            help="Journal used for settlement of advance to be paid"),
        'advance_product_id': fields.many2one('product.product', 'Advance product',
            help="Product used for advance request"),
        }
    
class account_config_settings(orm.TransientModel):
    _inherit = 'account.config.settings'
    _columns = {
        'advance_journal_id': fields.related(
            'company_id', 'advance_journal_id',
            type='many2one',
            relation="account.journal",
            string="Advance journal",
            help='Journal used for request of advance amounts to be paid'),
        'settlement_journal_id': fields.related(
            'company_id', 'settlement_journal_id',
            type='many2one',
            relation="account.journal",
            string="Settlement journal",
            help='Journal used for settlement of advance to be paid'),
        'advance_product_id': fields.related(
            'company_id', 'advance_product_id',
            type='many2one',
            relation="product.product",
            string="Advance product",
            help='Product used for advance request'),
    }
    
    def onchange_company_id(self, cr, uid, ids, company_id, context=None):
        res = super(account_config_settings, self).onchange_company_id(cr, uid, ids, company_id, context=context)
        if company_id:
            company = self.pool.get('res.company').browse(cr, uid, company_id, context=context)
            res['value'].update({
                'advance_journal_id': (company.advance_journal_id
                    and company.advance_journal_id.id or False),
                'settlement_journal_id': (company.settlement_journal_id
                    and company.settlement_journal_id.id or False),
                'advance_product_id': (company.advance_product_id
                    and company.advance_product_id.id or False),
                })
        else: 
            res['value'].update({
                'advance_journal_id': False,
                'settlement_journal_id': False,
                'advance_product_id': False,
                })
        return res
    
class res_partner(osv.osv):
    _inherit = 'res.partner'
     
    def _advance_search(self, cr, uid, ids, field_names, arg, context=None):
        ctx = context.copy()
        ctx['all_fiscalyear'] = True
        user = self.pool.get('res.users').browse(cr, uid, uid)
#         prop = self.pool.get('ir.property')
#         adv_dom = [('name', '=', 'property_advance_account'), ('company_id', '=', 1)]
#         prop_ids = prop.search(cr, uid, adv_dom, limit=1)
#         prop_data = prop.read(cr, uid, prop_ids, ['name', 'value_reference', 'res_id'])
#         adv_account = prop_data and prop_data[0].get('value_reference', False) and int(prop_data[0]['value_reference'].split(',')[1]) or False
#         adv_account = adv_account or self.browse(cr, uid, ids).property_advance_account.id
        adv_account = user.company_id.advance_product_id.property_account_expense.id
        if not adv_account:
            adv_account = None
        query = self.pool.get('account.move.line')._query_get(cr, uid, context=ctx)
        cr.execute("""SELECT l.partner_id, SUM(l.debit-l.credit)
                      FROM account_move_line l
                      LEFT JOIN account_account a ON (l.account_id=a.id)
                      WHERE a.id IN %s
                      AND l.partner_id IN %s
                      AND l.reconcile_id IS NULL
                      AND """ + query + """
                      GROUP BY l.partner_id
                      """,
                   (tuple([adv_account]), tuple(ids),))
        
        res = {}
        for pid, val in cr.fetchall():
            res[pid] = val or 0.0
        return res
    
    _columns = {
        'advance': fields.function(_advance_search, string='Total Advance', readonly=True, help="Total unreconciled advance amount of this partner"),
        'property_advance_account': fields.property(
            type='many2one',
            relation='account.account',
            string="Advance Account",
            domain="[('type', '=', 'payable')]",
            help="This account will be used instead of the default one as the advance account for the current partner",
            required=True),
    }
    
class account_invoice_line(osv.osv):
    _inherit = 'account.invoice.line'
    
    def default_get(self, cr, uid, fields_list, context=None):
        res = super(account_invoice_line, self).default_get(cr, uid, fields_list, context)
        user = self.pool.get('res.users').browse(cr, uid, uid)
        if context.get('advance_type', False) == 'request':
            product_id = user.company_id.advance_product_id
            if not product_id:
                raise osv.except_osv(_('Warning!'),
                                      _('Please configure advance product\n Goto Settings -> Configuration -> Accounting !'))
            if 'product_id' in fields_list:
                res['product_id'] = product_id.id
            if 'account_id' in fields_list:
                res['account_id'] = user.partner_id.property_account_payable.id
#                 res['account_id'] = user.partner_id.property_advance_account.id
            if 'name' in fields_list:
                res['name'] = False
            if 'quantity' in fields_list:
                res['quantity'] = 1
            if 'invoice_line_tax_id' in fields_list:
                res['invoice_line_tax_id'] = False
            if 'price_unit' in fields_list:
                res['price_unit'] = 0.0
        return res
    
#     def _get_uid(self, cr, uid, ids, name, args, context=None):
#         res={}
#         for line_id in ids:
#             res[line_id] = uid
#         return res
    
    _columns = {
        'advance_type' : fields.char("Advance Type"),
        'budget_remaining': fields.related('budget_line_id', 'remaining_amount', string="Budget Remaining", type="float", readonly=True),
#         'reserved_amount': fields.function(_res_amt, string='Remaining Reserved Amount', type='float', digits_compute=dp.get_precision('Account'), readonly=True),
        'state': fields.related('invoice_id', 'state', string="State", type="char"),
        'budget_line_id': fields.many2one('crossovered.budget.lines', 'Budget Lines', readonly=True, select=True, copy=False),
        'budget_remaining_show': fields.float(string='Remaining Budget', digits_compute=dp.get_precision('Account'), readonly=True, copy=False),
        'budget_remaining_show': fields.float(string='Remaining Budget', digits_compute=dp.get_precision('Account'), readonly=True, copy=False),
#         'active_uid': fields.function(_get_uid, string='Uid', type='integer'),
        'receipt_number': fields.char(string='Receipt Number')
    }
    
    @api.multi
    def price_unit_change(self, advance_type=False):
        values = {'advance_type': advance_type}
        return {'value': values}
    
    @api.multi
    def get_account(self, product_id=False):
        if not product_id :
            product_id = self.product_id
        else:
            product_id = self.env['product.product'].browse(product_id)
            
        if product_id.valuation == 'manual_periodic':
            account = product_id.property_account_expense or \
                        product_id.categ_id.property_account_expense_categ
        else:
            account = product_id.categ_id.property_stock_valuation_account_id
        if not account:
            raise osv.except_osv(_('Warning !'), _('Valuation or Expense Account for %s is Empty, \n Go to Product->Accounting->Internal Category') % (product_id.name))
        return account.id
    
    @api.multi
    def get_date(self, invoice_id=False):
        if invoice_id:
            date = self.invoice_id.browse(invoice_id).date_invoice or time.strftime(DEFAULT_SERVER_DATETIME_FORMAT)
            return date
    
    @api.multi
    def calculate_cc_budget(self, date, account_analytic_id):
        dom = [('state', '=', 'validate'), ('crossovered_budget_id.state', '=', 'validate')]
        dom.append(('date_to', '>=', date))
        dom.append(('date_from', '<=', date))
        dom.append(('analytic_account_id', '=', account_analytic_id))
        an_acc_ids = self.env['crossovered.budget.lines'].search(dom)
        amount = sum([line.remaining_amount for line in an_acc_ids])
        return amount
    
    @api.model
    @api.returns('self', lambda value:value.id)
    def create(self, vals):
        if vals.get('advance_type', False):
            advance_type = vals['advance_type']
            date = self.get_date(vals.get('invoice_id', False))
            account = self.get_account(vals.get('product_id', False))
            if advance_type == 'settlement':
                vals['budget_line_id'] = self.env['crossovered.budget.lines'].find_budget_line(vals['account_analytic_id'], account, date)
                vals['budget_remaining_show'] = self.env['crossovered.budget.lines'].browse(vals['budget_line_id']).remaining_amount
            elif advance_type == 'request':
                vals['budget_remaining_show'] = self.calculate_cc_budget(date, vals['account_analytic_id'])
            vals['invoice_line_tax_id'] = False
        return super(account_invoice_line, self).create(vals)
    
    @api.multi
    def write(self, vals):
        for s in self:
            if s.advance_type != 'none':
                if vals.get('product_id', False) or vals.get('account_analytic_id', False):
                    date = s.invoice_id.date_invoice or time.strftime(DEFAULT_SERVER_DATETIME_FORMAT)
                    account = s.get_account(vals.get('product_id', False))
                    analytic = vals.get('account_analytic_id', False) or s.account_analytic_id.id
                    if s.advance_type == 'settlement':
                        vals['budget_line_id'] = s.env['crossovered.budget.lines'].find_budget_line(vals['account_analytic_id'], account, date)
                        vals['budget_remaining_show'] = self.env['crossovered.budget.lines'].browse(vals['budget_line_id']).remaining_amount
                    elif s.advance_type == 'request':
                        vals['budget_remaining_show'] = s.calculate_cc_budget(date, vals['account_analytic_id'])
                vals['invoice_line_tax_id'] = False
        return super(account_invoice_line, self).write(vals)
        
class account_invoice(osv.osv):
    _inherit = 'account.invoice'
    
    def _amount_adv(self, cr, uid, ids, name, args, context=None):        
        res = {}
        for invoice in self.browse(cr, uid, ids, context=context):
            res[invoice.id] = {}
            res[invoice.id]['amount_adv'] = invoice.ref_advance_id.amount_total
            res[invoice.id]['amount_adv_bal'] = invoice.net_pay - res[invoice.id]['amount_adv']
        return res
    
    @api.multi
    @api.depends("partner_id")
    def _get_employee(self):
        for inv in self:
            emp = self.env['hr.employee'].search([('address_home_id', '=', inv.partner_id.id)], limit=1)
            inv.employee_id = emp
            
    _columns = {
        'amount_adv': fields.function(_amount_adv, digits_compute=dp.get_precision('Account'), store=True, string='Advance Amount', multi="advance"),
        'amount_adv_bal': fields.function(_amount_adv, digits_compute=dp.get_precision('Account'), string='Should be Paid', multi="advance"),
        'ref_advance_id': fields.many2one('account.invoice', 'Advance Reference', readonly=True, states={'draft':[('readonly', False)]}),
#         'employee_id': fields.many2one('hr.employee', 'Employee'),
        'advance_type': fields.selection([
            ('request', 'Advance Request'),
            ('settlement', 'Advance Settlement'),
            ('none', 'Supplier Invoice'),
            ], 'Advance Type'),
        'settled': fields.boolean('Settled', copy=False)
    }
    
    employee_id = Fields.Many2one(string="Employee", comodel_name="hr.employee",
        compute="_get_employee", store=True,)
    approved_by = Fields.Many2one('res.users', string='Approved by',
        readonly=True, states={'draft': [('readonly', False)]})
    checked_by = Fields.Many2one('res.users', string='Checked/Acknowledge by',
        readonly=True, states={'draft': [('readonly', False)]})
    verified_by = Fields.Many2one('res.users', string='Verified by',
        readonly=True, states={'draft': [('readonly', False)]})
    
    _defaults = {
        'advance_type': 'none',
    }
        
    @api.multi
    def onchange_partner_id(self, type, partner_id, date_invoice=False,
            payment_term=False, partner_bank_id=False, company_id=False):        
        res = super(account_invoice, self).onchange_partner_id(type, partner_id, date_invoice, payment_term, partner_bank_id, company_id)
        if not partner_id:
            res['value']['ref_advance_id'] = False
        return res
    
    @api.multi
    def onchange_company_id(self, company_id, part_id, type, invoice_line, currency_id):
        res = super(account_invoice, self).onchange_company_id(company_id, part_id, type, invoice_line, currency_id)
        if self._context.get('default_advance_type', False) == 'request':
            if res['value'].get('journal_id', False):
                company_id = self._context.get('company_id', self.env.user.company_id.id)
                company = self.env['res.company'].browse(company_id)
                if not company.advance_journal_id:
                    raise Warning(_('Please configure advance journal, \n Go to Setting->Configuration->Accounting'))
                res['value']['journal_id'] = company.advance_journal_id.id
            return res
        elif self._context.get('default_advance_type', False) == 'settlement':
            if res['value'].get('journal_id', False):
                company_id = self._context.get('company_id', self.env.user.company_id.id)
                company = self.env['res.company'].browse(company_id)
                if not company.settlement_journal_id:
                    raise Warning(_('Please configure settlement journal, \n Go to Setting->Configuration->Accounting'))
                res['value']['journal_id'] = company.settlement_journal_id.id
            return res
        else:
            return res
    
    @api.multi
    def onchange_advance_type(self, ttype): 
        res = {}
        res['value'] = {}       
        res['domain'] = {}
        if ttype != 'none' and not self.env.user.company_id.advance_journal_id:
                raise osv.except_osv(_('Warning!'),
                                      _('Please configure advance journal\n Goto Settings -> Configuration -> Accounting !'))
            
        if ttype == 'settlement':
#             res['value']['partner_id'] = self.env.user.partner_id.id
#             res['value']['account_id'] = self.env.user.partner_id.property_account_payable.id
            res['value']['date_invoice'] = time.strftime(DEFAULT_SERVER_DATETIME_FORMAT)
#             adv = self.search([('partner_id', '=', self.env.user.partner_id.id),
#                                ('advance_type', '=', 'request'),
#                                ('settled', '=', False),
#                                ('state', '=', 'paid')], limit=1)
#             res['value']['ref_advance_id'] = adv.id

#             res['domain']['ref_advance_id'] = [('journal_id', '=', self.env.user.company_id.advance_journal_id.id),
#                                                 ('partner_id', '=', self.partner_id.id),
#                                                 ('state', '=', 'paid'),
#                                                 ('settled', '=', False)]

# old
#             res['domain']['ref_advance_id'] = [('journal_id', '=', self.env.user.company_id.advance_journal_id.id), 
#                                                 ('partner_id', '=', self.env.user.partner_id.id), 
#                                                 ('account_id', '=', self.env.user.partner_id.property_advance_account.id), 
#                                                 ('reconcile_id', '=', False),
#                                                 ('debit', '!=', 0)]

        elif ttype == 'request':
            if not self.env.user.company_id.advance_product_id:
                raise osv.except_osv(_('Warning!'),
                                     _('Please configure advance product\n Goto Settings -> Configuration -> Accounting !'))
#             res['value']['partner_id'] = self.env.user.partner_id.id
#             res['value']['journal_id'] = self.env.user.company_id.advance_journal_id.id
#             res['value']['account_id'] = self.env.user.partner_id.property_account_payable.id
            res['value']['date_invoice'] = time.strftime(DEFAULT_SERVER_DATETIME_FORMAT)
            res['value']['invoice_line'] = [
                (0, 0, {
                    'product_id': self.env.user.company_id.advance_product_id.id,
                    'name': self.env.user.company_id.advance_product_id.name,
                    'account_id': self.env.user.company_id.advance_product_id.property_account_expense.id,
                    'quantity': 1,
                    'price_unit': 1000000,
                    'advance_type': 'request',
                })
            ]
        return res
    
    @api.multi
    def action_cancel(self):
        for inv in self:
            if inv.ref_advance_id:
                inv.ref_advance_id.settled = False
        return super(account_invoice, self).action_cancel()
        
    def invoice_validate(self, cr, uid, ids, context=None):
        for invoice in self.browse(cr, uid, ids, context):
            if invoice.advance_type == 'request':
                # check advance journal 
                if invoice.journal_id.id != invoice.company_id.advance_journal_id.id:
                    raise osv.except_osv(_('Warning!'),
                                         _("Please choose Advance Journal!"))
                # check if partner has no outstanding advance
                outstanding = self.search(cr, uid, [('advance_type', '=', 'request'), ('partner_id', '=', invoice.partner_id.id), ('state', 'in', ('open', 'paid')), ('settled', '=', False)])
                if outstanding:
                    raise osv.except_osv(_('Warning!'),
                                         _("%s has outstanding advance") % (invoice.partner_id.name))
                for line in invoice.invoice_line:
                    # check analytic account
                    if not line.account_analytic_id:
                        raise osv.except_osv(_('Warning!'),
                                             _("Please fill the Analytic Account!"))
                    # check advance product
                    if line.product_id.id != invoice.company_id.advance_product_id.id:
                        raise osv.except_osv(_('Warning!'),
                                             _("Please choose advance on product!"))
                    # check budget
                    if line.price_subtotal > line.budget_remaining_show:
                        raise osv.except_osv(_('Warning!'),
                                             _("Insufficient available budget."))
            elif invoice.advance_type == 'settlement':
                # check request ref if already settled
                if invoice.ref_advance_id:
                    if invoice.ref_advance_id.settled:
                        raise osv.except_osv(_('Warning!'),
                                             _("The Advance Reference already settled."))
                # set settled
                if invoice.ref_advance_id:
                    invoice.ref_advance_id.settled = True
                for line in invoice.invoice_line:
                    # check analytic account
                    if not line.account_analytic_id:
                        raise osv.except_osv(_('Warning!'),
                                             _("Please fill the Analytic Account!"))
        return super(account_invoice, self).invoice_validate(cr, uid, ids, context)
    
    @api.multi
    def test_paid(self):
        res = super(account_invoice, self).test_paid()
        for inv in self:
            if inv.advance_type == 'settlement':
                if inv.amount_total == inv.ref_advance_id.amount_total:
                    res = True
        return res
    
    @api.multi
    def _move_create(self):
        for inv in self:
            """ Creates invoice related analytics and financial move lines """
            account_invoice_tax = self.env['account.invoice.tax']
            account_move = self.env['account.move']
    
            if not inv.journal_id.sequence_id:
                raise except_orm(_('Warning!'), _('Please define sequence on the journal related to this invoice.'))
            if not inv.invoice_line:
                raise except_orm(_('No Invoice Lines!'), _('Please create some invoice lines.'))
            if inv.move_id:
                continue

            ctx = dict(self._context, lang=inv.partner_id.lang)

            company_currency = inv.company_id.currency_id
            if not inv.date_invoice:
                # FORWARD-PORT UP TO SAAS-6
                if inv.currency_id != company_currency and inv.tax_line:
                    raise except_orm(
                        _('Warning!'),
                        _('No invoice date!'
                            '\nThe invoice currency is not the same than the company currency.'
                            ' An invoice date is required to determine the exchange rate to apply. Do not forget to update the taxes!'
                        )
                    )
                inv.with_context(ctx).write({'date_invoice': time.strftime(DEFAULT_SERVER_DATETIME_FORMAT)})
            date_invoice = inv.date_invoice

            # create the analytical lines, one move line per invoice line
            iml = inv._get_analytic_lines()
            # check if taxes are all computed
            compute_taxes = account_invoice_tax.compute(inv.with_context(lang=inv.partner_id.lang))
            inv.check_tax_lines(compute_taxes)

            # I disabled the check_total feature
            if self.env.user.has_group('account.group_supplier_inv_check_total'):
                if inv.type in ('in_invoice', 'in_refund') and abs(inv.check_total - inv.amount_total) >= (inv.currency_id.rounding / 2.0):
                    raise except_orm(_('Bad Total!'), _('Please verify the price of the invoice!\nThe encoded total does not match the computed total.'))

            if inv.payment_term:
                total_fixed = total_percent = 0
                for line in inv.payment_term.line_ids:
                    if line.value == 'fixed':
                        total_fixed += line.value_amount
                    if line.value == 'procent':
                        total_percent += line.value_amount
                total_fixed = (total_fixed * 100) / (inv.amount_total or 1.0)
                if (total_fixed + total_percent) > 100:
                    raise except_orm(_('Warning!'), _("Cannot create the invoice.\nThe related payment term is probably misconfigured as it gives a computed amount greater than the total invoiced amount. In order to avoid rounding issues, the latest line of your payment term must be of type 'balance'."))

            # Force recomputation of tax_amount, since the rate potentially changed between creation
            # and validation of the invoice
            inv._recompute_tax_amount()
            # one move line per tax line
            iml += account_invoice_tax.move_line_get(inv.id)

            if inv.type in ('in_invoice', 'in_refund'):
                ref = inv.reference
            else:
                ref = inv.number

            diff_currency = inv.currency_id != company_currency
            # create one move line for the total and possibly adjust the other lines amount
            total, total_currency, iml = inv.with_context(ctx).compute_invoice_totals(company_currency, ref, iml)

            name = inv.supplier_invoice_number or inv.name or '/'
            totlines = []
            
            # advance 
            settlement_diff = total + inv.ref_advance_id.amount_total
            
            if settlement_diff:
                if inv.payment_term:
                    totlines = inv.with_context(ctx).payment_term.compute(total, date_invoice)[0]
                if totlines:
                    res_amount_currency = total_currency
                    ctx['date'] = date_invoice
                    for i, t in enumerate(totlines):
                        if inv.currency_id != company_currency:
                            amount_currency = company_currency.with_context(ctx).compute(t[1], inv.currency_id)
                        else:
                            amount_currency = False
    
                        # last line: add the diff
                        res_amount_currency -= amount_currency or 0
                        if i + 1 == len(totlines):
                            amount_currency += res_amount_currency
    
                        iml.append({
                            'type': 'dest',
                            'name': name,
                            'price': settlement_diff,
                            'account_id': inv.account_id.id,
                            'date_maturity': t[0],
                            'amount_currency': diff_currency and amount_currency,
                            'currency_id': diff_currency and inv.currency_id.id,
                            'ref': ref,
                        })
                else:
                    iml.append({
                        'type': 'dest',
                        'name': name,
                        'price': settlement_diff,
                        'account_id': inv.account_id.id,
                        'date_maturity': inv.date_due,
                        'amount_currency': diff_currency and total_currency,
                        'currency_id': diff_currency and inv.currency_id.id,
                        'ref': ref
                    })
            
            # advance line
            iml.append({
                'type': 'dest',
                'name': 'Advance ' + name,
                'price':-inv.ref_advance_id.amount_total,
                'account_id': inv.company_id.advance_product_id.property_account_expense and inv.company_id.advance_product_id.property_account_expense.id,
                'date_maturity': inv.date_due,
                'amount_currency': diff_currency and total_currency,
                'currency_id': diff_currency and inv.currency_id.id,
                'ref': ref
            })
            
            date = date_invoice

            part = self.env['res.partner']._find_accounting_partner(inv.partner_id)

            line = [(0, 0, self.line_get_convert(l, part.id, date)) for l in iml]
            line = inv.group_lines(iml, line)

            journal = inv.journal_id.with_context(ctx)
            if journal.centralisation:
                raise except_orm(_('User Error!'),
                        _('You cannot create an invoice on a centralized journal. Uncheck the centralized counterpart box in the related journal from the configuration menu.'))

            line = inv.finalize_invoice_move_lines(line)

            move_vals = {
                'ref': inv.reference or inv.name,
                'line_id': line,
                'journal_id': journal.id,
                'date': inv.date_invoice,
                'narration': inv.comment,
                'company_id': inv.company_id.id,
            }
            ctx['company_id'] = inv.company_id.id
            period = inv.period_id
            if not period:
                period = period.with_context(ctx).find(date_invoice)[:1]
            if period:
                move_vals['period_id'] = period.id
                for i in line:
                    i[2]['period_id'] = period.id

            ctx['invoice'] = inv
            ctx_nolang = ctx.copy()
            ctx_nolang.pop('lang', None)
            move = account_move.with_context(ctx_nolang).create(move_vals)

            # make the invoice point to that move
            vals = {
                'move_id': move.id,
                'period_id': period.id,
                'move_name': move.name,
            }
            inv.with_context(ctx).write(vals)
            # Pass invoice in context in method post: used if you want to get the same
            # account move reference when creating the same invoice after a cancelled one:
            move.post()
            self._log_event()
            return True
    
    @api.multi
    def action_move_create(self):
        for inv in self:
            if inv.ref_advance_id:
                self._move_create()
            else:
                res = super(account_invoice, self).action_move_create()
                return res
        
    
class account_move_line(osv.osv):
    _inherit = 'account.move.line'
        
    def name_get(self, cr, uid, ids, context=None):
        context = context or {}
        if context.get('type', False) == 'in_invoice' or context.get('remain', False):
            result = []
            for line in self.browse(cr, uid, ids, context=context):
                if line.reconcile_partial_id:
                    total = reduce(lambda y, t: (t.debit or 0.0) - (t.credit or 0.0) + y, line.reconcile_partial_id.line_partial_ids, 0.0)
                elif line.reconcile_id:
                    total = 0.0
                else:
                    total = line.debit - line.credit
                name = '%.2f' % (total)
                result.append((line.id, (line.move_id.name or '') + ' ' + line.name + ' (' + name + ')'))
            return result
        else :
            return super(account_move_line, self).name_get(cr, uid, ids, context)
    
