from openerp.osv import fields, osv, orm


class asset_category(osv.osv):
    _description = 'Asset Tags'
    _name = 'asset.category'
    _columns = {
        'name': fields.char('Tag', required=True, translate=True),
        'asset_ids': fields.many2many('asset.asset', id1='category_id', id2='asset_id', string='Assets'),
    }

class po_ext(osv.osv):
         
    _inherit = "asset.asset"   
    _columns = {
        'category_ids': fields.many2many('asset.category', id1='asset_id', id2='category_id', string='Tags'),
        'employee_id': fields.many2one('hr.employee', 'Employee', help="The employee who's borrewed"),
        'contact_numb': fields.char('Contact Number', size=32, help="Contact Employee"),
        'address_id': fields.char('Address', size=64, help="Address Employee"),
        'imei_id': fields.char('Imei', size=64, help="Imei number"),
        'condition' : fields.selection([('new', 'New'),
                                  ('used', 'Used'),('ok','OK'),('broken','Broken')],
                                 string="Condition Type"),
        'color': fields.char('Colour', size=64, help="Colour of Assets"),
        'notes': fields.text('Note',  help="Notes"),
        'qty': fields.float('Qty', help="Quantity"),         
        'price': fields.char('Price', size=64, help="Price Assets"), 
        'model_no': fields.char('Model Number', size=64, help="Model Number"), 
        'serial_pt': fields.char('No. Seri PT', size=64, help="Nomor Seri PT"),       
        
                }