# import datetime
# from dateutil.relativedelta import relativedelta

from openerp import api, fields, models, _
# from openerp.exceptions import except_orm, Warning, RedirectWarning
# from openerp.tools import float_is_zero, float_compare

# import openerp.addons.decimal_precision as dp

class res_company(models.Model):
    _inherit = 'res.partner.bank'
    
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id, 
         ondelete='cascade', help="Only if this bank account belong to your company")