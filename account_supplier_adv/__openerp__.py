{
    "name": "Invoice, Advance request",
    "version": "1.0",
    "depends": [
        'base', 
        'account', 
        'account_voucher', 
        'account_cancel', 
        'account_withholding_tax',
        'account_reserved_budget',
    ],
    "author": "Burgundy",
    "website": "http://www.burgundy.id/",
    "category":"Accounting",
    "description" : """Request supplier invoice, refund, advance, and settlement""",
    'data': [
        'account_supplier_adv_view.xml',
         "security/ir.model.access.csv",
    ],
    'demo':[     
    ],
    'test':[
    ],
    'installable' : True,
    'auto_install' : False,
}
