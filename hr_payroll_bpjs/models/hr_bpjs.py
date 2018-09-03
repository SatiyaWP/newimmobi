# -*- coding:utf-8 -*-

from openerp.osv import osv, fields
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT
from openerp.tools import float_compare
from openerp.tools.translate import _
from openerp import tools

class wizard_payroll_bpjs(osv.osv_memory):
    _name = 'wizard.payroll.bpjs'
    _description = 'Wizard Payroll BPJS'
        
    _columns = {
        'period_id': fields.many2one('l10n_id.tax_period', 'Period', required=True),
        } 
                
    def list_report(self, cr, uid, ids, context=None):
        period_id=ids[0]
        mod_obj = self.pool.get('ir.model.data')
        wizard = self.browse(cr, uid, ids)[0]
        pick_ids = []
        payroll_bpjs = self.pool.get('payroll.bpjs')
        cr.execute("DELETE from payroll_bpjs")
        cr.execute("""
                    INSERT INTO payroll_bpjs(norut,nik,nik_name,noktp,job_title,date_in,basic,jkk,jkm,jht_002,jht_037,total_premi,jp_1p,jp_2p,remark)
                    SELECT row_number() over() as norut, nik, name, ktp, jabatan, date_in, basic_salary, jkk, jkm, jht_002, jht_037, (jkk + jkm + jht_002 + jht_037 + jp_1p + jp_2p) AS total_premi,jp_1p,jp_2p, '' AS remark
                    FROM (
                        SELECT he.otherid AS nik, he.name_related AS name, he.identification_id AS ktp, hj.name AS jabatan, hc.date_start AS date_in, hc.wage ::float AS basic_salary,
                        (hc.wage*0.0024::float) AS jkk, (hc.wage*0.0030::float) AS jkm, (hc.wage*0.02::float) AS jht_002, (hc.wage*0.037::float) AS jht_037 , (hc.wage*0.01::float) AS jp_1p , (hc.wage*0.02::float) AS jp_2p 
                        FROM hr_payslip hp
                        INNER join hr_contract hc ON hp.contract_id = hc.id
                        INNER join hr_employee he ON hp.employee_id = he.id
                        INNER join hr_job hj ON he.job_id = hj.id
                        WHERE hp.tax_period_id = %s and he.type_employee=%s)x
                    """
                , (wizard.period_id.id,'I',))
        action_model, action_id = tuple(mod_obj.get_object_reference(cr, uid, 'hr_payroll_bpjs', 'action_payroll_bpjs'))
        action = self.pool.get(action_model).read(cr, uid, action_id, context=context) 
        ctx = eval(action['context'])
        ctx.update({
            'search_default_payroll_bpjs': ids[0]
        })
            
        res = {
           'name': 'List Payroll BPJS',
           'view_type': 'form',
           'view_mode': 'tree',
           'res_model': 'payroll.bpjs',
           'type': 'ir.actions.act_window',
           } 
                        
        return res
wizard_payroll_bpjs()

class payroll_bpjs(osv.osv):
    _name = "payroll.bpjs"
    _description = "Payroll BPJS"
    _columns = {
                'norut':fields.integer('No.'),
                'nik':fields.char('NIK'),
                'nik_name': fields.char('Name'),
                'noktp': fields.char('KTP'),
                'job_title': fields.char('Jabatan'),
                'date_in': fields.date('Date In'),
                'basic': fields.float('Basic Salary'),
                'jkk': fields.float('JKK (0,24%)'),
                'jkm': fields.float('JKM (0,30%)'),
                'jht_002': fields.float('JHT (2%)'),
                'jht_037': fields.float('JHT (3,7%)'),
                'jp_1p': fields.float('JP (1%)'),
                'jp_2p': fields.float('JP (2%)'),
                'total_premi': fields.float('Total Premi'),
                'remark': fields.char('Remark'),                
                }      
payroll_bpjs()

class hr_employee(osv.osv):
    _inherit="hr.employee"
    
    _columns={'type_employee':fields.selection([('I','Internal'),('T','Tenaga Ahli')], 'Employee Type', required=True, select=True),              
              }

    _defaults={'type_employee':'I'
               }

