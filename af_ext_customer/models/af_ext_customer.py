# -*- coding: utf-8 -*-
##########################################################################################################
import time
from openerp import SUPERUSER_ID
from openerp.osv import fields, osv
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT
import logging

_logger = logging.getLogger(__name__)

class customer_mapping(osv.osv):
    _name = "customer.mapping"
    _description = "Customer_Mapping"

    _columns = {
        'name': fields.char('Name', required=True),
    }
    
    def _migrate_from_res_partner(self, cr, uid, ids=None, context=None):
        if ids is not None:
            raise NotImplementedError("Ids is just there by convention! Please don't use it.")
        cr.execute("""  SELECT name FROM res_partner
                        WHERE NOT EXISTS ( SELECT * FROM customer_mapping t2, res_partner b2
                                    WHERE t2.name = b2.name )
                   """)
        if  cr.fetchone():
            cr.execute("""  INSERT INTO customer_mapping( name )
                            SELECT name FROM res_partner
                            WHERE NOT EXISTS ( SELECT * FROM customer_mapping t2, res_partner b2
                                               WHERE t2.name = b2.name )
                       """)
            cr.execute("""UPDATE res_partner set customer_id = customer_mapping.id
                          FROM customer_mapping
                          WHERE res_partner.name = customer_mapping.name
                       """)
            _logger.info("Successful data copy from res.partner to customer.mapping")
        else:
            _logger.info("Record customer.mapping is Existing")
        return True
    
    def create(self, cr, uid, vals, context=None):
        cr.execute("delete from customer_mapping where name not in (select name from res_partner)")
        result = super(customer_mapping, self).create(cr, uid, vals, context=context)
        return result

    def write(self, cr, uid, ids, vals, context=None):
        partner_obj = self.pool.get('res.partner')
        if context is None:
            context = {}
        if not ids:
            return True
        if isinstance(ids, (int, long)):
            ids = [ids]
        
        obj = self.browse(cr, uid, ids[0])
        if vals['name']:    
            _partnerid = partner_obj.search(cr, uid, [('name','=',obj.name)])
            if _partnerid :
                partner_obj.write(cr, uid, _partnerid[0], {'name':vals['name']})
        return super(customer_mapping, self).write(cr, uid, ids, vals, context=context)

class res_partner(osv.osv):
    _inherit = "res.partner"
    
    _columns = {
        'customer_id': fields.many2one('customer.mapping', 'Name', copy=False, required=True),
    }
    
#     def create(self, cr, uid, vals, context=None):
#         customer_obj = self.pool.get('customer.mapping')
#         result=None
#         print'vals cust:...................',vals
#         if context is None:
#             context = {}
#         if vals.get('customer_id',[]):
#             customer = customer_obj.browse(cr, uid, vals.get('customer_id',[]))
#             vals['name'] = customer.name
#             result = super(res_partner, self).create(cr, uid, vals, context=context)
#         return result


    def create(self, cr, uid, vals, context=None):
        customer_obj = self.pool.get('customer.mapping')
        result = None
        _cust = None
        if context is None:
            context = {}
        if vals.get('customer_id',[]) or vals['name']:
            if vals.get('customer_id',[]):
                customer = customer_obj.browse(cr, uid, vals.get('customer_id',[]))
                vals['name'] = customer.name
                _cust = vals['name']
            if _cust != vals['name']:
               customerid = customer_obj.search(cr, uid, [('name','=',vals['name'])])
               if not customerid:
                   custid = customer_obj.create(cr, uid, {'name':vals['name']})
                   vals['customer_id'] = custid
            result = super(res_partner, self).create(cr, uid, vals, context=context)
        return result    
    
    def unlink(self, cr, uid, ids, context=None):
        customer_obj = self.pool.get('customer.mapping')
        context = context or {}
        obj = self.browse(cr, uid,ids[0])
        _customerid = customer_obj.search(cr, uid, [('name','=',obj.name)])
        if _customerid:
           customer_obj.unlink(cr, uid,_customerid[0], context=context)
        return super(res_partner, self).unlink(cr, uid, ids, context=context)
        
    def onchange_customer_id(self, cr, uid, ids, customer_id, context=None):
        customer_obj = self.pool.get('customer.mapping')
        if customer_id:
           customer = customer_obj.browse(cr, uid, customer_id)
           _objid = self.search(cr, uid, [('name','=',customer.name)])
           if _objid:
                obj = self.browse(cr, uid,_objid[0])
                res = {
                    'value': {'name': obj.name,
                              'street': obj.street,
                              'function': obj.function,
                              'phone': obj.phone,
                              'mobile': obj.mobile,
                              'email': obj.email,
                              'kode_transaksi': obj.kode_transaksi,
                              'npwp': obj.npwp,
                              'property_account_receivable': obj.property_account_receivable,
                              'property_account_payable': obj.property_account_payable,
                              }
                    }
                return res
        return True
    
    
