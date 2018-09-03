# -*- coding: utf-8 -*-
# © 2017 Ibrohim Binladin | ibradiiin@gmail.com | +62-838-7190-9782 | http://ibrohimbinladin.wordpress.com
##########################################################################################################

from openerp import models, api, fields


class contract_template_wizard(models.TransientModel):
    _name = 'contract.template.wizard'


    contract_template_id = fields.Many2one(
        'hr.contract.template.report',
        string='Contract',
        required=True)
    employee_id = fields.Many2one('hr.employee', string='Employee', readonly=True)


    def default_get(self, cr, uid, fields_list, context=None):
        if context is None:
            context = {}
        data = {}
        # assert len(ids) == 1, 'This option should only be used for a single id at a time.'
        active_id = context.get('active_id', False)
        active_model = context.get('active_model', False)
        if active_model == 'hr.contract':
            if active_id:
                model_obj = self.pool.get('hr.contract').browse(cr, uid, active_id)
                if model_obj.contract_template_report_id:
                    data['contract_template_id'] = model_obj.contract_template_report_id.id
                    data['employee_id'] = model_obj.employee_id.id
        return data

    def print_contract(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        if not isinstance(ids, list):
            ids = [ids]

        wizard_obj = self.browse(cr, uid, ids[0])
        active_model = context.get('active_model', False)
        if active_model == 'hr.contract':
            active_ids = context.get('active_ids', [])
        else:
            active_ids = []
            #self.pool.get('ir.model.data').get_object_reference(
                #cr, uid, 'tko_account_contract_report_template', 'analytic_opportunity')[1]
            context.update({'active_model': 'hr.contract',
                            'active_ids': active_ids,})
        contract_obj = self.pool.get('hr.contract')
        #report_body_obj = self.pool.get('account.analytic.account.contract.report.body')
        return contract_obj.generate_contract(
            cr, uid, active_ids, context=context)
