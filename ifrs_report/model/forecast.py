# -*- coding: utf-8 -*-

from openerp import models, fields, api
from openerp.tools.translate import _


class AccountForecast(models.Model):
    _name = 'account.forecast'
    _description = 'Cash Forecast'

#     @api.multi
#     def _default_fiscalyear(self):
#         af_obj = self.env['account.fiscalyear']
#         return af_obj.find(exception=False)
# 
#     @api.onchange('company_id')
#     def onchange_company_id(self):
#         af_obj = self.env['account.fiscalyear']
#         self.fiscalyear_id = af_obj.find(exception=False)
#         self.currency_id = self.company_id.currency_id.id

    name = fields.Char(string='Name', required=True, help='Report name')
    company_id = fields.Many2one(
        'res.company', string='Company', change_default=False,
        required=False, readonly=True, states={},
        default=lambda self: self.env['res.company']._company_default_get(
            'account.forecast'), help='Company name')
    line_ids = fields.One2many('account.forecast.line', 'forecast_id', string='Forecast Lines', copy=True)


class AccountForecastLine(models.Model):
    _name = 'account.forecast.line'
    
    forecast_id = fields.Many2one('account.forecast', string='Forecast')
    account_id = fields.Many2one('account.account', string='Account', required=True)
    date_maturity = fields.Date(string='Date', required=True)
    amount = fields.Float(string='Amount')