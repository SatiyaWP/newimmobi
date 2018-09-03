import time
from datetime import datetime
from dateutil.relativedelta import relativedelta
from openerp import models, fields, api, _
from openerp.osv import fields, osv
import openerp.addons.decimal_precision as dp
from openerp.tools.translate import _

class generate_faktur_pajak(osv.osv_memory):
    _name = 'generate.faktur.pajak'    
    _columns = {
            'nomor_faktur_awal' : fields.char('Nomor Faktur Awal', size=20),
            'nomor_faktur_akhir' : fields.char('Nomor Faktur Akhir', size=20),
            'strip' : fields.char('Strip', size=3),
            'dot' : fields.char('Dot', size=3),
            'strip2' : fields.char('Strip', size=3),
            'dot2' : fields.char('Dot', size=3),
            'nomor_perusahaan' : fields.char('Nomor Perusahaan', size=3, required=True),
            'nomor_awal' : fields.char('Nomor Faktur Awal', size=8, required=True),
            'nomor_akhir' : fields.char('Nomor Faktur Akhir', size=8, required=True),
            'tahun' : fields.char('Tahun Penerbit', size=2,  required=True),
            'type'      : fields.selection([('in','Faktur Pajak Masukan'),('out','Faktur Pajak Keluaran')],'Type'),
    }
    _defaults = {
        'nomor_awal': '',
        'nomor_akhir': '',
        'type': 'out',
        'nomor_faktur_awal':'Nomor Faktur Awal:',
        'nomor_faktur_akhir':'Nomor Faktur Akhir:',
        'strip': '-',
        'dot': '.',
        'strip2': '-',
        'dot2': '.',
    }
    
    def generate_faktur(self, cr, uid, ids, context=None):
        if not context: context={}
        wizard = self.browse(cr, uid, ids[0], context)
        #print "=====wizard.nomor_awal=====",wizard.nomor_awal,int(wizard.nomor_awal)
        #print "=====wizard.nomor_akhir=====",wizard.nomor_akhir,int(wizard.nomor_akhir)
        awal = int(wizard.nomor_awal)
        akhir = int(wizard.nomor_akhir)
        while (awal <= akhir):
            value = {
                'nomor_perusahaan': wizard.nomor_perusahaan,
                'tahun_penerbit': wizard.tahun,
                'nomor_urut': '%08d' % awal,
                'status': '0',
                'type': wizard.type,
            }
            self.pool.get('nomor.faktur.pajak').create(cr,uid,value,context=context)
            awal += 1
        return {'type': 'ir.actions.act_window_close'}
    
    def onchange_nomor_faktur(self, cr, uid, ids, akhir, context=None):
        res = {}
        wizard = self.browse(cr, uid, ids[0], context)
        if akhir <= wizard.nomor_awal:
            warning = {
                'title': _('Warning'),
                'message': _('Wrong Format must 15 digit'),
            }
            return {'warning': warning, 'value' : {'nomor_akhir' : False}}
        return res
    
    
generate_faktur_pajak()