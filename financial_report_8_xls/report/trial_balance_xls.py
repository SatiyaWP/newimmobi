# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#
#    Copyright (c) 2013 Noviat nv/sa (www.noviat.com). All rights reserved.
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

import re
import time
import xlwt
from openerp.report import report_sxw
from report_engine_xls import report_xls
from openerp.tools.translate import _
from openerp import api

class ReportStatus(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context=None):
        super(ReportStatus, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'cr': cr,
            'uid': uid,
            'time': time,
        })

class account_trial_balance_xls(report_xls):
        
    def generate_xls_report(self, _p, _xs, data, objects, wb):
        ws = wb.add_sheet(('Trial Balance Report'))
        ws.panes_frozen = True
        ws.remove_splits = True
        ws.portrait = 0  # Landscape
        ws.fit_width_to_pages = 1   
        ws.set_horz_split_pos(4)     
        title_style = xlwt.easyxf(_xs['xls_title'])
        ws.write_merge(0, 0, 0, 14, 'TRIAL BALANCE'+" - "+data['company_id']+" - "+data['currency_id'], title_style)

        display_account = target_move = date_from = date_to = ""
        if data['data']['form']['display_account'] == 'all':
            display_account ='All Accounts'
        elif data['data']['form']['display_account'] == 'movement':
            display_account = 'With Movements'
        else:
            display_account = 'With Balance is not Equal to 0'
        
        if data['data']['form']['date_from']:
            date_from = str(data['data']['form']['date_from'])
        else: 
            date_from = '-'
        if data['data']['form']['date_to']:
            date_to = str(data['data']['form']['date_to'])
        else: 
            date_to = '-'
            
        if data['data']['form']['target_move'] == 'all':               
            target_move = 'All Entries' 
        else:
            target_move = 'All Posted Entries'
        
        #style
        cell_format = _xs['bold'] + _xs['fill_blue'] + _xs['borders_all']
        cell_style_center = xlwt.easyxf(cell_format + _xs['center'])  
        cell_style_head_data = xlwt.easyxf(cell_format + _xs['left']) 
        cell_style_head_data_decimal = xlwt.easyxf(cell_format + _xs['right'])  
        cell_style_param = xlwt.easyxf(_xs['borders_all'] + _xs['wrap'] + _xs['top'] + _xs['center'])  
        regular_cell_format = _xs['borders_all']
        regular_cell_style = xlwt.easyxf(regular_cell_format,num_format_str=report_xls.decimal_format)

        #header      
        ws.write_merge(2, 2, 0, 1, 'Display Accounts', cell_style_center)        
        ws.write_merge(2, 2, 2, 3, 'Date', cell_style_center)   
        ws.write_merge(2, 2, 4, 4, 'Target Moves', cell_style_center)     
        
        ws.row(3).height_mismatch = True
        ws.row(3).height = 28*20         
        ws.write_merge(3, 3, 0, 1, display_account, cell_style_param)
        ws.write_merge(3, 3, 2, 3, "From : "+ date_from +"  To : "+ date_to, cell_style_param)  
        ws.write_merge(3, 3, 4, 4, target_move, cell_style_param)      
        
        #header data
        ws.col(0).width = 256 * 15
        ws.write(5, 0, 'Code', cell_style_head_data)
        ws.col(1).width = 256 * 30
        ws.write(5, 1, 'Account', cell_style_head_data)
        ws.col(2).width = 256 * 20
        ws.write(5, 2, 'Debit', cell_style_head_data_decimal)
        ws.col(3).width = 256 * 20
        ws.write(5, 3, 'Credit', cell_style_head_data_decimal)
        ws.col(4).width = 256 * 20
        ws.write(5, 4, 'Balance', cell_style_head_data_decimal)

        row_post = 6
        for line in data['account_res']:
            col_post = 0
            ws.write(row_post, col_post, line['code'], regular_cell_style)
            col_post +=1
            ws.write(row_post, col_post, line['name'], regular_cell_style)
            col_post +=1
            ws.write(row_post, col_post, line['debit'], regular_cell_style)
            col_post +=1
            ws.write(row_post, col_post, line['credit'], regular_cell_style)
            col_post +=1
            ws.write(row_post, col_post, line['balance'], regular_cell_style)
            row_post +=1        
            
account_trial_balance_xls('report.report_trialbalance.excel', 'account.account', 'addons/financial_report_xls/report/report_excel.mako', parser=ReportStatus, header=False)
            
