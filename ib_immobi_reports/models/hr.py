# -*- coding: utf-8 -*-
# © 2017 Ibrohim Binladin | ibradiiin@gmail.com | +62-838-7190-9782 | http://ibrohimbinladin.wordpress.com
##########################################################################################################
from datetime import datetime, timedelta
from dateutil import relativedelta
# from openerp.osv import fields, osv
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
from openerp import api, models, fields, _
# from openerp import fields as Fields

class hr_contract_template_report(models.Model):
    _name = "hr.contract.template.report"

    name = fields.Char('Template Name', required=True, select=True)
    contract_body = fields.Text('Job Description', required=True)
    contract_title = fields.Text(string='Title')
    contract_header = fields.Text('Header')
    contract_footer = fields.Text('Footer')



class hr_contract(models.Model):
    _inherit = "hr.contract"

    @api.multi
    @api.depends('trial_date_start', 'trial_date_end', 'date_start', 'date_end')
    def _get_timeframe(self):
        hasil1 = False; hasil2 = False;
        for hrc in self:
            contract_duration = _('')
            trial_duration = _('')
            total_duration = _('')
            if hrc.trial_date_start and hrc.trial_date_end:
                p = datetime.strptime(str(hrc.trial_date_start), '%Y-%m-%d')
                t = datetime.strptime(str(hrc.trial_date_end), '%Y-%m-%d')
                q = t + timedelta(days=1)

                hasil1 = relativedelta.relativedelta(q, p)
                if hasil1.years > 0:
                    trial_duration += str(hasil1.years) + " Tahun "
                if hasil1.months > 0:
                    trial_duration += str(hasil1.months) + " Bulan "
                if hasil1.days > 0:
                    trial_duration += str(hasil1.days) + " Hari "
                hrc.trial_duration = trial_duration
            if hrc.date_start and hrc.date_end:
                x = datetime.strptime(str(hrc.date_start), '%Y-%m-%d')
                s = datetime.strptime(str(hrc.date_end), '%Y-%m-%d')
                y = s + timedelta(days=1)

                hasil2 = relativedelta.relativedelta(y, x)
                if hasil2.years > 0:
                    contract_duration += str(hasil2.years) + " Tahun "
                if hasil2.months > 0:
                    contract_duration += str(hasil2.months) + " Bulan "
                if hasil2.days > 0:
                    contract_duration += str(hasil2.days) + " Hari "
                hrc.contract_duration = contract_duration
            if hasil1 and hasil2:
                total = hasil1 + hasil2
                if total.years > 0:
                    total_duration += str(total.years) + " Tahun "
                if total.months > 0:
                    total_duration += str(total.months) + " Bulan "
                if total.days > 0:
                    total_duration += str(total.days) + " Hari "
                hrc.total_duration = total_duration

    contract_date = fields.Date(string="Contract Date")
    
    contract_duration = fields.Char(
        string="Contract Duration",
        compute="_get_timeframe",
        store=True,
    )
    trial_duration = fields.Char(
        string="Trial Duration",
        compute="_get_timeframe",
        store=True,
    )
    total_duration = fields.Char(
        string="Total Duration",
        compute="_get_timeframe",
        store=True,
    )
#     _columns = {
#         'contract_date': fields.date("Contract Date"),
        # 'contract_duration': fields.function(_get_timeframe, type="char", string='Contract Duration'),
#         'contract_duration': fields.function(_get_timeframe, type="char", string='Contract Duration', multi="advance"),
#         'trial_duration': fields.function(_get_timeframe, type="char", string='Trial Duration', multi="advance"),
#         'total_duration': fields.function(_get_timeframe, type="char", string='Total Duration', multi="advance"),
#     }




class hr_payslip(models.Model): #Testing_Edit
    _inherit = "hr.payslip"

    @api.one
    @api.depends('line_ids.total', 'line_ids.code', 'company_id.currency_id')
    def _compute_salary_total(self):
        res = sum(line.total for line in self.line_ids if line.code<>'GROSS') or 0.0
        self.salary_subtotal = self.company_id.currency_id.round(res)

    @api.one
    @api.depends('line_ids.total', 'line_ids.name',
                 'line_ids.category_id.name', 'company_id.currency_id')
    def _get_salary_details(self):
        self.detail_fee = _("")
        for line in self.line_ids:
            self.detail_fee += _(line.name)
            if line.category_id:
                self.detail_fee += " [" + _(line.category_id.name) + "] "
            if line.total and line.total > 0:
                self.detail_fee += _(self.company_id.currency_id.name) + " " + str(line.total)
            if len(self.line_ids) > 1:
                self.detail_fee += _("\n")

    detail_fee = fields.Text(string='Salary Details', compute='_get_salary_details')
    salary_subtotal = fields.Float(string='Total Salary', digits=dp.get_precision('Account'),
            compute='_compute_salary_total')
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id',
                                     string='Currency', store=True, readonly=True)

    def print_payslip(self, cr, uid, ids, context=None):
        assert len(ids) == 1, 'This option should only be used for a single id at a time.'
        context = context or {}
        slip_number = ''
        employee_id = 0; period_id = 0; struct_id = 0; contract_id = 0
        for slip in self.browse(cr, uid, ids, context=context):
            slip_number = slip.number
            period_id = slip.tax_period_id and slip.tax_period_id.id
            employee_id = slip.employee_id and slip.employee_id.id
            struct_id = slip.struct_id and slip.struct_id.id
            contract_id = slip.contract_id and slip.contract_id.id

        datas = {
            'ids': ids,
            'model': 'hr.payslip',
            'form': self.read(cr, uid, ids[0], context=context),
            'employee_id': int(employee_id),
            'period_id': int(period_id),
            'slip_no': slip_number,
            'struct_id': int(struct_id),
            'contract_id': int(contract_id),
        }
        return {
            'type': 'ir.actions.report.xml',
            'report_name': "hr.payslip.pdf",
            'datas': datas,
            'nodestroy': True
        }


