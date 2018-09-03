{
    'name' : 'Purchase Requisition sansaine',
    'version' : '1.1',
    'author' : 'PT. VISI',
    'category' : 'Purchase',
    'description' : """PR FOR Sansaine""",
    'website': 'https://www.visi.co.id',
    'depends' : ['purchase_requisition',
                 'stock'],
    'data': [
         "wizard/cfb_wizard_view.xml",
         "security/ir.model.access.csv",
		 "purchase_requisition_view.xml",
         "purchase_requisition_sequence.xml",
         "purchase_requisition_workflow.xml"
    ],
   
    'installable': True,
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
