# -*- coding: utf-8 -*-
##############################################################################
{
    'name': 'Reminder Application HR',
    'version': '0.1',
    'category': 'HR',
    'description': """
Notiikasi email jika ada aplikasi masuk dari pelamar kerja    """,
    'author': 'Tubagus Suhendra (tubagus.suhendra08@gmail.com)',
    'website': 'https://www.defasys.com',
    'depends': ['base','hr','hr_contract','hr_payroll','hr_recruitment','calendar'],
    'data': ['views/config_schedule.xml',
             'views/hr_application_view.xml',
             'edi/hr_application_reminder.xml',
    ],
    'test': [
    ],
    'demo': [
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
