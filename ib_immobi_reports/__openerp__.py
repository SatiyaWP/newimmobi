# -*- coding: utf-8 -*-
# © 2017 Ibrohim Binladin | ibradiiin@gmail.com | +62-838-7190-9782 | http://ibrohimbinladin.wordpress.com
##########################################################################################################
{
    "name": "Custom Report for PT.Immobi Solusi Prima",
    "version": "0.1",
    "category": "Custom Module",
    "depends": [
        "base",
        "sale",
        "jasper_reports",
        "ib_immobi_sales",
        "hr_contract",
        "hr_expense",
        "hr_payroll",
        "account_supplier_adv",
        "hr_reimburse",
        "purchase",
        "purchase_double_validation",
        "sale_margin",
    ],
    "author":"Ibrohim Binladin | +6283871909782 | ibradiiin@gmail.com",
    "website": "http://ibrohimbinladin.wordpress.com",
    "description": """
        Custom Report for Immobi (SO, BoQ, Quo, Contract, etc)
    """,
    "data": [
        'security/purchase_security.xml',
        'security/ir.model.access.csv',
        "views/invoice_view.xml",
        "views/hr_view.xml",
        "views/sale_view.xml",
        "views/project_view.xml",
        "views/purchase_view.xml",
    ],
    "installable": True,
    "application": False,
}
