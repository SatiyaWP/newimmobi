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

from openerp import tools
from openerp.osv import fields, osv
from openerp.addons.decimal_precision import decimal_precision as dp


class report_stock_purchase_requisition(osv.osv):
    _name = "report.stock.purchase.requisition"
    _description = "Purchase Requisition Analysis"
    _auto = False
    _columns = {
        'count_row' : fields.integer('Total Lines'),
        'date': fields.date('Date', readonly=True),
        'year': fields.char('Year', size=4, readonly=True),
        'day': fields.char('Day', size=128, readonly=True),
        'month':fields.selection([('01', 'January'), ('02', 'February'), ('03', 'March'), ('04', 'April'),
            ('05', 'May'), ('06', 'June'), ('07', 'July'), ('08', 'August'), ('09', 'September'),
            ('10', 'October'), ('11', 'November'), ('12', 'December')], 'Month', readonly=True),
        'user_id':fields.many2one('res.users', 'Requestor', readonly=True),
        'product_id':fields.many2one('product.product', 'Product', readonly=True),
        'uom_id':fields.many2one('product.uom', 'Unit of Measure', readonly=True),
        'product_type': fields.selection([
            ('product', 'Stockable'),
            ('consu', 'Consumable'),
            ('service', 'Service'),
            ], 'Product Type', readonly=True),
        'company_id':fields.many2one('res.company', 'Company', readonly=True),
        'stock_pr_id': fields.many2one('stock.purchase.requisition', 'Reference', readonly=True),
        'warehouse_id': fields.many2one('stock.warehouse', 'Deliver to', readonly=True, help="Location where the products requested"),
        'state': fields.selection([
            ('draft', 'Draft'),
            ('cancel', 'Cancelled'),
            ('done', 'Done'),
            ('approved', 'Approved')
            ], 'State', readonly=True),
        'parent_state': fields.selection([
            ('draft', 'Draft'),
            ('cancel', 'Cancelled'),
            ('wait_approval', 'Waiting Approval'),
            ('on_progress', 'On Progress'),
            ('done', 'Done'),
            ], 'Parent State', readonly=True, select=True),
        'product_qty':fields.integer('Quantity', readonly=True),
        'categ_id': fields.many2one('product.category', 'Product Category'),
        'value' : fields.float('Total Value', required=True),
        'analytic_account_id': fields.many2one('account.analytic.account', 'Analytic Account', required=True, readonly=True),
        'day_diff2':fields.float('Lag (Days)', readonly=True, digits_compute=dp.get_precision('Shipping Delay'), group_operator="avg"),
        'day_diff1':fields.float('Requested Lead Time (Days)', readonly=True, digits_compute=dp.get_precision('Shipping Delay'), group_operator="avg"),
        'day_diff':fields.float('Execution Lead Time (Days)', readonly=True, digits_compute=dp.get_precision('Shipping Delay'), group_operator="avg"),
    }
  
    def init(self, cr):
        tools.drop_view_if_exists(cr, 'report_stock_purchase_requisition')
        cr.execute("""
            CREATE OR REPLACE view report_stock_purchase_requisition AS (
                SELECT
                        min(prl.id) as id,
                        count(prl.id) as count_row,
                        date_trunc('day', pr.order_date) as date,
                        to_char(date_trunc('day',pr.order_date), 'YYYY') as year,
                        to_char(date_trunc('day',pr.order_date), 'MM') as month,
                        to_char(date_trunc('day',pr.order_date), 'YYYY-MM-DD') as day,
                        avg(date(prl.date)-date(pr.order_date)) as day_diff,
                        avg(date(prl.schedule_date)-date(pr.order_date)) as day_diff1,
                        avg(date(prl.date)-date(prl.schedule_date)) as day_diff2,
                        pr.user_id as user_id,
                        prl.product_id as product_id,
                        pt.type as product_type,
                        pr.company_id as company_id,
                        pr.id as stock_pr_id,
                        pr.warehouse_id as warehouse_id,
                        pr.state as parent_state,
                        prl.state as state,
                        prl.analytic_account_id as analytic_account_id,
                        pt.categ_id as categ_id,
                        pt.uom_id as uom_id,
                        sum(prl.unit_price * prl.qty) as value,
                        sum(prl.qty) as product_qty
                    FROM
                        stock_purchase_requisition_line as prl
                            LEFT JOIN stock_purchase_requisition pr ON (prl.stock_pr_id=pr.id)                            
                            LEFT JOIN product_product pp ON (prl.product_id=pp.id)                          
                            LEFT JOIN product_template pt ON (pp.product_tmpl_id=pt.id)
                    GROUP BY
                        date_trunc('day',pr.order_date), pr.user_id,
                        prl.product_id, pt.type, pr.company_id,
                        pr.id, pr.warehouse_id, pr.state, prl.state,
                        prl.analytic_account_id, pt.categ_id, year, month, day, pt.uom_id
               )
        """)
   
report_stock_purchase_requisition()