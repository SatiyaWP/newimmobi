# -*- coding: utf-8 -*-
##############################################################################
#    
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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

import time
from openerp.report import report_sxw
from openerp.osv import osv
from openerp import pooler
import datetime

class order(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(order, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({'time': time})

report_sxw.report_sxw('report.contract.template','contract.template','addons/ts_contract_template/report/order.rml',parser=order)

class contract(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(contract, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({'time': time,
                                  'get_my_startdate': self.get_my_startdate,
                                  'get_my_enddate': self.get_my_enddate,
                                  'get_my_birthday': self.get_my_birthday,
                                  'get_my_contract_date': self.get_my_contract_date,
                                  'get_transport':self.get_transport,
                                  'get_komunikasi':self.get_komunikasi,
                                  'get_jabatan':self.get_jabatan})

    def get_my_startdate(self,date):
        dt = datetime.datetime.strptime(date, '%Y-%m-%d')
        return dt.strftime('%d/%m/%Y')

    def get_my_enddate(self,date):
        dt = datetime.datetime.strptime(date, '%Y-%m-%d')
        return dt.strftime('%d/%m/%Y')

    def get_my_birthday(self,date):
        dt = datetime.datetime.strptime(date, '%Y-%m-%d')
        return dt.strftime('%d/%m/%Y')

    def get_my_contract_date(self,date):
        dt = datetime.datetime.strptime(date, '%Y-%m-%d')
        return dt.strftime('%d/%m/%Y')


    def get_transport(self,data):
        res=[]
        for line in data.struct_id.rule_ids:
            if line.category_id.code == 'TT':
               res.append(line.amount_fix)
        total=sum(res)        
        return total   

    def get_komunikasi(self,data):
        res=[]
        for line in data.struct_id.rule_ids:
            if line.category_id.code == 'TK':
               res.append(line.amount_fix)
        total=sum(res)        
        return total   
    
    def get_jabatan(self,data):
        res=[]
        for line in data.struct_id.rule_ids:
            if line.category_id.code == 'TJ':
               res.append(line.amount_fix)
        total=sum(res)        
        return total   
    
report_sxw.report_sxw('report.contract.internal','hr.contract','addons/ts_contract_template/report/internal.rml',parser=contract)
report_sxw.report_sxw('report.tenaga.ahli','hr.contract','addons/ts_contract_template/report/tenaga_ahli.rml',parser=contract)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

