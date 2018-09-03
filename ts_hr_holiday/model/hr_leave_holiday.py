# -*- coding: utf-8 -*-
# ©  2015 iDT LABS (http://www.@idtlabs.sl)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api, _
from openerp.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta
import calendar
import math


class HrHolidays(models.Model):
    _inherit = 'hr.holidays'

    holidays_date_ids = fields.One2many('hr.holidays.line','leave_holidays_id','Holiday Line')

# 
#     @api.multi
#     def onchange_employee(self, employee_id):
#         res = super(HrHolidays, self).onchange_employee(employee_id)
#         date_from = self.date_from or self.env.context.get('date_from')
#         date_to = self.date_to or self.env.context.get('date_to')
#         if (date_to and date_from) and (date_from <= date_to):
#             if not self._check_date_helper(employee_id, date_from):
#                 raise ValidationError(_("You cannot schedule the start date "
#                                         "on a public holiday or employee's "
#                                         "rest day"))
#             if not self._check_date_helper(employee_id, date_to):
#                 raise ValidationError(_("You cannot schedule the end date "
#                                         "on a public holiday or employee's "
#                                         "rest day"))
#             duration = self._compute_number_of_days(employee_id,
#                                                     date_to,
#                                                     date_from)
#             res['value']['number_of_days_temp'] = duration
#         return res

    @api.multi
    def onchange_date_from(self, date_to, date_from):
        public_holiday=self.env['hr.public.holiday']
        res = super(HrHolidays, self).onchange_date_from(date_to, date_from)
        employee_id = self.employee_id.id or self.env.context.get(
            'employee_id',
            False)
        date = datetime.strptime(date_from, "%Y-%m-%d %H:%M:%S")
        print res['value']['number_of_days_temp'],date.date()
        modified_date = date + timedelta(days=res['value']['number_of_days_temp'])
        
        list_holiday=[]
        search_holiday=public_holiday.search([])
        for x in search_holiday:
             if x.state =='validate':
                 holi_date=datetime.strptime(x.start_date, "%Y-%m-%d")
                 c=holi_date.date()
                 list_holiday.append(c)
        list_leave_holiday=[]
        list_sabtu_minggu=[]
        for i in range(int(res['value']['number_of_days_temp']) + 1):
            leave=date + timedelta(days=i)
            leave_date=leave.date()
            list_leave_holiday.append(leave_date)
            
            day_name=calendar.day_name[leave.weekday()]
            if (day_name == 'Saturday' or day_name=='Sunday'):
                list_sabtu_minggu.append(leave_date)
        compare=set(list_holiday) & set(list_leave_holiday)
        list_total_holiday=[]
        line_list = []
        for date_comp in compare:
            list_total_holiday.append(date_comp)
            vals={'leave_holidays_id':self.id,
                  'holiday_date': date_comp 
                  }
            line_list.append((0,0,vals))
        res['value']['number_of_days_temp']=res['value']['number_of_days_temp'] - len(list_total_holiday) - len(list_sabtu_minggu)   
       # self.holidays_date_ids=line_list
        return res

    @api.multi
    def onchange_date_to(self, date_to, date_from):
        public_holiday=self.env['hr.public.holiday']
        res = super(HrHolidays, self).onchange_date_to(date_to, date_from)
        employee_id = self.employee_id.id or self.env.context.get(
            'employee_id',
            False)
        date = datetime.strptime(date_from, "%Y-%m-%d %H:%M:%S")
        print res['value']['number_of_days_temp'],date.date()
        modified_date = date + timedelta(days=res['value']['number_of_days_temp'])
        
        list_holiday=[]
        search_holiday=public_holiday.search([])
        for x in search_holiday:
             if x.state =='validate':
                 holi_date=datetime.strptime(x.start_date, "%Y-%m-%d")
                 c=holi_date.date()
                 list_holiday.append(c)
        list_leave_holiday=[]
        list_sabtu_minggu=[]
        for i in range(int(res['value']['number_of_days_temp']) + 1):
            leave=date + timedelta(days=i)
            leave_date=leave.date()
            list_leave_holiday.append(leave_date)
            
            day_name=calendar.day_name[leave.weekday()]
            if (day_name == 'Saturday' or day_name=='Sunday'):
                list_sabtu_minggu.append(leave_date)
        compare=set(list_holiday) & set(list_leave_holiday)
        list_total_holiday=[]
        line_list = []
        for date_comp in compare:
            list_total_holiday.append(date_comp)
            vals={'leave_holidays_id':self.id,
                  'holiday_date': date_comp 
                  }
            line_list.append((0,0,vals))
        res['value']['number_of_days_temp']=res['value']['number_of_days_temp'] - len(list_total_holiday) - len(list_sabtu_minggu)   
        #self.holidays_date_ids=line_list
        return res


class hr_holidays_line(models.Model):
    _name='hr.holidays.line'
    
    leave_holidays_id = fields.Many2one('hr.holidays','Holiday Line')
    holiday_date = fields.Date('Date')
    description =  fields.Text('Description')
    
    

class hr_public_holiday(models.Model):
    _inherit='hr.public.holiday'

    start_date =  fields.Date('Date',required="True")
