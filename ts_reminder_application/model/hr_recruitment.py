# -*- coding: utf-8 -*-

from openerp.osv import fields, osv
import logging

_logger = logging.getLogger(__name__)


class res_company_mail(osv.osv):
    _inherit="res.company"
    _columns={'email_recepient_id': fields.many2many('res.partner','partner_email_receipt_rel', 'user_company_id', 'partner_id', 'Email Recepient', required=False, change_default=True, select=True),
              }


class hr_recruitment_source(osv.osv):
    _inherit='hr.recruitment.source'
    
    _columns={'send_notif':fields.boolean('Send Email Reminder')
              }

class hr_recruitment(osv.osv):
    _inherit = 'hr.applicant'

    _columns={'status_recruitment':fields.selection([('N','New'),('R','Read')], 'Status Applikasi',  change_default=True, select=True),
              }
    
    _defaults={'status_recruitment':'N'}

    def wkf_send_rfq_reminder(self, cr, uid,  context=None):
        '''
        This function opens a window to compose an email, with the edi mo induk template message loaded by default
        '''
        mail_compose_message=self.pool.get('mail.compose.message')
        ir_model_data = self.pool.get('ir.model.data')
        email_template_object=self.pool.get('email.template')
        company_obj=self.pool.get('res.company')
        hr_applicant=self.pool.get('hr.applicant')
        
        try:
            template_id = ir_model_data.get_object_reference(cr, uid, 'ts_reminder_application', 'email_template_edi_report_recruitment_reminder')[1]
        except ValueError:
            template_id = False
        try:
            compose_form_id = ir_model_data.get_object_reference(cr, uid, 'mail', 'email_compose_message_wizard_form')[1]
        except ValueError:
            compose_form_id = False
        subtype = 'mail.mt_comment'     
        ctx={}
        ctx.update({
            'default_model': 'hr.applicant',
            'default_res_id': [],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'active_model':'hr.applicant',
            'search_disable_custom_filters':True,
            'active_ids':[],
            'active_id':[],
        })
        hr_applicant_search=hr_applicant.search(cr,uid,[('status_recruitment','=','N')])
        for x in  hr_applicant_search:
            print'tes send email reminder:.....................'
            _logger.info("looping applicant hr:......................")
            applicant_id=hr_applicant.browse(cr,uid,x)
            if applicant_id.source_id.send_notif == True:
                _logger.info("looping applicant hr with condition:......................")
                print'11111111111111',applicant_id.company_id
                print'xxxxxxxxxxxxxxxxx',x
                company_obj_id=company_obj.browse(cr,uid,applicant_id.company_id.id)
                print'22222222',company_obj_id
                print'3333333333',company_obj_id.email_recepient_id
                receipt=[f.id for f in company_obj_id.email_recepient_id]
                print'receipt:...............'
                if not receipt:
                     return
                email_templ_obj=self.pool.get('email.template').browse(cr,uid,template_id)
                print'teessss:.............'
                _logger.info("check email receipt:......................")
                post_values = {
                            'subject': email_templ_obj.subject +' '+ applicant_id.name  ,
                            'body': email_templ_obj.body_html,
                            'parent_id': [],
                            'partner_ids': receipt,
                            'attachment_ids': [],
                            'attachments': [],
                        }
                self.message_post(cr, uid, [applicant_id.id], type='comment', subtype=subtype, context=ctx, **post_values)
                hr_applicant.write(cr,uid,applicant_id.id,{'status_recruitment':'R'})
        return True    