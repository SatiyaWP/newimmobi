import time
from openerp.osv import fields, osv
from datetime import datetime
from openerp.tools.translate import _


class AssetMove(osv.osv):
    _name='asset.move'
    _inherit = ['mail.thread', 'ir.needaction_mixin']    
    _description = "Purchase Order"

    _columns={
    'name':fields.char('Asset Move Number',index=True, copy=False, readonly=True, states={'confirm':[('readonly',True)]}),
    'asset_id':fields.many2one('asset.asset',string='Asset', required=True, states={'confirm':[('readonly',True)]} ),
    'description': fields.text('Description', states={'confirm':[('readonly',True)]}),
    'date_move':fields.date('Move Date', required=True, index=True, copy=False, states={'confirm':[('readonly',True)]} ,\
        help="Date Move."),
    'employee_id':fields.many2one('hr.employee', string="Employee", required=True, states={'confirm':[('readonly',True)]} ),
    'location_id':fields.many2one('stock.location', string="Asset Location" ,required=True, states={'confirm':[('readonly',True)]} ),
    'department_id': fields.related('employee_id','department_id',string='Department',readonly=True,type='many2one',relation='hr.department', store=True),
    'state':fields.selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirm')
        ], string='Status', readonly=True, index=True, copy=False, default='draft', track_visibility='onchange'),
    'serial': fields.related('asset_id','serial',string='Serial',readonly=True,type='char', store=True),
    'model': fields.related('asset_id','model',string='Model',readonly=True,type='char', store=True),
    'imei_id': fields.related('asset_id','imei_id',string='Imei',readonly=True,type='char', store=True),
    'image_asset': fields.related('asset_id','image_medium',string='Image',readonly=True,type='binary', store=True),
    'color': fields.related('asset_id','color',string='Color',readonly=True,type='char', store=True),

    }
    _defaults={'state':'draft',
               'date_move':fields.date.context_today}

    def create(self, cr, uid, values, context=None):
          name = self.pool.get('ir.sequence').get(cr, uid, 'asset.move.seq')
          values.update({'name': name})
          res = super(AssetMove,self).create(cr,uid,values,context=context)             
          return res

    def action_confirm(self,cr,uid,ids,context=None):
        asset_obj=self.pool.get('asset.asset')
        asset_move_id=self.browse(cr,uid,ids[0])
        asset_obj.write(cr,uid,asset_move_id.asset_id.id,{'date_move':asset_move_id.date_move,
                                                          'employee_id':asset_move_id.employee_id.id,
                                                          'property_stock_asset':asset_move_id.location_id.id,
                                                          })
        self.write(cr,uid,ids[0],{'state': 'confirm'})
        return True    


#     def set_to_draft(self,cr,uid,ids,context=None):
#         self.write(cr,uid,ids[0],{'state': 'draft'})
#         return True    
    
    def unlink(self, cr, uid, ids, context=None):
        asset_move = self.read(cr, uid, ids, ['state'], context=context)
        unlink_ids = []
        for s in asset_move:
            if s['state'] in ['draft']:
                unlink_ids.append(s['id'])
            else:
                raise osv.except_osv(_('Invalid Action!'), _('Canot Delete,Asset Move has been Confirm.'))
        return super(AssetMove, self).unlink(cr, uid, ids, context=context)

    

class asset_asset_move(osv.osv):
    _inherit='asset.asset'
    _columns={'date_move':fields.date('Move Date', readonly=True),
#              'asset_employee_id':fields.many2one('hr.employee','Employee',  readonly=True),
#              'asset_location_id':fields.many2one('stock.location', string="Location Move" , readonly=True),
              }    
    
    
    
    