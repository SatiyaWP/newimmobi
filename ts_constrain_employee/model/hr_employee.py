import time
from openerp.osv import fields, osv
from datetime import datetime
from openerp import tools, SUPERUSER_ID
from openerp.tools.translate import _


class hr_employee_constrain(osv.osv):
    _inherit='hr.employee'



    def create(self, cr, uid, vals, context=None):
        if vals.get('otherid',[]):
            print'otherid:........',vals.get('otherid',[]) 
            employee_search=self.search(cr,uid,[('otherid','=',vals.get('otherid',[]))])
            if employee_search:
                raise osv.except_osv(_('NIK tidak boleh sama !'), _('Silahkan cek kembali.'))
        return super(hr_employee_constrain, self).create(cr, uid, vals, context=context)  

    def write(self, cr, uid, ids, vals, context=None):
        res = super(hr_employee_constrain, self).write(cr, uid, ids, vals, context=context)
        empl_id=self.browse(cr,uid,ids[0])
        if vals.get('otherid',[]) :
            employee_search=self.search(cr,uid,[('otherid','=',vals.get('otherid',[])),('id','!=',empl_id.id),('active','=',False)])
            zz=self.search(cr,uid,[('otherid','=',vals.get('otherid',[]))])
            print'employee_search:...............',employee_search,vals.get('otherid',[]),empl_id.otherid,empl_id.id,zz
            if employee_search:
                raise osv.except_osv(_('NIK tidak boleh sama !'), _('Silahkan cek kembali.'))
            employee_search=self.search(cr,uid,[('otherid','=',vals.get('otherid',[])),('id','!=',empl_id.id),('active','=',True)])
            if employee_search:
                raise osv.except_osv(_('NIK tidak boleh sama !'), _('Silahkan cek kembali.'))
        return res


class hr_contract_constrain(osv.osv):
    _inherit='hr.contract'
    
    def create(self, cr, uid, vals, context=None):
        if vals.get('name',[]):
            employee_search=self.search(cr,uid,[('name','=',vals.get('name',[]))])
            if employee_search:
                raise osv.except_osv(_('Nomor Kontrak tidak boleh sama !'), _('Silahkan cek kembali.'))
        return super(hr_contract_constrain, self).create(cr, uid, vals, context=context)  

    def write(self, cr, uid, ids, vals, context=None):
        res = super(hr_contract_constrain, self).write(cr, uid, ids, vals, context=context)
        for x in self.browse(cr,uid,ids):
            if vals.get('name',[]) :
                employee_search=self.search(cr,uid,[('name','=',vals.get('name',[])),('id','!=',x.id)])
                if employee_search:
                    raise osv.except_osv(_('Nomor Kontrak tidak boleh sama !'), _('Silahkan cek kembali.'))
        return res
    