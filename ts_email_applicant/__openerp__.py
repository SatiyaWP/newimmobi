# -*- coding: utf-8 -*-
##############################################################################
{
    'name': 'Email Applicant',
    'version': '0.1',
    'category': 'HR',
    'description': """
Send Email Applicant From Calendar    """,
    'author': 'Tubagus Suhendra (tubagus.suhendra08@gmail.com)',
    'website': 'https://www.defasys.com',
    'depends': ['base','hr','hr_recruitment','calendar'],
    'data': [
             'views/base_calendar_view.xml',
             'views/email_template_applicant_view.xml',
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
