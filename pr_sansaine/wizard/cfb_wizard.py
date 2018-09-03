import time

from openerp.osv import fields, osv
from openerp.tools.translate import _

class cfb_wizard(osv.osv_memory):
    _name = "cfb.wizard"
    _description = "Calls for Bids Wizard"
    _columns = {
       'cfb_name': fields.char('Name', required=True),
       'date_end': fields.datetime('Bid Submission Deadline'),
       'ordering_date': fields.date('Scheduled Ordering Date'),
       'schedule_date': fields.date('Scheduled Date'),
       'exclusive': fields.selection([("exclusive", "Select only one RFQ (exclusive)"),
                                      ("multiple", "Select multiple RFQ"), ], 'Bid Selection Type'),
       'multiple': fields.boolean('Multiple RFQ per Supplier'),
    }

    _defaults = {
        'cfb_name': '/',
        'date_end': lambda *a: time.strftime('%Y-%m-%d'),
        'ordering_date': lambda *a: time.strftime('%Y-%m-%d'),
        'schedule_date': lambda *a: time.strftime('%Y-%m-%d'),
        'exclusive': 'exclusive',
    }

    def action_ok(self, cr, uid, ids, context=None):
        pr_obj = self.pool.get('purchase.requisition')
        pr = pr_obj.browse(cr, uid, context['active_id'])
        # Cek apakah ada selisih amount
        for wiz in self.browse(cr, uid, ids):
            vals_line = []
            for line in pr.line_ids:
                vals_line.append((0, 0, {
                        'product_id': line.product_id.id,
                        'product_qty': line.product_qty,
                        'product_uom_id': line.product_uom_id.id,
                        'schedule_date': line.schedule_date,
                        'account_analytic_id': line.account_analytic_id.id,
                }))
            
            vals = {
                'name': wiz.cfb_name,
                'is_pr': False,
                'exclusive': wiz.exclusive,
                'account_analytic_id': pr.account_analytic_id.id,
                'multiple_rfq_per_supplier': wiz.multiple,
                'date_end': wiz.date_end,
                'ordering_date': wiz.ordering_date,
                'schedule_date': wiz.schedule_date,
                'origin': pr.name,
                'line_ids': vals_line,
            }
            self.pool.get('purchase.requisition').create(cr, uid, vals, context)
            self.pool.get(context['active_model']).message_post(cr, uid, [pr.id], body=_("Call for Bids Created"), context=context)
            
        return True
