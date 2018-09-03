import time
from datetime import datetime
from dateutil.relativedelta import relativedelta

from openerp.osv import fields, osv
import openerp.addons.decimal_precision as dp
from openerp.tools.translate import _
from openerp import SUPERUSER_ID

class asset_depresiasi(osv.osv):
    _inherit = 'account.asset.asset'
    
    _columns={'asset_usage_date': fields.date('Usage Date', required=True, readonly=True, states={'draft':[('readonly',False)]}),
              }


    _defaults = {
        'asset_usage_date': lambda obj, cr, uid, context: time.strftime('%Y-%m-%d'),
    }

    def _get_last_depreciation_date(self, cr, uid, ids, context=None):
        """
        @param id: ids of a account.asset.asset objects
        @return: Returns a dictionary of the effective dates of the last depreciation entry made for given asset ids. If there isn't any, return the purchase date of this asset
        """
        cr.execute("""
            SELECT a.id as id, COALESCE(MAX(l.date),a.asset_usage_date) AS date
            FROM account_asset_asset a
            LEFT JOIN account_move_line l ON (l.asset_id = a.id)
            WHERE a.id IN %s
            GROUP BY a.id, a.asset_usage_date """, (tuple(ids),))
        return dict(cr.fetchall())

    def compute_depreciation_board(self, cr, uid, ids, context=None):
        depreciation_lin_obj = self.pool.get('account.asset.depreciation.line')
        currency_obj = self.pool.get('res.currency')
        for asset in self.browse(cr, uid, ids, context=context):
            if asset.value_residual == 0.0:
                continue
            posted_depreciation_line_ids = depreciation_lin_obj.search(cr, uid, [('asset_id', '=', asset.id), ('move_check', '=', True)],order='depreciation_date desc')
            old_depreciation_line_ids = depreciation_lin_obj.search(cr, uid, [('asset_id', '=', asset.id), ('move_id', '=', False)])
            if old_depreciation_line_ids:
                depreciation_lin_obj.unlink(cr, uid, old_depreciation_line_ids, context=context)

            amount_to_depr = residual_amount = asset.value_residual
            if asset.prorata:
                depreciation_date = datetime.strptime(self._get_last_depreciation_date(cr, uid, [asset.id], context)[asset.id], '%Y-%m-%d')
            else:
                # depreciation_date = 1st January of purchase year
                purchase_date = datetime.strptime(asset.asset_usage_date, '%Y-%m-%d')
                #purchase_date = datetime.strptime(asset.purchase_date, '%Y-%m-%d')
                #if we already have some previous validated entries, starting date isn't 1st January but last entry + method period
                if (len(posted_depreciation_line_ids)>0):
                    last_depreciation_date = datetime.strptime(depreciation_lin_obj.browse(cr,uid,posted_depreciation_line_ids[0],context=context).depreciation_date, '%Y-%m-%d')
                    depreciation_date = (last_depreciation_date+relativedelta(months=+asset.method_period))
                else:
                    if purchase_date.day > 15:
                        depreciation_date = datetime(purchase_date.year,purchase_date.month + 1, 1)
                    else:    
                        depreciation_date = datetime(purchase_date.year,purchase_date.month, 1)
                   # depreciation_date = datetime(purchase_date.year, 1, 1)
            day = depreciation_date.day
            month = depreciation_date.month
            year = depreciation_date.year
            total_days = (year % 4) and 365 or 366

            undone_dotation_number = self._compute_board_undone_dotation_nb(cr, uid, asset, depreciation_date, total_days, context=context)
            print'undone_dotation_number:............',undone_dotation_number
            for x in range(len(posted_depreciation_line_ids), undone_dotation_number):
                i = x + 1
                amount = self._compute_board_amount(cr, uid, asset, i, residual_amount, amount_to_depr, undone_dotation_number, posted_depreciation_line_ids, total_days, depreciation_date, context=context)
                residual_amount -= amount
                last_date_of_month = datetime(depreciation_date.year,depreciation_date.month,1)+relativedelta(months=1,days=-1)
                last_date = last_date_of_month.strftime('%d')
                depre_asset=datetime(depreciation_date.year,depreciation_date.month, int(last_date))
                
                vals = {
                     'amount': amount,
                     'asset_id': asset.id,
                     'sequence': i,
                     'name': str(asset.id) +'/' + str(i),
                     'remaining_value': residual_amount,
                     'depreciated_value': (asset.purchase_value - asset.salvage_value) - (residual_amount + amount),
                     #'depreciation_date': depreciation_date.strftime('%Y-%m-%d'),
                     'depreciation_date': depre_asset.strftime('%Y-%m-%d'),

                }
                depreciation_lin_obj.create(cr, uid, vals, context=context)
                # Considering Depr. Period as months
                depreciation_date = (datetime(year, month, day) + relativedelta(months=+asset.method_period))
                day = depreciation_date.day
                month = depreciation_date.month
                year = depreciation_date.year
        return True

    
    def create(self, cr, uid, vals, context=None):
        if vals.get('asset_usage_date',[]) < vals.get('purchase_date',[]) :
            print'usage:........',vals.get('asset_usage_date',[])
            raise osv.except_osv(_('Tanggal usage date lebih kecil dari purchase date !'), _('Silahkan cek kembali.'))
        return super(asset_depresiasi, self).create(cr, uid, vals, context=context)  

    def write(self, cr, uid, ids, vals, context=None):
        res = super(asset_depresiasi, self).write(cr, uid, ids, vals, context=context)
        for asset in self.browse(cr,uid,ids):
            print asset,vals
            if vals.get('asset_usage_date',[])  :
                if vals.get('purchase_date',[]):
                    if vals['asset_usage_date'] <  vals['purchase_date'] :
                        print'asset.purchase_date:.......',asset.purchase_date,vals['purchase_date']
                        raise osv.except_osv(_('Tanggal usage date lebih kecil dari purchase date !'), _('Silahkan cek kembali.'))
            if vals.get('asset_usage_date',[]) :
                if vals.get('asset_usage_date',[]) <  asset.purchase_date :
                    print'asset.purchase_date:.......',asset.purchase_date
                    raise osv.except_osv(_('Tanggal usage date lebih kecil dari purchase date !'), _('Silahkan cek kembali.'))
            if vals.get('purchase_date',[]):
                if vals.get('purchase_date',[]) >  asset.asset_usage_date :
                    raise osv.except_osv(_('Tanggal usage date lebih kecil dari purchase date !'), _('Silahkan cek kembali.'))
                        
        #print bags
        return res
      

class asset_invoice_line(osv.osv):
    _inherit='account.invoice.line'

    def asset_create(self, cr, uid, lines, context=None):
        context = context or {}
        asset_obj = self.pool.get('account.asset.asset')
        asset_ids = []
        for line in lines:
            if line.invoice_id.number:
                #FORWARDPORT UP TO SAAS-6
                asset_ids += asset_obj.search(cr, SUPERUSER_ID, [('code', '=', line.invoice_id.number), ('company_id', '=', line.company_id.id)], context=context)
        asset_obj.write(cr, SUPERUSER_ID, asset_ids, {'active': False})
        for line in lines:
            if line.asset_category_id:
                vals = {
                    'name': line.name,
                    'code': line.invoice_id.number or False,
                    'category_id': line.asset_category_id.id,
                    'purchase_value': line.price_subtotal,
                    'partner_id': line.invoice_id.partner_id.id,
                    'company_id': line.invoice_id.company_id.id,
                    'currency_id': line.invoice_id.currency_id.id,
                    'purchase_date' : line.invoice_id.date_invoice,
                    'asset_usage_date' : line.invoice_id.date_invoice,
                }
                changed_vals = asset_obj.onchange_category_id(cr, uid, [], vals['category_id'], context=context)
                vals.update(changed_vals['value'])
                asset_id = asset_obj.create(cr, uid, vals, context=context)
                if line.asset_category_id.open_asset:
                    asset_obj.validate(cr, uid, [asset_id], context=context)
        return True
