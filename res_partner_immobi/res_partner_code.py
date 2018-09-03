# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from openerp import api, fields, models, SUPERUSER_ID

class ResPartner(models.Model):
    _inherit="res.partner"

    partner_code_id = fields.Many2one("res.partner.code", string="Partner's Code")
    is_generate_code = fields.Boolean('Generate Code', default=False)

    @api.model
    def create(self, vals):
        vals_ids = super(ResPartner, self).create(vals)
        if vals_ids.partner_code_id:
            vals_ids.is_generate_code = True
            vals_ids.ref = self.env['ir.sequence'].next_by_id(vals_ids.partner_code_id.sequence_id.id) or '/'
        return vals_ids
    
    @api.multi
    def write(self, vals):
        vals_ids = super(ResPartner, self).write(vals)
        for partner in self:
            if not partner.is_generate_code and vals.get('partner_code_id'):
                partner.is_generate_code = True
                seq_id = partner.partner_code_id.sequence_id
                partner.ref = self.env['ir.sequence'].next_by_id(seq_id.id) or '/'
        return vals_ids
    
class PartnerCode(models.Model):
    _name="res.partner.code"
    _description="It gives a sequence number to customers or suppliers"

    name = fields.Char(string='Partner Code', required=True)
    padding = fields.Integer('Number Padding', default=5, help="Number of Digit Code Increment, ex: 00001")
    prefix = fields.Char('Prefix', help="Prefix of code ex: SUPP or CUST")
    suffix = fields.Char('Suffix', help="Suffix of code")
    is_created=fields.Boolean('Created')
    note = fields.Text('Description')
    sequence_id = fields.Many2one('ir.sequence', string='Sequence', readonly=True, copy=False)
        
    @api.model
    def create(self, vals):
        data = {
            'name' : vals['name'],
            'prefix' : vals['prefix'],
            'suffix' : vals['suffix'],
            'padding' : vals['padding'],
        }
        seq_id = self.env['ir.sequence'].create(data)
        vals['is_created'] = True
        vals['sequence_id'] = seq_id.id
        return super(PartnerCode, self).create(vals)
#     
