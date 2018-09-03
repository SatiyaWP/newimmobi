# -*- coding: utf-8 -*-
# © 2017 Ibrohim Binladin | ibradiiin@gmail.com | +62-838-7190-9782 | http://ibrohimbinladin.wordpress.com
##########################################################################################################

#from openerp.osv import fields, osv
import openerp.addons.jasper_reports as jasper_reports
from datetime import datetime

x = datetime.now()

def sales_report(cr, uid, ids, data, context):
    return { #sip
        'parameters': {
            'order_id': data['order_id'],
            'order_date': data['order_date'],
            'print_datetime': str(datetime(x.year, x.month, x.day, x.hour, x.minute, x.second).strftime("%d-%m-%Y %H:%M:%S")),
        },
    }
jasper_reports.report_jasper(
    'report.sales.order.pdf',
    'sale.order',
    parser=sales_report
    )
jasper_reports.report_jasper(
    'report.quotation.pdf',
    'sale.order',
    parser=sales_report
    )
jasper_reports.report_jasper(
    'report.quotation.other.pdf',
    'sale.order',
    parser=sales_report
    )
    

def boq_report(cr, uid, ids, data, context):
    return {
        'parameters': {
            'title': 'BoQ (Bill of Quantity)',
            'order_id': data['order_id'],
            'SUBREPORT_DIR': data['subdir_report'],
            ##'print_datetime': str(datetime(x.year, x.month, x.day, x.hour, x.minute, x.second).strftime("%d-%m-%Y %H:%M:%S")),
        },
    }
jasper_reports.report_jasper(
    'report.boq2.pdf',  #'report.boq.pdf',
    ##'product.combo.item',
    'sale.order',
    parser=boq_report
    )


def invoice_report(cr, uid, ids, data, context):
    return {
        'parameters': {
            'title': 'INVOICE',
            'inv_date' : data['invoice_date'],
            'print_datetime': str(datetime(x.year, x.month, x.day, x.hour, x.minute, x.second).strftime("%d-%m-%Y %H:%M:%S")),
        },
    }

jasper_reports.report_jasper(
    'report.acc.invoice.pdf',
    'account.invoice',
    parser=invoice_report
    )


def request_reports(cr, uid, ids, data, context):
    return {
        'parameters': {
            'title': 'Request Report',
            'number': data['number'],
            'employee_id': data['employee_id'],
            'move_id': data['move_id'],
            'ref_advance_id': data['ref_advance_id'],
        },
    }

jasper_reports.report_jasper(
    'report.acc.cash.advance.pdf',
    'account.invoice',
    parser=request_reports
    )
jasper_reports.report_jasper(
    'report.acc.reimbursement.pdf',
    'account.invoice',
    parser=request_reports
    )
jasper_reports.report_jasper(
    'report.acc.lpj.pdf',
    'account.invoice',
    parser=request_reports
    )
jasper_reports.report_jasper(
    'report.acc.medical.exp.pdf',
    'account.invoice',
    parser=request_reports
    )


def payslip_report(cr, uid, ids, data, context):
    return {
        'parameters': {
            'title': 'PAYSLIP',
            'employee_id' : data['employee_id'],
            'period_id': data['period_id'],
            'slip_no': data['slip_no'],
            'struct_id': data['struct_id'],
            'contract_id': data['contract_id'],
        },
    }

jasper_reports.report_jasper(
    'report.hr.payslip.pdf',
    'hr.payslip',
    parser=payslip_report
    )
