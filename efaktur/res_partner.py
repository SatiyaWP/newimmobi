# -*- coding: utf-8 -*-
##############################################################################
#
#    Alphasoft Solusi Integrasi, PT
#    Copyright (C) 2014 Alphasoft (<http://www.alphasoft.co.id>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################


import itertools
from lxml import etree
from openerp import tools, api
from openerp.osv import fields, osv
from openerp.exceptions import except_orm, Warning, RedirectWarning
import openerp.addons.decimal_precision as dp

ADDRESS_FIELDS = ('street', 'street2', 'rt', 'rw', 'kelurahan_id', 'kecamatan_id', 'kabupaten_id', 'zip', 'city', 'state_id', 'country_id')

class res_partner(osv.Model):
    _inherit = 'res.partner'
    _description = 'res partner'
    
    _columns = {
        'type': fields.selection([('default', 'Default'), 
                                  ('invoice', 'Invoice'),
                                   ('delivery', 'Shipping'), 
                                   ('contact', 'Contact'),
                                   ('npwp', 'NPWP'),
                                   ('other', 'Other')], 'Address Type',
            help="Used to select automatically the right address according to the context in sales and purchases documents."),
        #'nama_npwp': fields.char('Nama NPWP'),
        'npwp': fields.char('NPWP', size=20),
        'kawasan': fields.selection([('yes','YES'),('no','NO')], 'Kawasan', help=''),
        'kode_transaksi': fields.selection([('010','010 Normal'),('020','020 Bendaharawan (Tdk Terlampir)'),('030','030 Bendaharawan (Terlampir)'),('080','080 Tanpa PPN')], 'No. Seri Faktur'),
        'rt': fields.char('RT', size=3),
        'rw': fields.char('RW', size=3),
        'kecamatan_id': fields.many2one('res.kecamatan',"Kecamatan"),
        'kabupaten_id': fields.many2one('res.kabupaten',"Kabupaten"),
        'kelurahan_id': fields.many2one('res.kelurahan',"Kelurahan"),
    }
    
    _defaults = {
        'npwp': '00.000.000.0-000.000',
        'kode_transaksi': '010',
    }
    
    def _address_fields(self, cr, uid, context=None):
        """ Returns the list of address fields that are synced from the parent
        when the `use_parent_address` flag is set. """
        return list(ADDRESS_FIELDS)
    
    def _display_address(self, cr, uid, address, without_company=False, context=None):
        '''
        The purpose of this function is to build and return an address formatted accordingly to the
        standards of the country where it belongs.

        :param address: browse record of the res.partner to format
        :returns: the address formatted in a display that fit its country habits (or the default ones
            if not country is specified)
        :rtype: string
        '''

        # get the information that will be injected into the display format
        # get the address format
        #address_format = address.country_id.address_format or \
        #      "%(street)s\n%(street2)s\n%(city)s %(state_code)s %(zip)s\n%(country_name)s"
        #FORMAT ALAMAT INDONESIA
        address_format = "%(street)s\n%(street2)s RT/RW: %(rt)s/%(rw)s\nKel. %(kelurahan_name)s, Kec. %(kecamatan_name)s, Kab. %(kabupaten_name)s\n%(city)s - %(state_name)s %(zip)s\n%(country_name)s"
        args = {
            'state_code': address.state_id.code or '',
            'state_name': address.state_id.name or '',
            'country_code': address.country_id.code or '',
            'country_name': address.country_id.name or '',
            'company_name': address.parent_name or '',
            'kabupaten_name': address.kabupaten_id.name or '',
            'kecamatan_name': address.kecamatan_id.name or '',
            'kelurahan_name': address.kelurahan_id.name or '',
        }
        for field in self._address_fields(cr, uid, context=context):
            args[field] = getattr(address, field) or ''
        if without_company:
            args['company_name'] = ''
        elif address.parent_id:
            address_format = '%(company_name)s\n' + address_format
        return address_format % args
    
    def onchange_kelurahan_id(self, cr, uid, ids, kelurahan_id, context=None):
        kec_id = kab_id = state_id = country_id = False
        if not kelurahan_id:
            return {'value': {'zip': '', 'kecamatan_id': kec_id,'kabupaten_id': False, 'state_id': False, 'country_id': False}}
        kelurahan_obj = self.pool.get('res.kelurahan').browse(cr, uid, kelurahan_id, context=context)
        if kelurahan_obj.kecamatan_id:
            kec_id = kelurahan_obj.kecamatan_id.id
        if kelurahan_obj.kabupaten_id:
            kab_id = kelurahan_obj.kabupaten_id.id
        if kelurahan_obj.kabupaten_id and kelurahan_obj.kabupaten_id.state_id:
            state_id = kelurahan_obj.kabupaten_id.state_id.id
        if kelurahan_obj.kabupaten_id and kelurahan_obj.kabupaten_id.state_id and kelurahan_obj.kabupaten_id.state_id.country_id:
            country_id = kelurahan_obj.kabupaten_id.state_id.country_id.id
        return {'value': {'zip': kelurahan_obj.zip, 'kecamatan_id': kec_id, 'kabupaten_id': kab_id, 'state_id': state_id, 'country_id': country_id}}
    
    def onchange_kecamatan_id(self, cr, uid, ids, kecamatan_id, context=None):
        kab_id = state_id = country_id = False
        if not kecamatan_id:
            return {'value': {'kabupaten_id': False, 'state_id': False, 'country_id': False}}
        kecamatan_obj = self.pool.get('res.kecamatan').browse(cr, uid, kecamatan_id, context=context)
        if kecamatan_obj.kabupaten_id:
            kab_id = kecamatan_obj.kabupaten_id.id
        if kecamatan_obj.kabupaten_id and kecamatan_obj.kabupaten_id.state_id:
            state_id = kecamatan_obj.kabupaten_id.state_id.id
        if kecamatan_obj.kabupaten_id and kecamatan_obj.kabupaten_id.state_id and kecamatan_obj.kabupaten_id.state_id.country_id:
            country_id = kecamatan_obj.kabupaten_id.state_id.country_id.id
        return {'value': {'kabupaten_id': kab_id, 'state_id': state_id, 'country_id': country_id}}
    
    def onchange_kabupaten_id(self, cr, uid, ids, kabupaten_id, context=None):
        state_id = country_id = False
        if not kabupaten_id:
            return {'value': {'state_id': False, 'country_id': False}}
        kabupaten_obj = self.pool.get('res.kabupaten').browse(cr, uid, kabupaten_id, context=context)
        if kabupaten_obj.state_id:
            state_id = kabupaten_obj.state_id.id
        if kabupaten_obj.state_id and kabupaten_obj.state_id.country_id:
            country_id = kabupaten_obj.state_id.country_id.id
        return {'value': {'state_id': state_id, 'country_id': country_id}}
    
    def onchange_npwp(self, cr, uid, ids, npwp, context=None):
        res = {}
        vals = {}
        if npwp == False:
            return res
        elif len(npwp)==20:
            return {"value":npwp}
        elif len(npwp)==15:
            formatted_npwp = npwp[:2]+'.'+npwp[2:5]+'.'+npwp[5:8]+'.'+npwp[8:9]+'-'+npwp[9:12]+'.'+npwp[12:15]
            vals = {"npwp" : formatted_npwp}
            return {"value":vals}
        else:
            warning = {
                'title': _('Warning'),
                'message': _('Wrong Format must 15 digit'),
            }
            return {'warning': warning, 'value' : {'npwp' : False}}
        return res

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
