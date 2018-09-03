# -*- coding: utf-8 -*-
# © 2017 Ibrohim Binladin | ibradiiin@gmail.com | +62-838-7190-9782 | http://ibrohimbinladin.wordpress.com
##########################################################################################################
from datetime import datetime

from openerp.osv import fields, osv
import openerp.addons.decimal_precision as dp
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT as OE_DFORMAT

class hr_religion(osv.osv):
    _name = "hr.religion.employee"
    _description = "Religion Employee"
    _columns = {
        'name': fields.char('Religion', size=64, help="Religion Employee", required=True),
    }


class hr_edu_level(osv.osv):
    _name = "hr.employee.edu.level"
    _columns = {
        'name': fields.char('Level of Education', size=64, required=True),
    }


class hr_edu_institutions(osv.osv):
    _name = "hr.employee.edu.institutions"
    _description = "Educational Institutions"
    _columns = {
        'name': fields.char('Institution / Organization', size=124, help="Name of Institution or Organization", required=True),
    }


class hr_edu_majors(osv.osv):
    _name = "hr.employee.edu.majors"
    _description = "Majors"
    _columns = {
        'name': fields.char('Majors', size=256, required=True),
    }


class hr_edu_history(osv.osv):
    _name = 'hr.employee.edu.history'
    _columns = {
        'employee_id': fields.many2one('hr.employee', 'Employee', required=True),
        'name': fields.char('Description', size=124),
        'edu_level_id': fields.many2one('hr.employee.edu.level', 'Level of Education', required=True),
        'institution_id': fields.many2one('hr.employee.edu.institutions', 'Institution / Organization', required=True),
        'majors_id': fields.many2one('hr.employee.edu.majors', 'Majors'),
        'gpa': fields.float('GPA (IPK)', digits_compute=dp.get_precision('Stock Weight')),
    }



class hr_employee(osv.osv):
    _inherit = 'hr.employee'

    def _calculate_age(self, cr, uid, ids, field_name, arg, context=None):

        res = dict.fromkeys(ids, False)
        for ee in self.browse(cr, uid, ids, context=context):
            if ee.birthday:
                dBday = datetime.strptime(ee.birthday, OE_DFORMAT).date()
                dToday = datetime.now().date()
                res[ee.id] = (dToday - dBday).days / 365
        return res

    _columns = {
        'education_line': fields.one2many('hr.employee.edu.history', 'employee_id', 'Education Line', copy=True),
        'religion_id': fields.many2one('hr.religion.employee', 'Religion'),
        'age': fields.function(_calculate_age, type='integer', method=True, string='Age'),
    }


