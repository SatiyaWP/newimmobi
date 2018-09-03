{
    "name": "Stock Purchase Requisition",
    "version": "1.0",
    "depends": [
        'stock_analytic_account',
        'stock',
        'purchase_requisition',
        'purchase',
    ],
    "author":"Burgundy",
    "website": "http://www.burgundy.id",
    "category":"Purchase",
    "description" : """Stock Purchase Requisition""",
    'data': [
        'pr_data.xml',
        'pr_view.xml',
        'security/ir.model.access.csv',
        'wizard/pr_create_bids_view.xml',
        'report/report_pr_view.xml',
        'pr_sequence.xml',
    ],
    'demo':[     
    ],
    'test':[
    ],
    'installable' : True,
    'auto_install' : False,
}
