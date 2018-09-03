# -*- coding: utf-8 -*-
# © 2017 Ibrohim Binladin | ibradiiin@gmail.com | +62-838-7190-9782 | http://ibrohimbinladin.wordpress.com
##########################################################################################################
{
    "name": "Item of Combo Product, Sales Order Tax, and Sales calculation",
    "version": "0.1",
    "category": "Custom Module",
    "depends": [
        "base",
        "sale",
        "account",
    ],
    # "demo": ["data/immobi_demo.xml",],
    "author":"Ibrohim Binladin | +6283871909782 | ibradiiin@gmail.com",
    "website": "http://ibrohimbinladin.wordpress.com",
    "description": """
    Added some functionality and user interface on the sales order form to client requirements (PT.Immobi Solusi Prima):\n
        1. Items of Combo Product (BoQ), example :\n
           PC-Desktop : consists of 1 Unit CPU, 1 Unit Keyboard, 1 Unit Mouse, and 1 Unit LCD Monitor\n 
           or Product-A : consists of 1 Product-B, 2 Product-C, etc...\n
        2. Adding sale_order_tax_line object into sale_order (Other Component)\n
        3. Calculate gross margins, gross profits and net profit from sales
    """,
    "data": [
        "wizard/combo_product_info_view.xml",
        "security/ir.model.access.csv",
        #"data/immobi_demo.xml",
        "views/view.xml",
    ],
    "installable": True,
    "auto_install": False,
}
