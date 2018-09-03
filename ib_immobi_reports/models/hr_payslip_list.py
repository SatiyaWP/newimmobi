# -*- coding: utf-8 -*-
# © 2017 Ibrohim Binladin | ibradiiin@gmail.com | +62-838-7190-9782 | http://ibrohimbinladin.wordpress.com
##########################################################################################################
from openerp.osv import fields, osv
from openerp import tools


class hr_payslip_custom_view(osv.osv):
    _name = "payslip.custom.list"
    _auto = False
    _rec_name = 'number'
    _columns = {
        'number': fields.char('Payslip Ref#', readonly=True), #payslip
        'employee_id': fields.many2one('hr.employee', 'Employee', readonly=True),
        'date_from': fields.date('Date From', readonly=True),
        'date_to': fields.date('Date To', readonly=True),
        'struct_id': fields.many2one('hr.payroll.structure', 'Structure', readonly=True),
        'contract_id': fields.many2one('hr.contract', 'Contract', readonly=True),

        'description': fields.char('Description', readonly=False),#payslip_lines
        'code': fields.char('Code', size=64, readonly=True),
        'category_id': fields.many2one('hr.salary.rule.category', 'Category', readonly=True),
        'total_salary': fields.float('Total Salary', readonly=True),
        'rate': fields.float('Rate (%)', readonly=True),
        'amount': fields.float('Amount', readonly=True),
        'quantity': fields.float('Quantity', readonly=True),
    }
    _order = 'payslip desc'

    def init(self, cr):
        tools.drop_view_if_exists(cr, 'payslip_custom_list')
        cr.execute("""
            create or replace view payslip_custom_list as (
                select
                    min(l.id) as id,
                    l.name as description,
                    l.code as code, 
                    l.category_id as category_id,
                    l.total as total_salary,
                    l.rate as rate, 
                    l.amount as amount, 
                    l.quantity as quantity,
                    ps.number as number,
                    ps.employee_id as employee_id,
                    ps.date_from as date_from,
                    ps.date_to as date_to,
                    ps.struct_id as struct_id,
                    ps.contract_id as contract_id
                from
                    hr_payslip_line l
                      join hr_payslip ps on (l.slip_id=ps.id)
                group by
                    l.id, 
                    l.category_id, 
                    ps.id
            )
        """)