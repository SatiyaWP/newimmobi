# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright {2014} {Fadhlullah} <{fadhlullah@visi.co.id}>
#    All Rights Reserved
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import fields, osv, orm
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp


class res_company(orm.Model):
    _inherit = 'res.company'
    _columns = {
        'withholding_journal_id': fields.many2one('account.journal', 'Withholding journal',
            help="Journal used for registration of witholding amounts to be paid"),
        }
    
class account_config_settings(orm.TransientModel):
    _inherit = 'account.config.settings'
    _columns = {
        'withholding_journal_id': fields.related(
            'company_id', 'withholding_journal_id',
            type='many2one',
            relation="account.journal",
            string="Withholding journal",
            help='Journal used for registration of witholding amounts to be paid'),
    }
    
    def onchange_company_id(self, cr, uid, ids, company_id, context=None):
        res = super(account_config_settings, self).onchange_company_id(cr, uid, ids, company_id, context=context)
        if company_id:
            company = self.pool.get('res.company').browse(cr, uid, company_id, context=context)
            res['value'].update({
                'withholding_journal_id': (company.withholding_journal_id
                    and company.withholding_journal_id.id or False),
                })
        else: 
            res['value'].update({
                'withholding_journal_id': False,
                })
        return res


class account_invoice_wht(osv.osv):
    
    _inherit = 'account.invoice'
    
    def _amount_wht(self, cr, uid, ids, name, args, context=None):        
        res = {}
        for invoice in self.browse(cr, uid, ids, context=context):
            res[invoice.id] = 0
            for line in invoice.invoice_line:
                if line.amount_wht_line:
                    res[invoice.id] += line.amount_wht_line
        return res
        
    def _net_pay(self, cr, uid, ids, name, args, context=None):        
        res = {}
        for invoice in self.browse(cr, uid, ids, context):
            res[invoice.id] = invoice.amount_total - invoice.amount_wht
        return res
    
    def reconcile_withholding_move_payable(self, cr, uid, invoice, wh_move, context=None):
        line_pool = self.pool.get('account.move.line')
        rec_ids = []
        for inv_move_line in invoice.move_id.line_id:
            if inv_move_line.account_id.type == 'payable' and not inv_move_line.reconcile_id:
                rec_ids.append(inv_move_line.id)
        for wh_line in wh_move.line_id:
            for inv_line in invoice.invoice_line:
                if wh_line.account_id.type == 'payable' and inv_line.wht_id.account_id and inv_line.wht_id.account_id.id != wh_line.account_id.id and not wh_line.reconcile_id:
                    rec_ids.append(wh_line.id)
        return line_pool.reconcile_partial(cr, uid, rec_ids, type='auto', context=context)
    
    def copy(self, cr, uid, id, default=None, context=None):
        res = super(account_invoice_wht, self).copy(cr, uid, id, default, context)
        self.write(cr, uid, [res], {'wht_move_id' : False})
        return res
    
    def button_wht(self, cr, uid, ids, context=None):

        if context is None:
            context = {}
        """Open the change discount wizard"""
        context.update({
            'active_model': self._name,
            'active_ids': ids,
            'active_id': len(ids) and ids[0] or False
        })
        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'account.wht.wizard',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': context,
            'nodestroy': True,
            'auto_refresh':True,
        }
        
    def withholding_move_create(self, cr, uid, ids, num, context=None):
        account_move_obj = self.pool.get('account.move')
        curr_obj = self.pool.get('res.currency')
        for invoice in self.browse(cr, uid, ids, context=None):
            total_line_amount = curr_obj.round(cr, uid, invoice.company_id.currency_id, invoice.amount_wht)
            if invoice.company_id.withholding_journal_id.id == False :
                raise osv.except_osv(_('Warning!'), _('Input Withholding Journal \n Goto Settings -> Configuration -> Accounting !'))
            new_move = {
                        'journal_id': invoice.company_id.withholding_journal_id.id,
                        'number' : self.pool.get('ir.sequence').get(cr, uid, invoice.company_id.withholding_journal_id.sequence_id.id),
                        'period_id': invoice.period_id.id,
                        'date': invoice.date_invoice,
                        'ref' : _(invoice.number),
                        'line_id': []
                        }
            if invoice.type in ['out_refund', 'in_invoice'] :
                new_line = {
                            'name': invoice.number,
                            'account_id': invoice.account_id.id,
                            'partner_id': invoice.partner_id.id,
                            'debit': total_line_amount,
                            'credit': 0.0,
                }
            else :
                new_line = {
                            'name': invoice.number,
                            'account_id': invoice.account_id.id,
                            'partner_id': invoice.partner_id.id,
                            'debit': 0.0,
                            'credit': total_line_amount,
                }
            new_move['line_id'].append((0, 0, new_line))
                
            for line in invoice.invoice_line:
                if line.wht_id:
                        line_amount = curr_obj.round(cr, uid, invoice.company_id.currency_id, line.amount_wht_line)
                        
                        if invoice.type in ['out_refund', 'in_invoice'] :
                            new_line = {
                                'name': _(num) + _(' - ') + line.name,
                                'account_id': line.wht_id.account_id.id,
                                'debit': 0.0,
                                'credit': line_amount,
                            }
                        else : 
                            new_line = {
                                'name': _(num) + _(' - ') + line.name,
                                'account_id': line.wht_id.account_id.id,
                                'debit': line_amount,
                                'credit': 0.0,
                            }
                        new_move['line_id'].append((0, 0, new_line))
                        
            move_id = self.pool.get('account.move').create(cr, uid, new_move, context=context)
            invoice.write({'wht_move_id' : move_id})
            if invoice.type in ['in_refund', 'in_invoice'] :
                self.reconcile_withholding_move_payable(cr, uid, invoice, account_move_obj.browse(cr, uid, move_id, context), context)
        return True
        
    _columns = {
        'amount_wht' : fields.function(_amount_wht, digits_compute=dp.get_precision('Account'), store=True, string='Withholding Taxes'),
        'net_pay' : fields.function(_net_pay, digits_compute=dp.get_precision('Account'), string='Net Pay'),
        'wht_move_id':fields.many2one('account.move', 'Withholding_Tax Journal', required=False),
        }
    
    _defaults = {
        'amount_wht' : 0,
        }
        
class account_invoice_line_wht(osv.osv):
     
    _inherit = 'account.invoice.line'

    def _amount_wht_line(self, cr, uid, ids, name, args, context=None):
        cur_obj = self.pool.get('res.currency')
        res = {}
        for line in self.browse(cr, uid, ids, context=context):
            res[line.id] = line.price_subtotal * ((line.wht_id.percentage or 0.0) / 100.0)
            if line.invoice_id:
                cur = line.invoice_id.currency_id
                res[line.id] = cur_obj.round(cr, uid, cur, res[line.id])
        return res

    _columns = {
        'wht_id' : fields.many2one('account.withholding.tax', 'WH Taxes'),
        'amount_wht_line' : fields.function(_amount_wht_line, type='float', digits_compute=dp.get_precision('Account'), string='Withholding Taxes'),
        }

class account_withholding_tax(orm.Model):
    _name = "account.withholding.tax"
    _description = "Account Withholding Tax"

    _columns = {
        'name': fields.char('Name', size=128, required=True),
        'code': fields.char('Code', size=64, required=True),
        'percentage': fields.float('Percentage', digits_compute=dp.get_precision('Account')),
        'partner_id' : fields.many2one('res.partner', 'Tax Authorities', help="""Kantor Pajak"""),
        'type': fields.selection([('sale', 'Sales'), ('purchase', 'Purchases')], 'Tax Application', required=True),
        'account_id': fields.many2one('account.account', 'Withholding Tax Account', required=True),
    }
    
    defaults = {
        'type' : 'purchase',
        }
    
    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'Unfortunately this name is already used, please choose a unique one'),
        ('code_unique', 'UNIQUE(code)', 'Unfortunately this code is already used, please choose a unique one')
    ]
            
    # Check amount 
    def onchange_amount(self, cr, uid, ids, amount, context=None):
        # percentage over 100%
        if amount > 100:
            raise osv.except_osv(_('Warning!'), _('The Percentage are invalid.\nNegative numbers and percentage\nover 100 are not allowed.'))
            return False
        # negative number
        if amount < 0:
            raise osv.except_osv(_('Warning!'), _('The Percentage are invalid.\nNegative numbers and percentage\nover 100 are not allowed.'))
            return False        
        return True
    
class purchase_line_wht(osv.osv):
    
    _inherit = 'purchase.order.line'
    
    def _amount_wht_line(self, cr, uid, ids, name, args, context=None):
        cur_obj = self.pool.get('res.currency')
        res = {}
        for line in self.browse(cr, uid, ids, context=context):
            res[line.id] = line.price_subtotal * ((line.wht_id.percentage or 0.0) / 100.0)
            if line.order_id:
                cur = line.order_id.pricelist_id.currency_id
                res[line.id] = cur_obj.round(cr, uid, cur, res[line.id])
        return res
    
    _columns = {
        'wht_id' : fields.many2one('account.withholding.tax', 'WH Taxes'),
        'amount_wht_line' : fields.function(_amount_wht_line, type='float', digits_compute=dp.get_precision('Account'), string='Withholding Taxes'),
        }
    
class purchase_wht(osv.osv):
    _inherit = 'purchase.order'
        
    def _amount_wht(self, cr, uid, ids, name, args, context=None):        
        res = {}
        for order in self.browse(cr, uid, ids, context=context):
            res[order.id] = 0
            for line in order.order_line:
                if line.amount_wht_line:
                    res[order.id] += line.amount_wht_line
        return res
        
    def _net_pay(self, cr, uid, ids, name, args, context=None):
        res = {}
        for order in self.browse(cr, uid, ids, context):
            res[order.id] = order.amount_total - order.amount_wht
        return res
    
    def _prepare_inv_line(self, cr, uid, account_id, order_line, context=None):
        res = super(purchase_wht, self)._prepare_inv_line(cr, uid, account_id, order_line, context)
        res['wht_id'] = order_line.wht_id.id
        return res
    
    _columns = {
        'amount_wht' : fields.function(_amount_wht, digits_compute=dp.get_precision('Account'), store=True, string='Withholding Taxes'),
        'net_pay' : fields.function(_net_pay, digits_compute=dp.get_precision('Account'), string='Net Pay'),
        }
    
