import time
from openerp.osv import fields, osv
from datetime import datetime
from openerp import tools, SUPERUSER_ID
from openerp.tools.translate import _


class email_applicant(osv.osv):
    _inherit='calendar.event'
    
    _columns={'partner_name':fields.char('Applicant'),
              'email_applicant':fields.char('Email'),
              'job_position':fields.char('Job Position')
              }
    
    def create_attendees(self, cr, uid, ids, context=None):
        res = super(email_applicant, self).create_attendees(cr, uid, ids, context=context)
        applicant_id=self.browse(cr,uid,ids[0])
        for event in self.browse(cr,uid,ids):
            if event.email_applicant:
                print 'tess email applicant'
                if self.pool['calendar.attendee']._send_mail_to_applicant_hr(cr, uid, [att.id for att in event.attendee_ids], email_from=event.user_id.partner_id.email, context=context):
                    print'email applicant send'
                    self.message_post(cr, uid, event.id, body=_("An invitation email has been sent to attendee ") , subtype="calendar.subtype_invitation", context=context)
 
             
        return res



class hr_applicant_email(osv.osv):
    _inherit='hr.applicant'
    

    def action_makeMeeting(self, cr, uid, ids, context=None):
        applicant_id=self.browse(cr,uid,ids[0])
        res = super(hr_applicant_email, self).action_makeMeeting(cr, uid, ids, context=context)
        res['context']['default_email_applicant']=applicant_id.email_from
        res['context']['default_partner_name']=applicant_id.partner_name
        res['context']['default_job_position']=applicant_id.job_id.name
        return res
    

class calendar_attendee_applicant(osv.osv):
    _inherit='calendar.attendee'
    
    def _send_mail_to_applicant_hr(self, cr, uid, ids, email_from=tools.config.get('email_from', False),
                                template_xmlid='calendar_template_meeting_invitation_to_applicant', force=False, context=None):
        res = False

        if self.pool['ir.config_parameter'].get_param(cr, uid, 'calendar.block_mail', default=False) or context.get("no_mail_to_attendees"):
            return res

        mail_ids = []
        data_pool = self.pool['ir.model.data']
        mailmess_pool = self.pool['mail.message']
        mail_pool = self.pool['mail.mail']
        template_pool = self.pool['email.template']
        local_context = context.copy()
        color = {
            'needsAction': 'grey',
            'accepted': 'green',
            'tentative': '#FFFF00',
            'declined': 'red'
        }

        if not isinstance(ids, (tuple, list)):
            ids = [ids]

        dummy, template_id = data_pool.get_object_reference(cr, uid, 'ts_email_applicant', template_xmlid)
        dummy, act_id = data_pool.get_object_reference(cr, uid, 'calendar', "view_calendar_event_calendar")
        local_context.update({
            'color': color,
            'action_id': self.pool['ir.actions.act_window'].search(cr, uid, [('view_id', '=', act_id)], context=context)[0],
            'dbname': cr.dbname,
            'base_url': self.pool['ir.config_parameter'].get_param(cr, uid, 'web.base.url', default='http://localhost:8069', context=context)
        })

        for attendee in self.browse(cr, uid, ids, context=context):
            if attendee.email and email_from and (attendee.email != email_from or force):
                ics_file = self.get_ics_file(cr, uid, attendee.event_id, context=context)
                print'attendee.id:.............',attendee.id,template_id
                
                mail_id = template_pool.send_mail(cr, uid, template_id, attendee.id, context=local_context)

                vals = {}
                if ics_file:
                    vals['attachment_ids'] = [(0, 0, {'name': 'invitation.ics',
                                                      'datas_fname': 'invitation.ics',
                                                      'datas': str(ics_file).encode('base64')})]
                vals['model'] = None  # We don't want to have the mail in the tchatter while in queue!
                the_mailmess = mail_pool.browse(cr, uid, mail_id, context=context).mail_message_id
                mailmess_pool.write(cr, uid, [the_mailmess.id], vals, context=context)
                mail_ids.append(mail_id)
        print'mail_ids:.........',mail_ids        
        if mail_ids:
            res = mail_pool.send(cr, uid, mail_ids, context=context)

        return res
