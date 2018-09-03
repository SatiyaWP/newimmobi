# -*- coding: utf-8 -*-
# © 2017 Ibrohim Binladin | ibradiiin@gmail.com | +62-838-7190-9782 | http://ibrohimbinladin.wordpress.com
##########################################################################################################
#from openerp.osv import osv
from openerp import models, fields, api
import openerp.addons.decimal_precision as dp

class l10n_id_ptkp(models.Model):
    _inherit = "l10n_id.ptkp"

    @api.one
    @api.depends('line_ids.ptkp_rate',)
    def _compute_amount(self):
        self.amount_total = sum(line.ptkp_rate for line in self.line_ids)


    amount_total = fields.Float(string='Total Tarif PTKP', digits=dp.get_precision('Account'),
            store=True, readonly=True, compute='_compute_amount')
    payroll_id = fields.Many2one('hr.payslip', string='Payroll',
            domain=[('state','!=','cancel')], copy=False)
    contract_id = fields.Many2one('hr.contract', string='Contract', copy=False)







