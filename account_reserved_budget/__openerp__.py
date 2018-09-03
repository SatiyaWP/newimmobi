{
    "name": "Reserved Budget",
    "version": "1.0",
    "depends": [
        'base',
        'account',
        'account_budget',
        'stock_purchase_requisition',
        'purchase_budget',
    ],
    "author": "Burgundy",
    "website": "http://www.burgundy.id/",
    "category":"Account Budget",
    "description" : """Reserved Budget""",
    'data': [
        'account_data.xml',
        'account_view.xml',
        'report_account_view.xml',
        'views/report_crossoveredbudget.xml',
    ],
    'demo':[     
    ],
    'test':[
    ],
    'installable' : True,
    'auto_install' : False,
}
