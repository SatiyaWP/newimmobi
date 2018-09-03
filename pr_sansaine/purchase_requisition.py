from openerp.osv import osv, fields
from openerp.tools.translate import _

class purchase_requisition(osv.Model):
    _inherit = "purchase.requisition"
    _columns = {
        'state': fields.selection([('draft', 'Draft'), ('in_approve', 'Waiting Approval'),
                                   ('in_progress', 'Confirmed'),
                                   ('open', 'Bid Selection'), ('done', 'PO Created'),
                                   ('cancel', 'Cancelled')],
                                  'Status', track_visibility='onchange', required=True,
                                  copy=False),
        "is_pr": fields.boolean("PR", copy=True, default=lambda self: self._context.get('is_pr', False),),            
        'note' : fields.text('Notes'),
    }
    
    _defaults = {
        'name': '/'
    }
    
    def tender_in_approve(self, cr, uid, ids, context=None):
        ctx = context or {}
        for pr in self.browse(cr,uid,ids):
            # Set Name
            if pr.is_pr:
                if pr.name == '/':
                    pr.name = self.pool.get('ir.sequence').get(cr, uid, 'purchase.requisition') or '/'
            else:
                pr.name = self.pool.get('ir.sequence').get(cr, uid, 'purchase.order.requisition') or '/'
            if pr.is_pr:
              pr.write({'state': 'in_approve'})
            if not pr.is_pr:
              self.tender_in_progress(cr, uid, ids)

        return True

    def generate_po(self, cr, uid, ids, context=None):
        super(purchase_requisition, self).generate_po(cr, uid, ids, context=context)
        for tender in self.browse(cr, uid, ids, context=context):
            self.write(cr, uid, tender.id, {'state': 'done'}, context=context)
        return True