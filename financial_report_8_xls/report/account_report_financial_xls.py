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
from symbol import comparison

class ReportStatus(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context=None):
        super(ReportStatus, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'cr': cr,
            'uid': uid,
            'time': time,
        })

class account_report_financial_xls(report_xls):
    def _get_tab(self, level):
        tab = ""
        i = 1
        while i < level:
            tab += "    "
            i += 1
        return tab
        
    
    def generate_xls_report(self, _p, _xs, data, objects, wb):
        ws = wb.add_sheet((data['info']['form']['account_report_id'][1] + 'Report'))
        ws.panes_frozen = True
        ws.remove_splits = True
        ws.portrait = 0  # Landscape
        ws.fit_width_to_pages = 1   
        ws.set_horz_split_pos(6)     
        title_style = xlwt.easyxf(_xs['xls_title'] + _xs['center'])
        ws.write_merge(0, 0, 0, 6, data['info']['form']['account_report_id'][1] + " " + data['company_id'], title_style)
        
        target_move = "All Entries" if data['info']['form']['target_move'] == "all" else "All Posted Entries"
        debit_credit = data['info']['form']['debit_credit'] if not data['info']['form']['enable_filter'] else False
        date_from = data['info']['form']['date_from']
        date_to = data['info']['form']['date_to']
        comparison = data['info']['form']['enable_filter']
        filter_by = "Periods" if data['info']['form']['filter'] == "filter_period" else "Date" if data['info']['form']['filter'] == "filter_date" else "No Filters"

#         #style
        cell_format = _xs['bold'] + _xs['borders_all']
        cell_style_center = xlwt.easyxf(cell_format + _xs['center'])  
        cell_style_head_data = xlwt.easyxf(cell_format) 
        cell_style_head_data_decimal = xlwt.easyxf(cell_format + _xs['right'])  
        cell_style_param = xlwt.easyxf(_xs['borders_all'] + _xs['wrap'] + _xs['top'] + _xs['center'])  
        c_hdr_cell_style = xlwt.easyxf(_xs['bold'] + _xs['fill'] + _xs['borders_all'], num_format_str=report_xls.decimal_format)
        regular_cell_format = _xs['borders_all']
        regular_cell_style = xlwt.easyxf(regular_cell_format, num_format_str=report_xls.decimal_format)

        col_header = 0
        col_header2 = 2
#         #header      
        ws.write_merge(2, 2, col_header, col_header2, "Target Moves", cell_style_center)
        col_header += 3
        col_header2 += 3
        ws.write_merge(2, 2, col_header, col_header2, "Filter by", cell_style_center)
        col_header += 3
        col_header2 += 3
        if date_from:        
            ws.write_merge(2, 2, col_header, col_header2, 'Date from', cell_style_center)
            col_header += 3
            col_header2 += 3
        if date_to:   
            ws.write_merge(2, 2, col_header, col_header2, 'Date to', cell_style_center)     
        
        ws.row(3).height_mismatch = True
        ws.row(3).height = 28 * 30         
        col_header = 0
        col_header2 = 2
        ws.write_merge(3, 3, col_header, col_header2, target_move, cell_style_param)
        col_header += 3
        col_header2 += 3
        period = "Period from " + data['info']['form']['period_from'] + " to" + data['info']['form']['period_to'] if data['info']['form']['period_from'] else " "
        date = "Date from " + data['info']['form']['date_from'] + " to" + data['info']['form']['date_to'] if data['info']['form']['date_from'] else " "
        ws.write_merge(3, 3, col_header, col_header2, filter_by + "\n" + period if data['info']['form']['filter'] == "filter_period" else date if data['info']['form']['filter'] == "filter_date" else "No Filters" , cell_style_param)
        col_header += 3
        col_header2 += 3
        if date_from:        
            ws.write_merge(3, 3, col_header, col_header2, date_from, cell_style_param)
            col_header += 3
            col_header2 += 3
        if date_to:   
            ws.write_merge(3, 3, col_header, col_header2, date_to, cell_style_param)     
          
        # header data
        col_post = 0
        col_head = 0
        seq = 1
        for lines in data['data']:
            ws.col(col_head).width = 256 * 15
            ws.col(col_head + 1).width = 256 * 35
            if seq == 1:
#                 ws.write_merge(5, 5, col_head, col_head + 1, 'Account Name', cell_style_head_data)
                col_head += 2
            if debit_credit or lines[0][0]['elimination']:
                # coa name
                if lines[0][0]['elimination']:
                    ws.write_merge(4, 4, col_head, col_head + 1, lines[0][0]['coa_name'], cell_style_center)
                else:
                    ws.write_merge(4, 4, col_head, col_head + 2, lines[0][0]['coa_name'], cell_style_center)
                ws.col(col_head).width = 256 * 30
                ws.write(5, col_head, 'Debit', cell_style_head_data)
                col_head += 1
                ws.col(col_head).width = 256 * 30
                ws.write(5, col_head, 'Credit', cell_style_head_data)
                col_head += 1
            else:
                # coa name
                ws.write(4, col_head, lines[0][0]['coa_name'], cell_style_center)
            
            ws.col(col_head).width = 256 * 30
            if not lines[0][0]['elimination']:
                ws.write(5, col_head, 'Balance', cell_style_head_data)
            col_head += 1
            if comparison:
                ws.col(col_head).width = 256 * 30
                ws.write(5, col_head, data['info']['form']['label_filter'], cell_style_head_data)
                col_head += 1

            a = col_post
            b = 0
            row_post = 6
            for line in lines[1]:
                if seq == 1:
                    ws.write_merge(row_post, row_post, col_post, col_post + 1, self._get_tab(line['level']) + line['name'], line['header'] and cell_style_head_data or regular_cell_style)
                    col_post += 2
                if debit_credit:
                    if line.get('debit', False) and line.get('credit', False):
                        ws.write(row_post, col_post, line['debit'], line['header'] and cell_style_head_data or regular_cell_style)
                        col_post += 1
                        ws.write(row_post, col_post, line['credit'], line['header'] and cell_style_head_data or regular_cell_style)
                        col_post += 1
                if line.get('balance', False):
                    ws.write(row_post, col_post, line['balance'], line['header'] and cell_style_head_data or regular_cell_style)
                    col_post += 1
                if comparison:
                    if line.get('balance_cmp', False):
                        ws.write(row_post, col_post, line['balance_cmp'], line['header'] and cell_style_head_data or regular_cell_style)
                b = col_post
                col_post = a
                row_post += 1
            col_post = b
            seq += 1
            
account_report_financial_xls('report.financial_report', 'account.move.line', 'addons/financial_report_8_xls/report/report_excel.mako', parser=ReportStatus, header=False)
            
