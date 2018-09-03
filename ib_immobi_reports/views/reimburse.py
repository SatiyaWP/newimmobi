import datetime
from dateutil.relativedelta import relativedelta

from openerp import api, fields, models, _
from openerp.exceptions import except_orm, Warning, RedirectWarning
from openerp.tools import float_is_zero, float_compare

import openerp.addons.decimal_precision as dp

class res_company(models.Model):
    _inherit = 'res.company'
    rmb_journal_id = fields.Many2one('account.journal', string='Reimbursement journal',
        help="Journal used for reimbursement")

class account_config_settings(models.Model):
    _inherit = 'account.config.settings'
    rmb_journal_id = fields.Many2one(
        'account.journal',
        related='company_id.rmb_journal_id',
        string="Reimbursement journal",
        help='Journal used for reimbursement')

class account_invoice_reimburse(models.Model):
    _inherit = 'account.invoice'
    
    reimburse = fields.Boolean(string='Reimburse')
    paid_by = fields.Selection([
        ('cash','Cash'),('cheque','Cheque'),
        ('transfer','Transfer')], string='Paid By', index=True,
        default='cash', copy=False)
    
    @api.multi
    def onchange_company_id(self, company_id, part_id, type, invoice_line, currency_id):
        res = super(account_invoice_reimburse, self).onchange_company_id(company_id, part_id, type, invoice_line, currency_id)
        if self._context.get('default_reimburse', False):
            if res['value'].get('journal_id', False):
                company_id = self._context.get('company_id', self.env.user.company_id.id)
                company = self.env['res.company'].browse(company_id)
                if not company.rmb_journal_id:
                    raise Warning(_('Please configure reimburse journal, \n Go to Setting->Configuration->Accounting'))
                res['value']['journal_id'] = company.rmb_journal_id.id
            return res
        else:
            return res
    
    @api.model
    @api.returns('self', lambda value:value.id)
    def create(self, vals):
        if vals.get('reimburse', False):
            if vals.get('date_invoice', False):
                date_str = vals['date_invoice']
                date = datetime.datetime.strptime(date_str, "%Y-%m-%d")
                date_due = date + datetime.timedelta(days=30)
                date_due_str = date_due.strftime("%Y-%m-%d")
                vals['date_due'] = date_due_str
        return super(account_invoice_reimburse, self).create(vals)
    
    @api.multi
    def write(self, vals):
        for inv in self:
            if inv.reimburse:
                if vals.get('date_invoice', False):
                    date_str = vals['date_invoice']
                    date = datetime.datetime.strptime(date_str, "%Y-%m-%d")
                    date_due = date + datetime.timedelta(days=30)
                    date_due_str = date_due.strftime("%Y-%m-%d")
                    vals['date_due'] = date_due_str
        return super(account_invoice_reimburse, self).write(vals)
    
    @api.multi
    def invoice_validate(self):
        for inv in self:
            if inv.reimburse:
                if not self.env.user.company_id.medical_account_id:
                    raise Warning(_('Please configure medical account\n Goto Settings -> Configuration -> Human Resource !'))
                for line in inv.invoice_line:
                    # check analytic account
                    if not line.account_analytic_id:
                        raise Warning(_('Please fill the Analytic Account!'))
                    if line.account_id == self.env.user.company_id.medical_account_id:
                        # check medical budget
                        # calculate this year expenses
                        inv_year = datetime.datetime.strptime(inv.date_invoice, "%Y-%m-%d").year
                        min_date = str(inv_year) + '-01-01'
                        max_date = str(inv_year) + '-12-31'
                        aml_medical = self.env['account.move.line'].search([
                            ('date', '>=', min_date),
                            ('date', '<=', max_date),
                            ('account_id', '=', self.env.user.company_id.medical_account_id.id),
                            ('partner_id', '=', inv.partner_id.id)])
                        usage_debit = sum([aml.debit for aml in aml_medical])
                        usage_credit = sum([aml.credit for aml in aml_medical])
                        usage = usage_debit - usage_credit
                        
                        # find salary
                        emp = self.env['hr.employee'].search([('address_home_id', '=', inv.partner_id.id)], limit=1)
                        contracts = self.env['hr.contract'].search([('employee_id', '=', emp.id),
                                                                    ('date_start', '<=', inv.date_invoice),
                                                                    '|', ('date_end', '>=', inv.date_invoice), ('date_end', '=', False)])
    
                        if not contracts:
                            raise Warning(_('This employee has no active contract'))
                        if len(contracts) > 1:
                            active_contract_date = max([contract.date_start for contract in contracts])
                            active_contract = self.env['hr.contract'].search([('employee_id', '=', emp.id),
                                                                              ('date_start', '=', active_contract_date)], limit=1)
                        else:
                            active_contract = contracts
                        if usage > active_contract.wage:
                            raise Warning(_('Insufficient medical budget'))
                    else:
                        # find contract
                        if line.price_subtotal > line.budget_remaining + line.price_subtotal:
                            raise Warning(_('Insufficient available budget for analytic %s' % (line.account_analytic_id.name)))
        return super(account_invoice_reimburse, self).invoice_validate()


class account_invoice_line_reimburse(models.Model):
    _inherit = 'account.invoice.line'
    
    reimburse = fields.Boolean(string='Reimburse')
    receipt_number = fields.Char(string='Receipt Number')
    receipt_date = fields.Date(string='Date', index=True, copy=False)
    
    @api.multi
    def price_unit_change_reimburse(self, advance_type=False, reimburse=False):
        values = {
            'advance_type': advance_type,
            'reimburse': reimburse,
        }
        return {'value': values}

class res_company(models.Model):
    _inherit = 'res.company'
    
    medical_account_id = fields.Many2one('account.account', string='Medical Account', help="Default account for medical expense")
    
class account_config_settings(models.TransientModel):
    _inherit = 'account.config.settings'
    
    
    medical_account_id = fields.Many2one('account.account', related='company_id.medical_account_id', string="Medical account"
                                         , help='Default account for medical expense')
    
    def onchange_company_id(self, cr, uid, ids, company_id, context=None):
        res = super(account_config_settings, self).onchange_company_id(cr, uid, ids, company_id, context=context)
        if company_id:
            company = self.pool.get('res.company').browse(cr, uid, company_id, context=context)
            res['value'].update({
                'rmb_journal_id': (company.rmb_journal_id
                    and company.rmb_journal_id.id or False),
                'medical_account_id': (company.medical_account_id
                    and company.medical_account_id.id or False),
                })
        else: 
            res['value'].update({
                'rmb_journal_id': False,
                'medical_account_id': False,
            })
        return res
    
