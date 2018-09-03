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

import xlwt
from openerp.addons.report_xls.report_xls import report_xls
from openerp.addons.report_xls.utils import rowcol_to_cell
from openerp.addons.account_financial_report_webkit.report.aged_partner_balance \
    import AccountAgedPartnerBalanceWebkit
from openerp.tools.translate import _
# import logging
# _logger = logging.getLogger(__name__)


def display_line(all_comparison_lines):
    return any([line.get('balance') for line in all_comparison_lines])


class aged_partners_balance_xls(report_xls):
    
    def print_title(self, ws, _p, row_position, xlwt, _xs):
        cell_style = xlwt.easyxf(_xs['xls_title'])
        report_name = ' - '.join([_p.report_name.upper(),
                                 _p.company.partner_id.name,
                                 _p.company.currency_id.name])
        c_specs = [
            ('report_name', 1, 0, 'text', report_name),
        ]
        row_data = self.xls_row_template(c_specs, [x[0] for x in c_specs])
        row_position = self.xls_write_row(
            ws, row_position, row_data, row_style=cell_style)
        return row_position
    
    def print_empty_row(self, ws, row_position):
        c_sizes = self.column_sizes
        c_specs = [('empty%s' % i, 1, c_sizes[i], 'text', None)
                   for i in range(0, len(c_sizes))]
        row_data = self.xls_row_template(c_specs, [x[0] for x in c_specs])
        row_position = self.xls_write_row(
            ws, row_position, row_data, set_column_size=True)
        return row_position
    
    def generate_xls_report(self, _p, _xs, data, objects, wb):
        ws = wb.add_sheet(('Aged Partner Balance'))
        ws.panes_frozen = True
        ws.remove_splits = True
        ws.portrait = 0  # Landscape
        ws.fit_width_to_pages = 1   
        ws.set_horz_split_pos(4)     
        row_pos = 0
        row_pos = self.print_title(ws, _p, row_pos, xlwt, _xs) 
        
        if data['target_move'] == 'posted':
            target_mv = 'All Posted Entries'
        else:
            target_mv = 'All Entries'
             
        if data['result_selection'] == 'customer':
            res_selection = 'Receivable Account'
        elif data['result_selection'] == 'supplier':
            res_selection = 'Payable Account' 
        else :
            res_selection = 'Receivable and Payable Account'  
        
        #style
        cell_format = _xs['bold'] + _xs['fill_blue'] + _xs['borders_all']
        cell_style_center = xlwt.easyxf(cell_format + _xs['center'])  
        cell_style_param = xlwt.easyxf(_xs['borders_all'] + _xs['wrap'] + _xs['top'] + _xs['center'])  
        c_hdr_cell_style = xlwt.easyxf(_xs['bold'] + _xs['fill'] + _xs['borders_all'])
        regular_cell_format = _xs['borders_all']
        regular_cell_style = xlwt.easyxf(regular_cell_format)
        regular_cell_style_decimal = xlwt.easyxf(regular_cell_format + _xs['right'],num_format_str=report_xls.decimal_format)
        regular_cell_style_decimal_total = xlwt.easyxf(regular_cell_format + _xs['right'] + _xs['bold'],num_format_str=report_xls.decimal_format)
        regular_cell_style_bold = xlwt.easyxf(regular_cell_format + _xs['left'] + _xs['bold'])
        cell_style_param_header = xlwt.easyxf(_xs['bold'] + _xs['fill'] + _xs['borders_all'] +_xs['right'])
        cell_format_header = _xs['xls_title'] + _xs['bold'] + _xs['fill'] + _xs['borders_all']
        cell_style_header = xlwt.easyxf(cell_format_header)
        percent_format = report_xls.percentage_format
        percent_style = xlwt.easyxf(regular_cell_format, num_format_str=percent_format)
                  
        #header      
        ws.write_merge(2, 2, 0, 1, 'Fiscal Year', cell_style_center)        
        ws.write_merge(2, 2, 2, 3, 'Period', cell_style_center)   
        ws.write_merge(2, 2, 4, 5, 'Account Filter', cell_style_center)     
        ws.write_merge(2, 2, 6, 7, 'Target Moves', cell_style_center)   
        ws.write_merge(2, 2, 8, 10, 'Chart of Account ', cell_style_center)
        
        ws.row(3).height_mismatch = True
        ws.row(3).height = 28*20         
        ws.write_merge(3, 3, 0, 1, _p.fiscalyear.name, cell_style_param)  
        ws.write_merge(3, 3, 2, 3, "From : 01/"+_p.fiscalyear.name+"  To : "+data['period_to'], cell_style_param)        
        ws.write_merge(3, 3, 4, 5, res_selection, cell_style_param)      
        ws.write_merge(3, 3, 6, 7, target_mv, cell_style_param)   
        ws.write_merge(3, 3, 8, 10, data['chart_account_id'], cell_style_param)
        
        #data
        row_pos = 4
        for current_account in objects:
            #loop account id
            partners_order = _p['partners_order'].get(current_account.id, False)
            # klo ga ada line continue
            if not partners_order:
                continue
            #header data
            row_pos += 1
            ws.write_merge(row_pos, row_pos, 0, 10, current_account.code +" - "+current_account.name, cell_style_header)
            row_pos += 1
            col_count = 0
            ws.col(col_count).width = 256 * 30
            ws.write(row_pos, col_count, 'Partner Name', c_hdr_cell_style)
            col_count += 1
            ws.col(col_count).width = 256 * 30
            ws.write(row_pos, col_count, 'Code / Ref', c_hdr_cell_style)
            col_count += 1
            ws.col(col_count).width = 256 * 20
            ws.write(row_pos, col_count, ' Balance', cell_style_param_header)
            col_count += 1
            #range due
            for range in _p.ranges:
                if str(range[1]) == "100000000000":
                    ranges = 'Overdue > 360'
                elif str(range[0]) == "-100000000000": 
                    ranges = 'Due'
                else:
                    ranges = 'Overdue '+str(range[0]+1)+' - '+ str(range[1])
                #write data range to xls                    
                ws.col(col_count).width = 256 * 20        
                ws.write(row_pos, col_count, ranges, cell_style_param_header)
                col_count += 1
            # ambil data line
            current_partner_amounts = _p['agged_lines_accounts'].get(current_account.id, False)
            current_tot_amounts = _p['agged_totals_accounts'].get(current_account.id, False)
            current_percent_amounts = _p['agged_percents_accounts'].get(current_account.id, False)
             
            for (partner_code_name, partner_id, partner_ref, partner_name) \
                    in partners_order:                
                partner = current_partner_amounts.get(partner_id, {})
                if not partner_name:
                    partner_name = "None"
                
                row_pos += 1
                row_data_start = row_pos
                col_data_start = 0  
                ws.write(row_data_start, col_data_start, partner_name, regular_cell_style)
                col_data_start += 1
                ws.write(row_data_start, col_data_start, partner_ref, regular_cell_style)
                col_data_start += 1
                ws.write(row_data_start, col_data_start, partner['balance'], regular_cell_style_decimal)                
                col_data_start += 1
                # aged_line data
                aged_lines = sorted(partner['aged_lines'].items())
                for aged_line in aged_lines:                      
                    ws.write(row_data_start, col_data_start, aged_line[1], regular_cell_style_decimal)
                    col_data_start += 1  
            # total  
            row_data_start += 1  
            col_data_start = 0          
            ws.write_merge(row_data_start, row_data_start, 0, 0, "Total", regular_cell_style_bold)        
            col_data_start +=2  
            total_lines = sorted(current_tot_amounts.items())
            for total_line in total_lines: 
                ws.write(row_data_start, col_data_start, total_line[1], regular_cell_style_decimal_total)
                col_data_start += 1
                
            #percent
            row_data_start += 1  
            col_data_start = 0           
            ws.write_merge(row_data_start, row_data_start, 0, 1, "Percents", regular_cell_style_bold)
            col_data_start += 3           
            percent_lines = sorted(current_percent_amounts.items())
            for percent_line in percent_lines: 
                ws.write(row_data_start, col_data_start, percent_line[1]/100.0, percent_style)
                col_data_start += 1
                    
            row_pos = row_data_start+1

aged_partners_balance_xls('report.account.account_report_aged_partner_balance_xls',
                     'account.account',
                     parser=AccountAgedPartnerBalanceWebkit)
