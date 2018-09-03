# -*- coding: utf-8 -*-
# © 2017 Ibrohim Binladin | ibradiiin@gmail.com | +62-838-7190-9782 | http://ibrohimbinladin.wordpress.com
##########################################################################################################
import amount_to_text_en
from openerp import models, fields, api, _

class account_invoice(models.Model):
    _inherit = "account.invoice"

    amount_to_text = fields.Text('Says [Amount to Text]')
    partner_contact_id = fields.Many2one('res.partner', string='Attn/Contact', change_default=True,
        readonly=True, states={'draft': [('readonly', False)]})
    bak_no = fields.Char(string='BAK No', readonly=True, states={'draft': [('readonly', False)]})
    bak_date = fields.Date(string='BAK Date', readonly=True,
        states={'draft': [('readonly', False)]}, index=True, copy=False)
    approved_by = fields.Many2one('res.users', string='Approvved by', readonly=True, states={'draft': [('readonly', False)]})


    @api.multi
    def button_calculate(self):
        self.button_reset_taxes()
        for inv in self:
            currency = inv.currency_id.name
            text_amount = amount_to_text_en.amount_to_text(inv.amount_total, 'id', currency)
            self.write({'amount_to_text': 'Say, '+text_amount})
        return True


