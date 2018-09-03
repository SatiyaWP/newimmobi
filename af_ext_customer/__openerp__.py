# -*- coding: utf-8 -*-
##########################################################################################################
{
    "name": "Ext.Customer Module",
    "version": "0.1",
    'description': """
    Add sugestion on customer name        """,
    "category": "Sale",
    "depends": [
        "base","sale",
    ],
    
    "data": ["security/ir.model.access.csv",
        "views/af_ext_customer_view.xml",
    ],
    "installable": True,
    "auto_install": False,
}
