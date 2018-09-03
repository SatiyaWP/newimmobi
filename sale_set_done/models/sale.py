# import datetime
# from dateutil.relativedelta import relativedelta

from openerp import api, fields, models, _
# from openerp.exceptions import except_orm, Warning, RedirectWarning
# from openerp.tools import float_is_zero, float_compare

# import openerp.addons.decimal_precision as dp

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    @api.multi
    def action_done(self):
        self.state = 'done'
