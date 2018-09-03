# -*- coding: utf-8 -*-
# © 2017 Ibrohim Binladin | ibradiiin@gmail.com | +62-838-7190-9782 | http://ibrohimbinladin.wordpress.com
##########################################################################################################

import logging
import re
import time

from openerp import _
from openerp.osv import osv
from openerp.report import report_sxw

_logger = logging.getLogger(__name__)


class contract_template_internal(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(contract_template_internal, self).__init__(
            cr, uid, name, context=context)
        active_ids = context['active_ids']

        self.pool.get('hr.contract').check_fields(
                cr, uid, active_ids, context=context)
        self.localcontext.update({
                'time': time,
                'compute_template_variables': self.compute_template_variables,
            })

    def compute_template_variables(self, object, text):
        if text:
            # user can use o instead of object to access fields of object
            o = object
            pattern = re.compile('\$\{(.+?)\}s')
            expression_matches = pattern.findall(str(text.encode('utf-8')))
            for expression in expression_matches:
                error_label = 'Invalid Variable or Python Expression'
                try:
                    value = str(eval(expression))
                    text = text.replace(
                        '${' + expression + '}s',
                        value)
                except:
                    try:
                        value = (
                                    '<font color="red"><strong>[ERROR: %s : %s]<strong></font>') % (
                                    error_label, expression)
                    except Exception as err:
                        value = err
                    text = text.replace(
                        '${' + expression + '}s',
                        value)
                    _logger.error(
                        ("ERROR: %s %s") %
                        (error_label, expression))
        # evaluate object variables
        # this case will be used only for image, above method can't print images with binary data
        # evaluate python expression
        # python expression would use {}
        # eg: ${time.strftime("%d de %B de %Y").decode("utf-8")}s
        # we can't use same bracket
        # because we need to match variables and expressions separately
        # because we need to treat them differently
        # in case of we use same bracket for both of them
        # there is a chance we start matching with the $( of variable and ending
        # on )s or )p of expression
        # which is wrong

        variable_patterns = re.compile('\$\((.*?)\)s')

        matches = variable_patterns.findall(str(text.encode('utf-8')))
        while len(matches):
            value = ''
            type = ''
            if len(matches):
                for match in matches:
                    value = object
                    block = match.split(',')
                    for field in block[0].split('.'):
                        try:
                            type = value._fields[field].type
                            if type != 'selection':
                                value = value[field]
                            else:
                                # get label for selection field
                                value = str(
                                    dict(
                                        value._model.fields_get(
                                            self.cr,
                                            self.uid,
                                            allfields=[field])[field]['selection'])[
                                        unicode(
                                            value[field]).encode('utf-8')])
                        except Exception as err:
                            value = (
                                        '<font color="red"><strong>[ERROR: Field %s doesn\'t exist  in %s]<strong></font>') % (
                                        err, value)
                            _logger.error(
                                ("Field %s doesn't exist  in %s") %
                                (err, value))
                    if value:
                        if type != 'binary':
                            text = text.replace(
                                '$(' + match + ')s', str(unicode(value).encode('utf-8')).decode('utf-8'))

                        else:
                            width, height = '', ''
                            try:
                                if block[1]:
                                    width = ' width="%spx"' % block[1]
                                if block[2]:
                                    height = ' height="%spx"' % block[2]
                                text = text.replace(
                                    '$(' + match + ')s', '<img src="data:image/jpeg;base64,' + str(value) + '"%s%s/>' %
                                    (width, height))
                            except Exception as err:
                                value = _(
                                    u'<font color="red"><strong>[ERROR: Wrong image size indication in "%s". Examples: "(partner_id.image,160,160)" or "(partner_id.image,,160)" or "(partner_id.image,160,)" or "(partner_id.image,,)"]<strong></font>' %
                                    match)
                                _logger.error(
                                    _(
                                        u'Wrong image size indication in "$(%s)s". Examples: $(partner_id.image,160,160)s or $(partner_id.image,,160)s or $(partner_id.image,160,)s or $(partner_id.image,,)s' % match))
                                text = text.replace(
                                    '$(' + match + ')s', str(value))

                    if not value:
                        text = text.replace('$(' + match + ')s', '')
            matches = variable_patterns.findall(str(text.encode('utf-8')))
        return text


class report_contract_template_internal(osv.AbstractModel):
    _name = 'report.ib_immobi_reports.contract_template_internal'
    _inherit = 'report.abstract_report'
    _template = 'ib_immobi_reports.contract_template_internal'
    _wrapped_report_class = contract_template_internal
