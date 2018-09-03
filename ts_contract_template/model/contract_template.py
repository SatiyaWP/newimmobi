import time
from openerp.osv import fields, osv
from datetime import datetime
from openerp.tools.translate import _


class contract_template(osv.osv):
    _name='contract.template'
    _inherit = ['mail.thread', 'ir.needaction_mixin']    
    _description = "Contract Template"

    _columns={
    'name':fields.char('Contract Template Name',index=True, copy=False, ),
    'contract_template_line':fields.one2many('contract.template.line','contract_template_id'),
    'notes':fields.text('Note'),
    'logo_header_immobi':fields.binary('Logo Header Immobi'),
    'partner_id':fields.many2one('res.partner'),
    'description': fields.text('Description', ),
    'description2': fields.text('Description2', ),
    'description3': fields.text('Description3', ),
    'description4': fields.text('Description4', ),
    'description5': fields.text('Description4', ),
    'description6': fields.text('Description4', ),
    'description7': fields.text('Description4', ),
    'description8': fields.text('Description4', ),
    'description9': fields.text('Description4', ),
    'description10': fields.text('Description4', ),
    'description11': fields.text('Description4', ),
    'description12': fields.text('Description4', ),
    'description13': fields.text('Description4', ),
    'description14': fields.text('Description4', ),
    'description15': fields.text('Description4', ),
    'description16': fields.text('Description4', ),
    'description17': fields.text('Description4', ),
    'description18': fields.text('Description4', ),
    'description19': fields.text('Description4', ),
    'description20': fields.text('Description4', ),
    'description21': fields.text('Description4', ),
    'description22': fields.text('Description4', ),
    'description23': fields.text('Description4', ),
    'description24': fields.text('Description4', ),
    'description25': fields.text('Description4', ),
    'description26': fields.text('Description4', ),
    'description27': fields.text('Description4', ),
    'description28': fields.text('Description4', ),
    'description29': fields.text('Description4', ),
    'description30': fields.text('Description4', ),
    'description31': fields.text('Description4', ),
    'description32': fields.text('Description4', ),
    'description33': fields.text('Description4', ),
    'description34': fields.text('Description4', ),
    'description35': fields.text('Description4', ),
    'description36': fields.text('Description4', ),
    'description37': fields.text('Description4', ),
    'description38': fields.text('Description4', ),
    'description39': fields.text('Description4', ),
    'description40': fields.text('Description4', ),
    'description41': fields.text('Description4', ),
    'description42': fields.text('Description4', ),
    'description43': fields.text('Description4', ),
    'description44': fields.text('Description4', ),
    'description45': fields.text('Description4', ),
    'description46': fields.text('Description4', ),
    'description47': fields.text('Description4', ),
    'description48': fields.text('Description4', ),
    'description49': fields.text('Description4', ),
    'description50': fields.text('Description4', ),
    'description51': fields.text('Description4', ),
    'description52': fields.text('Description4', ),
    'description53': fields.text('Description4', ),
    'description54': fields.text('Description4', ),
    'description55': fields.text('Description4', ),
    'description56': fields.text('Description4', ),
##tenaga ahli
    'description_ta': fields.text('Description', ),
    'description_ta2': fields.text('Description2', ),
    'description_ta3': fields.text('Description3', ),
    'description_ta4': fields.text('Description4', ),
    'description_ta5': fields.text('Description4', ),
    'description_ta6': fields.text('Description4', ),
    'description_ta7': fields.text('Description4', ),
    'description_ta8': fields.text('Description4', ),
    }


    def action_confirm(self,cr,uid,ids,context=None):
        for x in self.browse(cr,uid,ids):
            self.write(cr,uid,x.id, {'description':
                                            'Perjanjian Kerja Waktu Tertentu ini (untuk \
                                            selanjutnya disebut "Perjanjian"), dibuat dan \
                                            ditandatangani di Jakarta pada hari Selasa \
                                            tanggal 1 Febuari 2017 oleh dan antara \
                                            PIHAK-PIHAK berikut ini:', 
                                      'description2':'I. PT IMMOBI SOLUSI PRIMA',
                                      'description3':'Suatu Perseroan Terbatas, didirikan pada tanggal 8-9-2014,\
                                              berdasarkan Akta Pendirian No. 3 Notaris Dwi Yulianti, S.H., di Jakarta, telah \
                                              disahkan dengan  Surat Keputusan  Menteri Hukum Dan HAM Republik Indonesia Hukum \
                                               dan HAM RI No. AHU-0101404.40.80.2014 Tahun 2014, berkedudukan di Gedung Tifa, \
                                               Lantai 8 Jalan Kuningan Barat No. 26, Jakarta 12710, dalam hal ini diwakili oleh \
                                               Heksantono Hartadi  dengan jabatan Direktur Utama pada PT. Immobi Solusi Prima, \
                                               dengan demikian sah dan berwenang bertindak untuk dan atas nama PT Immobi Solusi Prima,\
                                                selanjutnya disebut  "PIHAK KESATU";',
                                    'description4':'Dalam hal ini bertindak untuk diri sendiri, selanjutnya disebut  "PIHAK KEDUA"', 
                                    'description5':'Untuk  secara bersama-sama disebut "PARA PIHAK"',
                                    'description6':'PARA PIHAK telah sepakat untuk mengadakan hubungan kerja waktu tertentu dengan ketentuan sebagaimana tersebut dalam pasal-pasal berikut:',
                                    'description7':'PIHAK KESATU mengadakan ikatan kerja dengan PIHAK KEDUA, untuk masa waktu tertentu selama ',
                                    'description8':'(1) PIHAK KESATU akan menempatkan PIHAK KEDUA di lokasi kerja PIHAK PERTAMA, beralamat di Gedung Tifa Lt.8, Jl.Kuningan Barat kav.26 sebagai',     
                                    'description9':'(2) PIHAK KESATU berdasarkan pertimbangan tertentu berhak memindahkan ke bagian lain dan atau \
                                                    mengubah nama jabatan PIHAK KEDUA, dan karenanya PIHAK KEDUA bersedia untuk',
                                    'description10':'dipindahkan ke bagian lain dan atau diubah nama jabatannya sesuai kebutuhan PIHAK KESATU, dengan',                
                                    'description11':'pemberitahuan tertulis dari PIHAK KESATU kepada PIHAK KEDUA.' ,
                                    'description12':'(1) Selama perjanjian berlangsung, PIHAK KEDUA berhak untuk memperoleh:',
                                    'description13':'a. Gaji dan fasilitas dari PIHAK KESATU sebagaimana tercantum pada Lampiran 1 Perjanjian ini, merupakan kesatuan dan menjadi bagian yang tak terpisahkan dengan Perjanjian ini.',
                                    'description14':'b. Sarana pendukung dari PIHAK KESATU untuk menunjang Jenis Pekerjaan sebagaimana disebutkan dalam Pasal 2 ayat (1) Perjanjian ini, dan ditetapkan dalam Lampiran 1 Perjanjian ini yang merupakan kesatuan dan menjadi bagian yang tak terpisahkan dengan  Perjanjian ini.',
                                    'description15':'c. Akses kepada karyawan, data, informasi pada lingkungan perusahaan PIHAK KESATU terkait Jenis Pekerjaan sebagaimana disebutkan dalam Pasal 2 ayat (1) Perjanjian ini',
                                    'description16':'(2) Selama jangka waktu perjanjian sebagaimana tersebut dalam Pasal 1 Perjanjian ini , PIHAK KEDUA berkewajiban untuk: ',
                                    'description17':'a. Melaksanakan tugas dan kewajiban umum sesuai dengan kebijakan perusahaan, yakni:',
                                    'description18':'i. Melaksanakan tugas dengan sebaik-baiknya serta berusaha semaksimal mungkin ditujukan untuk kepentingan dan kemajuan perusahaan;',
                                    'description19':'ii. Memberikan dan menyampaikan segala gagasan, masukan, informasi, dan atau laporan yang dianggap penting dan relevan untuk kemajuan perusahaan;',
                                    'description20':'b. Melaksanakan tugas dan kewajiban khusus sebagaimana ditetapkan dalam Lampiran 2, Perjanjian ini, yang merupakan kesatuan dan menjadi bagian tak terpisahkan dalam Perjanjian ini.',
                                    'description21':'c. Mencurahkan waktu, perhatian dan kemampuannya pada perusahaan dan hal-hal lain yang menyangkut kepentingan perusahaan',
                                    'description22':'d. Terikat untuk tetap mandiri dari semua pihak dan bertindak untuk menjaga kepentingan perusahaan.',
                                    'description23':'e. Tidak terlibat baik secara langsung maupun tidak langsung dalam usaha maupun jabatan lain yang sejenis dengan Jenis Pekerjaan sebagaimana disebutkan dalam Pasal 2 ayat (1) Perjanjian ini.',
                                    'description24':'(3) PARA PIHAK mengadakan evaluasi setiap 3 (tiga) bulan atas kinerja dan realisasi dari pekerjaan dan tanggung jawab  yang telah ditetapkan pada Lampiran 2  Perjanjian ini.',
                                    'description25':'(4) Apabila hasil evaluasi yang tersebut dalam Pasal 3 ayat (3) Perjanjian ini PIHAK KEDUA tidak dapat meneruskan Perjanjian ini, maka PIHAK KEDUA dapat mengajukan permintaan untuk mengundurkan diri secara sukarela dengan tanpa memperoleh penggantian apapun dari PIHAK KESATU, dengan pemberitahuan tertulis paling lambat  30 hari  sebelum tanggal pengunduran diri.',
                                    'description26':'(1) Hari Kerja normal adalah Senin sampai dengan Jumat, kecuali diperjanjikan lain sebagaimana pada Lampiran 2 Perjanjian ini.',
                                    'description27':'(2) Jam kerja normal dimulai jam 08.30 sampai dengan jam 17.30, dengan waktu istirahat maksimal 1 jam, kecuali diperjanjikan lain sebagaimana disebutkan dalam Lampiran 2 Perjanjian ini dan total jam kerja normal dalam 1 minggu adalah 40 jam.',
                                    'description28':'(3) Ketentuan waktu kerja ini dapat berubah sewaktu-waktu sesuai dengan kebutuhan PIHAK KESATU. Setiap perubahan tentang waktu kerja akan diberitahukan kepada PIHAK KEDUA dan bersifat mengikat.',
                                    'description29':'(1) Perjanjian ini tunduk pada Peraturan Perundangan Tentang Ketenagakerjaan di Indonesia.',
                                    'description30':'(2) PIHAK KEDUA setuju untuk patuh kepada segala peraturan dan tata tertib yang berlaku pada perusahaan PIHAK KESATU, dan taat pada tatanan hukum yang berlaku di Negara Republik Indonesia.',
                                    'description31':'(3) PIHAK KEDUA tidak berhak dan dilarang keras menyebarkan semua data dan/atau informasi yang bersifat rahasia dalam bentuk dan alasan apapun seperti dan tidak terbatas pada keterangan pelanggan, pemasok, formula, contoh barang, rencana kerja, metode dan rahasia dagang, yang diketahuinya baik secara langsung, maupun tidak langsung sehubungan dengan pekerjaannya kepada pihak lain tanpa seizin tertulis dari PIHAK KESATU, baik selama Perjanjian ini berlangsung, maupun 60 (enam puluh) bulan setelah berakhirnya jangka waktu Perjanjian ini.',
                                    'description32':'(1) PIHAK KESATU berhak secara sepihak mengakhiri Perjanjian ini setiap waktu, jika terjadi hal-hal sebagaimana disebutkan di bawah ini:',
                                    'description33':'a. PIHAK KEDUA secara berturut-turut selama 5 (lima) hari telah meninggalkan pekerjaannya tanpa pemberitahuan secara tertulis dan tanpa alasan yang dapat dipertanggungjawabkan.',
                                    'description34':'b. PIHAK KEDUA dijatuhi hukuman oleh Instansi yang berwajib karena tindakan kriminal yang dilakukan.',
                                    'description35':'c. PIHAK KEDUA meninggal dunia, mengalami gangguan kesehatan kronis atau berada dalam penanganan dokter karena gangguan kesehatan kronis.',
                                    'description36':'d. PIHAK KEDUA tidak cakap melakukan pekerjaannya walaupun sudah diberi peringatan.',
                                    'description37':'e. Pada saat kesepakatan kerja diadakan, PIHAK KEDUA memberikan keterangan palsu atau dipalsukan.',
                                    'description38':'f. Apabila PIHAK KEDUA melakukan pelanggaran ringan dan telah diberikan 3 (tiga) kali surat peringatan, namun tidak memperbaiki diri.',
                                    'description39':'(2) Apabila, karena satu dan lain hal Perjanjian ini berakhir sebagaimana disebutkan dalam Pasal 3 ayat (4), Pasal 5 ayat (3), Pasal 6 ayat (1) Perjanjian ini,  maka PIHAK KEDUA harus mengembalikan fasilitas dan sarana penunjang yang diberikan oleh perusahaan sebagaimana disebutkan pada Lampiran 1 Perjanjian ini.',
                                    'description40':'(3) Pada saat  Perjanjian ini berakhir, PIHAK KEDUA wajib menyerahkan seluruh catatan, memorandum, surat-menyurat dan dokumen lain serta barang-barang milik perusahaan, baik secara fisik maupun data digital, kecuali hasil penelitian-penelitian serta tulisan-tulisan ilmiah yang dibuat oleh PIHAK KEDUA selama jangka waktu berlakunya Perjanjian ini yang merupakan hak cipta pribadi dari PIHAK KEDUA.  PIHAK KEDUA tidak akan menahan salinan dari dokumen-dokumen milik perusahaan serta tidak akan mempergunakannya untuk kepentingan sendiri dan atau untuk orang/pihak lain.',
                                    'description41':'(4) Apabila Perjanjian ini berakhir karena alasan-alasan sebagaimana tersebut dalam Pasal 5 ayat (3) dan Pasal  6 ayat (1) Perjanjian ini, PIHAK KEDUA tidak lagi mempunyai hubungan kerja atau kaitan apapun dengan PIHAK KESATU, dan oleh karenanya PIHAK KEDUA tidak akan mengajukan segala tuntutan, klaim, gugatan dan ganti rugi dalam bentuk apapun kepada PIHAK KESATU sehubungan dengan berakhirnya hubungan kerja tersebut dan/ atau Perjanjian ini.',
                                    'description42':'(5) Apabila masa berlakunya Perjanjian ini telah selesai atau sekalipun diperpanjang dan berakhir pula masa berlakunya, maka hubungan kerja PIHAK KESATU dengan PIHAK KEDUA putus dengan sendirinya, kecuali PARA PIHAK menginginkan perpanjangan masa Perjanjian ini.',
                                    'description43':'(6) PIHAK KESATU tidak berhak membayar kewajiban dalam bentuk apapun kepada PIHAK KEDUA bilamana jangka waktu Perjanjian ini berakhir, termasuk jika terdapat perpanjangan atau perubahan terhadap Perjanjian ini, kecuali upah PIHAK KEDUA pada bulan berjalan.',
                                    'description44':'(1) Perjanjian ini ditafsirkan, tunduk dan diatur serta dilaksanakan menurut Hukum Negara Republik Indonesia.',
                                    'description45':'(2) Perjanjian ini tidak dapat diubah atau dimodifikasi kecuali dengan persetujuan tertulis bersama PARA PIHAK.',
                                    'description46':'(3) Kecuali disetujui secara tegas dalam suatu dokumen terpisah, Perjanjian ini menggantikan semua perjanjian dan kesepakatan lain yang ada dan atau telah dibuat sebelum tanggal penjanjian ini, baik tertulis maupun tidak tertulis, yang dibuat oleh PARA PIHAK mengenai pokok masalah yang sama.',
                                    'description47':'(4) Jika ada salah satu atau lebih ketentuan Perjanjian ini dinyatakan atau menjadi tidak sah atau tidak dapat dilaksanakan, maka tidak absahnya atau tidak dapat dilaksanakannya ketentuan-ketentuan tersebut tidak akan mempengaruhi keabsahan Perjanjian ini secara keseluruhan dan dapat dilaksanakannya ketentuan lainnya dari Perjanjian ini. PARA PIHAK wajib untuk mengganti ketentuan yang dinyatakan atau menjadi tidak sah atau tidak dapat dilaksanakan tersebut dengan ketentuan lain yang sah yang dapat dilaksanakan yang memiliki maksud dan pengertian yang terdekat dengan ketentuan yang digantikan tersebut.',
                                    'description48':'(5) Judul Perjanjian ini dan setiap pasal-pasal yang terkandung di dalamnya dinyatakan demikian untuk maksud kemudahan saja dan tidak akan mempengaruhi penafsiran dari perjanjian dan masing-masing pasal yang bersangkutan. ',
                                    'description49':'(1) Setiap pemberitahuan atau komunikasi yang menyangkut Perjanjian ini wajib dilakukan secara tertulis dalam bahasa Indonesia dan diserahkan langsung atau dengan jasa kurir atau fax atau email yang dialamatkan kepada:',
                                    'description50':'(2) Perubahan atas nama, alamat, telepon, fax, atau email yang tercantum dalam ayat (1) wajib diberitahukan kepada PIHAK lainnya dalam waktu 7 (tujuh) hari kerja setelah perubahan tersebut efektif.',
                                    'description51':'(3) Segala macam perselisihan yang mungkin timbul dalam perjanjian ini atau dalam pelaksanaannya akan diselesaikan secara musyawarah mufakat terlebih dahulu dengan atasan langsung dan/ atau pimpinan perusahaan yang diwakilkan.',
                                    'description52':'(4) Apabila dalam tahap penyelesaian dengan atasan langsung tersebut belum juga terselesaikan, maka perselisihan dan perbedaan pendapat tersebut dapat diajukan secara tertulis kepada pimpinan perusahaan guna dicarikan jalan keluar yang layak dan adil sesuai kondisi yang berlaku secara umum serta mengacu kepada ketentuan perundang-undangan yang berlaku.',
                                    'description53':'(5) Apabila penyelesaian sebagaimana termaksud dalam Pasal 8 ayat (4) Perjanjian ini tidak berlangsung, maka PARA PIHAK sepakat meminta penyelesaiannya kepada kantor Departemen Tenaga Kerja setempat.',
                                    'description54':'Demikian Perjanjian ini dibuat, ditandatangani pada hari dan tanggal sebagaimana disebutkan pada awal Perjanjian ini dibuat tanpa ada paksaan dari siapapun dan dibuat dalam keadaan sadar, sehat jasmani dan rohani. Setelah dibaca dan dipahami serta disetujui isinya yang kemudian ditandatangani oleh PARA PIHAK, dalam rangkap 2, yang sama isi dan ketentuan hukumnya, masing-masing untuk PARA PIHAK, dan diberlakukan pada hari dan tanggal sebagaimana disebutkan terlebih dahulu di bagian depan Perjanjian ini.',
            ##tenaga ahli
                                    'description_ta':'Perjanjian Pelayanan Jasa ini (untuk selanjutnya disebut "Perjanjian"), dibuat dan ditandatangani di Jakarta pada hari Jumat tanggal 19 bulan Mei tahun dua ribu tujuh belas (19- 5 - 2017) oleh dan antara PIHAK-PIHAK sebagai berikut :',           
                                    'description_ta2':'1. PT. IMMOBI SOLUSI PRIMA, berkedudukan di Gedung Tifa, lantai 8 suite 803, Jalan Kuningan Barat No.26, Jakarta Selatan-12710, didirikan menurut hukum negara Republik Indonesia berdasarkan Akta Pendirian No.03 tanggal 8 September 2014, yang dibuat oleh/di hadapan Dwi Yulianti, S.H., Notaris di Jakarta Selatan, dan telah mendapatkan pengesahan sebagai Badan Hukum melalui Surat Keputusan Menteri Hukum Dan Hak Asasi Manusia Republik Indonesia No. AHU-27695.40.10.2014 tanggal 2 Oktober 2014, dan terakhir telah mengalami perubahan melalui Akta No.05 tanggal 10 Maret 2016 yang dibuat oleh/di hadapan Notaris yang sama tersebut. Dalam hal ini diwakili oleh Asiyah dalam jabatannya selaku Head Of HR & GA, dengan demikian sah bertindak atas nama dan untuk kepentingan PT. Immobi Solusi Prima. Untuk selanjutnya disebut "PIHAK PERTAMA".',
                                    'description_ta3':'Dalam hal ini bertindak atas nama dan untuk kepentingan diri sendiri. Untuk selanjutnya disebut "PIHAK KEDUA"',
                                    'description_ta4':'Dengan ini PARA PIHAK telah sepakat untuk membuat, menandatangani dan melaksanakan Perjanjian ini dengan syarat-syarat dan ketentuan-ketentuan sebagaimana berikut :',
                                    'description_ta5':'tempat/kedudukan lain dari lokasi kerja atau lokasi project perusahaan, maupun mengubah tugas dan tanggung jawab nya, dan oleh karenanya PIHAK KEDUA bersedia untuk dipindahkan ke tempat/kedudukan lain dari lokasi kerja atau lokasi project perusahaan, maupun diubah tugas dan tanggung jawabnya sesuai kebutuhan PIHAK PERTAMA.',
                                    'description_ta6':'Mei (05) dua ribu tujuh belas (2017) dan akan berakhir pada tanggal Dua  Puluh Delapan   (28) Agustus  (08) dua ribu tujuh belas (2017). ',
                                    'description_ta7':'Perjanjian ini, yang merupakan satu kesatuan dan menjadi bagian yang tak terpisahkan dalam perjanjian ini;',
                                    'description_ta8':'perjanjian ini, yang dibayarkan berdasarkan sistem reimbursement atas dasar bukti-bukti pembayaran asli dan resmi;',
                                    })
            hr_contract_obj=self.pool.get('hr.contract')
            hr_contract_search=hr_contract_obj.search(cr,uid,[])
            for contract in hr_contract_search:
                hr_contract_obj.write(cr,uid,contract, {'description':
                                            'Perjanjian Kerja Waktu Tertentu ini (untuk \
                                            selanjutnya disebut "Perjanjian"), dibuat dan \
                                            ditandatangani di Jakarta pada hari Selasa \
                                            tanggal 1 Febuari 2017 oleh dan antara \
                                            PIHAK-PIHAK berikut ini:', 
                                      'description2':'I. PT IMMOBI SOLUSI PRIMA',
                                      'description3':'Suatu Perseroan Terbatas, didirikan pada tanggal 8-9-2014,\
                                              berdasarkan Akta Pendirian No. 3 Notaris Dwi Yulianti, S.H., di Jakarta, telah \
                                              disahkan dengan  Surat Keputusan  Menteri Hukum Dan HAM Republik Indonesia Hukum \
                                               dan HAM RI No. AHU-0101404.40.80.2014 Tahun 2014, berkedudukan di Gedung Tifa, \
                                               Lantai 8 Jalan Kuningan Barat No. 26, Jakarta 12710, dalam hal ini diwakili oleh \
                                               Heksantono Hartadi  dengan jabatan Direktur Utama pada PT. Immobi Solusi Prima, \
                                               dengan demikian sah dan berwenang bertindak untuk dan atas nama PT Immobi Solusi Prima,\
                                                selanjutnya disebut  "PIHAK KESATU";',
                                    'description4':'Dalam hal ini bertindak untuk diri sendiri, selanjutnya disebut  "PIHAK KEDUA"', 
                                    'description5':'Untuk  secara bersama-sama disebut "PARA PIHAK"',
                                    'description6':'PARA PIHAK telah sepakat untuk mengadakan hubungan kerja waktu tertentu dengan ketentuan sebagaimana tersebut dalam pasal-pasal berikut:',
                                    'description7':'PIHAK KESATU mengadakan ikatan kerja dengan PIHAK KEDUA, untuk masa waktu tertentu selama ',
                                    'description8':'(1) PIHAK KESATU akan menempatkan PIHAK KEDUA di lokasi kerja PIHAK PERTAMA, beralamat di Gedung Tifa Lt.8, Jl.Kuningan Barat kav.26 sebagai',     
                                    'description9':'(2) PIHAK KESATU berdasarkan pertimbangan tertentu berhak memindahkan ke bagian lain dan atau \
                                                    mengubah nama jabatan PIHAK KEDUA, dan karenanya PIHAK KEDUA bersedia untuk',
                                    'description10':'dipindahkan ke bagian lain dan atau diubah nama jabatannya sesuai kebutuhan PIHAK KESATU, dengan',                
                                    'description11':'pemberitahuan tertulis dari PIHAK KESATU kepada PIHAK KEDUA.' ,
                                    'description12':'(1) Selama perjanjian berlangsung, PIHAK KEDUA berhak untuk memperoleh:',
                                    'description13':'a. Gaji dan fasilitas dari PIHAK KESATU sebagaimana tercantum pada Lampiran 1 Perjanjian ini, merupakan kesatuan dan menjadi bagian yang tak terpisahkan dengan Perjanjian ini.',
                                    'description14':'b. Sarana pendukung dari PIHAK KESATU untuk menunjang Jenis Pekerjaan sebagaimana disebutkan dalam Pasal 2 ayat (1) Perjanjian ini, dan ditetapkan dalam Lampiran 1 Perjanjian ini yang merupakan kesatuan dan menjadi bagian yang tak terpisahkan dengan  Perjanjian ini.',
                                    'description15':'c. Akses kepada karyawan, data, informasi pada lingkungan perusahaan PIHAK KESATU terkait Jenis Pekerjaan sebagaimana disebutkan dalam Pasal 2 ayat (1) Perjanjian ini',
                                    'description16':'(2) Selama jangka waktu perjanjian sebagaimana tersebut dalam Pasal 1 Perjanjian ini , PIHAK KEDUA berkewajiban untuk: ',
                                    'description17':'a. Melaksanakan tugas dan kewajiban umum sesuai dengan kebijakan perusahaan, yakni:',
                                    'description18':'i. Melaksanakan tugas dengan sebaik-baiknya serta berusaha semaksimal mungkin ditujukan untuk kepentingan dan kemajuan perusahaan;',
                                    'description19':'ii. Memberikan dan menyampaikan segala gagasan, masukan, informasi, dan atau laporan yang dianggap penting dan relevan untuk kemajuan perusahaan;',
                                    'description20':'b. Melaksanakan tugas dan kewajiban khusus sebagaimana ditetapkan dalam Lampiran 2, Perjanjian ini, yang merupakan kesatuan dan menjadi bagian tak terpisahkan dalam Perjanjian ini.',
                                    'description21':'c. Mencurahkan waktu, perhatian dan kemampuannya pada perusahaan dan hal-hal lain yang menyangkut kepentingan perusahaan',
                                    'description22':'d. Terikat untuk tetap mandiri dari semua pihak dan bertindak untuk menjaga kepentingan perusahaan.',
                                    'description23':'e. Tidak terlibat baik secara langsung maupun tidak langsung dalam usaha maupun jabatan lain yang sejenis dengan Jenis Pekerjaan sebagaimana disebutkan dalam Pasal 2 ayat (1) Perjanjian ini.',
                                    'description24':'(3) PARA PIHAK mengadakan evaluasi setiap 3 (tiga) bulan atas kinerja dan realisasi dari pekerjaan dan tanggung jawab  yang telah ditetapkan pada Lampiran 2  Perjanjian ini.',
                                    'description25':'(4) Apabila hasil evaluasi yang tersebut dalam Pasal 3 ayat (3) Perjanjian ini PIHAK KEDUA tidak dapat meneruskan Perjanjian ini, maka PIHAK KEDUA dapat mengajukan permintaan untuk mengundurkan diri secara sukarela dengan tanpa memperoleh penggantian apapun dari PIHAK KESATU, dengan pemberitahuan tertulis paling lambat  30 hari  sebelum tanggal pengunduran diri.',
                                    'description26':'(1) Hari Kerja normal adalah Senin sampai dengan Jumat, kecuali diperjanjikan lain sebagaimana pada Lampiran 2 Perjanjian ini.',
                                    'description27':'(2) Jam kerja normal dimulai jam 08.30 sampai dengan jam 17.30, dengan waktu istirahat maksimal 1 jam, kecuali diperjanjikan lain sebagaimana disebutkan dalam Lampiran 2 Perjanjian ini dan total jam kerja normal dalam 1 minggu adalah 40 jam.',
                                    'description28':'(3) Ketentuan waktu kerja ini dapat berubah sewaktu-waktu sesuai dengan kebutuhan PIHAK KESATU. Setiap perubahan tentang waktu kerja akan diberitahukan kepada PIHAK KEDUA dan bersifat mengikat.',
                                    'description29':'(1) Perjanjian ini tunduk pada Peraturan Perundangan Tentang Ketenagakerjaan di Indonesia.',
                                    'description30':'(2) PIHAK KEDUA setuju untuk patuh kepada segala peraturan dan tata tertib yang berlaku pada perusahaan PIHAK KESATU, dan taat pada tatanan hukum yang berlaku di Negara Republik Indonesia.',
                                    'description31':'(3) PIHAK KEDUA tidak berhak dan dilarang keras menyebarkan semua data dan/atau informasi yang bersifat rahasia dalam bentuk dan alasan apapun seperti dan tidak terbatas pada keterangan pelanggan, pemasok, formula, contoh barang, rencana kerja, metode dan rahasia dagang, yang diketahuinya baik secara langsung, maupun tidak langsung sehubungan dengan pekerjaannya kepada pihak lain tanpa seizin tertulis dari PIHAK KESATU, baik selama Perjanjian ini berlangsung, maupun 60 (enam puluh) bulan setelah berakhirnya jangka waktu Perjanjian ini.',
                                    'description32':'(1) PIHAK KESATU berhak secara sepihak mengakhiri Perjanjian ini setiap waktu, jika terjadi hal-hal sebagaimana disebutkan di bawah ini:',
                                    'description33':'a. PIHAK KEDUA secara berturut-turut selama 5 (lima) hari telah meninggalkan pekerjaannya tanpa pemberitahuan secara tertulis dan tanpa alasan yang dapat dipertanggungjawabkan.',
                                    'description34':'b. PIHAK KEDUA dijatuhi hukuman oleh Instansi yang berwajib karena tindakan kriminal yang dilakukan.',
                                    'description35':'c. PIHAK KEDUA meninggal dunia, mengalami gangguan kesehatan kronis atau berada dalam penanganan dokter karena gangguan kesehatan kronis.',
                                    'description36':'d. PIHAK KEDUA tidak cakap melakukan pekerjaannya walaupun sudah diberi peringatan.',
                                    'description37':'e. Pada saat kesepakatan kerja diadakan, PIHAK KEDUA memberikan keterangan palsu atau dipalsukan.',
                                    'description38':'f. Apabila PIHAK KEDUA melakukan pelanggaran ringan dan telah diberikan 3 (tiga) kali surat peringatan, namun tidak memperbaiki diri.',
                                    'description39':'(2) Apabila, karena satu dan lain hal Perjanjian ini berakhir sebagaimana disebutkan dalam Pasal 3 ayat (4), Pasal 5 ayat (3), Pasal 6 ayat (1) Perjanjian ini,  maka PIHAK KEDUA harus mengembalikan fasilitas dan sarana penunjang yang diberikan oleh perusahaan sebagaimana disebutkan pada Lampiran 1 Perjanjian ini.',
                                    'description40':'(3) Pada saat  Perjanjian ini berakhir, PIHAK KEDUA wajib menyerahkan seluruh catatan, memorandum, surat-menyurat dan dokumen lain serta barang-barang milik perusahaan, baik secara fisik maupun data digital, kecuali hasil penelitian-penelitian serta tulisan-tulisan ilmiah yang dibuat oleh PIHAK KEDUA selama jangka waktu berlakunya Perjanjian ini yang merupakan hak cipta pribadi dari PIHAK KEDUA.  PIHAK KEDUA tidak akan menahan salinan dari dokumen-dokumen milik perusahaan serta tidak akan mempergunakannya untuk kepentingan sendiri dan atau untuk orang/pihak lain.',
                                    'description41':'(4) Apabila Perjanjian ini berakhir karena alasan-alasan sebagaimana tersebut dalam Pasal 5 ayat (3) dan Pasal  6 ayat (1) Perjanjian ini, PIHAK KEDUA tidak lagi mempunyai hubungan kerja atau kaitan apapun dengan PIHAK KESATU, dan oleh karenanya PIHAK KEDUA tidak akan mengajukan segala tuntutan, klaim, gugatan dan ganti rugi dalam bentuk apapun kepada PIHAK KESATU sehubungan dengan berakhirnya hubungan kerja tersebut dan/ atau Perjanjian ini.',
                                    'description42':'(5) Apabila masa berlakunya Perjanjian ini telah selesai atau sekalipun diperpanjang dan berakhir pula masa berlakunya, maka hubungan kerja PIHAK KESATU dengan PIHAK KEDUA putus dengan sendirinya, kecuali PARA PIHAK menginginkan perpanjangan masa Perjanjian ini.',
                                    'description43':'(6) PIHAK KESATU tidak berhak membayar kewajiban dalam bentuk apapun kepada PIHAK KEDUA bilamana jangka waktu Perjanjian ini berakhir, termasuk jika terdapat perpanjangan atau perubahan terhadap Perjanjian ini, kecuali upah PIHAK KEDUA pada bulan berjalan.',
                                    'description44':'(1) Perjanjian ini ditafsirkan, tunduk dan diatur serta dilaksanakan menurut Hukum Negara Republik Indonesia.',
                                    'description45':'(2) Perjanjian ini tidak dapat diubah atau dimodifikasi kecuali dengan persetujuan tertulis bersama PARA PIHAK.',
                                    'description46':'(3) Kecuali disetujui secara tegas dalam suatu dokumen terpisah, Perjanjian ini menggantikan semua perjanjian dan kesepakatan lain yang ada dan atau telah dibuat sebelum tanggal penjanjian ini, baik tertulis maupun tidak tertulis, yang dibuat oleh PARA PIHAK mengenai pokok masalah yang sama.',
                                    'description47':'(4) Jika ada salah satu atau lebih ketentuan Perjanjian ini dinyatakan atau menjadi tidak sah atau tidak dapat dilaksanakan, maka tidak absahnya atau tidak dapat dilaksanakannya ketentuan-ketentuan tersebut tidak akan mempengaruhi keabsahan Perjanjian ini secara keseluruhan dan dapat dilaksanakannya ketentuan lainnya dari Perjanjian ini. PARA PIHAK wajib untuk mengganti ketentuan yang dinyatakan atau menjadi tidak sah atau tidak dapat dilaksanakan tersebut dengan ketentuan lain yang sah yang dapat dilaksanakan yang memiliki maksud dan pengertian yang terdekat dengan ketentuan yang digantikan tersebut.',
                                    'description48':'(5) Judul Perjanjian ini dan setiap pasal-pasal yang terkandung di dalamnya dinyatakan demikian untuk maksud kemudahan saja dan tidak akan mempengaruhi penafsiran dari perjanjian dan masing-masing pasal yang bersangkutan. ',
                                    'description49':'(1) Setiap pemberitahuan atau komunikasi yang menyangkut Perjanjian ini wajib dilakukan secara tertulis dalam bahasa Indonesia dan diserahkan langsung atau dengan jasa kurir atau fax atau email yang dialamatkan kepada:',
                                    'description50':'(2) Perubahan atas nama, alamat, telepon, fax, atau email yang tercantum dalam ayat (1) wajib diberitahukan kepada PIHAK lainnya dalam waktu 7 (tujuh) hari kerja setelah perubahan tersebut efektif.',
                                    'description51':'(3) Segala macam perselisihan yang mungkin timbul dalam perjanjian ini atau dalam pelaksanaannya akan diselesaikan secara musyawarah mufakat terlebih dahulu dengan atasan langsung dan/ atau pimpinan perusahaan yang diwakilkan.',
                                    'description52':'(4) Apabila dalam tahap penyelesaian dengan atasan langsung tersebut belum juga terselesaikan, maka perselisihan dan perbedaan pendapat tersebut dapat diajukan secara tertulis kepada pimpinan perusahaan guna dicarikan jalan keluar yang layak dan adil sesuai kondisi yang berlaku secara umum serta mengacu kepada ketentuan perundang-undangan yang berlaku.',
                                    'description53':'(5) Apabila penyelesaian sebagaimana termaksud dalam Pasal 8 ayat (4) Perjanjian ini tidak berlangsung, maka PARA PIHAK sepakat meminta penyelesaiannya kepada kantor Departemen Tenaga Kerja setempat.',
                                    'description54':'Demikian Perjanjian ini dibuat, ditandatangani pada hari dan tanggal sebagaimana disebutkan pada awal Perjanjian ini dibuat tanpa ada paksaan dari siapapun dan dibuat dalam keadaan sadar, sehat jasmani dan rohani. Setelah dibaca dan dipahami serta disetujui isinya yang kemudian ditandatangani oleh PARA PIHAK, dalam rangkap 2, yang sama isi dan ketentuan hukumnya, masing-masing untuk PARA PIHAK, dan diberlakukan pada hari dan tanggal sebagaimana disebutkan terlebih dahulu di bagian depan Perjanjian ini.',
                              ##tenaga ahli
                                    'description_ta':'Perjanjian Pelayanan Jasa ini (untuk selanjutnya disebut "Perjanjian"), dibuat dan ditandatangani di Jakarta pada hari Jumat tanggal 19 bulan Mei tahun dua ribu tujuh belas (19- 5 - 2017) oleh dan antara PIHAK-PIHAK sebagai berikut :',           
                                    'description_ta2':'1. PT. IMMOBI SOLUSI PRIMA, berkedudukan di Gedung Tifa, lantai 8 suite 803, Jalan Kuningan Barat No.26, Jakarta Selatan-12710, didirikan menurut hukum negara Republik Indonesia berdasarkan Akta Pendirian No.03 tanggal 8 September 2014, yang dibuat oleh/di hadapan Dwi Yulianti, S.H., Notaris di Jakarta Selatan, dan telah mendapatkan pengesahan sebagai Badan Hukum melalui Surat Keputusan Menteri Hukum Dan Hak Asasi Manusia Republik Indonesia No. AHU-27695.40.10.2014 tanggal 2 Oktober 2014, dan terakhir telah mengalami perubahan melalui Akta No.05 tanggal 10 Maret 2016 yang dibuat oleh/di hadapan Notaris yang sama tersebut. Dalam hal ini diwakili oleh Asiyah dalam jabatannya selaku Head Of HR & GA, dengan demikian sah bertindak atas nama dan untuk kepentingan PT. Immobi Solusi Prima. Untuk selanjutnya disebut "PIHAK PERTAMA".',
                                    'description_ta3':'Dalam hal ini bertindak atas nama dan untuk kepentingan diri sendiri. Untuk selanjutnya disebut "PIHAK KEDUA"',
                                    'description_ta4':'Dengan ini PARA PIHAK telah sepakat untuk membuat, menandatangani dan melaksanakan Perjanjian ini dengan syarat-syarat dan ketentuan-ketentuan sebagaimana berikut :',
                                    'description_ta5':'tempat/kedudukan lain dari lokasi kerja atau lokasi project perusahaan, maupun mengubah tugas dan tanggung jawab nya, dan oleh karenanya PIHAK KEDUA bersedia untuk dipindahkan ke tempat/kedudukan lain dari lokasi kerja atau lokasi project perusahaan, maupun diubah tugas dan tanggung jawabnya sesuai kebutuhan PIHAK PERTAMA.',
                                    'description_ta6':'Mei (05) dua ribu tujuh belas (2017) dan akan berakhir pada tanggal Dua  Puluh Delapan   (28) Agustus  (08) dua ribu tujuh belas (2017). ',
                                    'description_ta7':'Perjanjian ini, yang merupakan satu kesatuan dan menjadi bagian yang tak terpisahkan dalam perjanjian ini;',
                                    'description_ta8':'perjanjian ini, yang dibayarkan berdasarkan sistem reimbursement atas dasar bukti-bukti pembayaran asli dan resmi;',
                                    })
        return

class contract_template_line(osv.osv):
    _name='contract.template.line'
    _columns={'contract_template_id':fields.many2one('contract.template','Template Line'),
              'name':fields.char('Name'),
              }
    
        
class hr_contract_template(osv.osv): 
    _inherit='hr.contract'
    _columns={
    'name':fields.char('Contract Template Name',index=True, copy=False, ),
    'description': fields.text('Description', ),
    'description2': fields.text('Description2', ),
    'description3': fields.text('Description3', ),
    'description4': fields.text('Description4', ),
    'description5': fields.text('Description4', ),
    'description6': fields.text('Description4', ),
    'description7': fields.text('Description4', ),
    'description8': fields.text('Description4', ),
    'description9': fields.text('Description4', ),
    'description10': fields.text('Description4', ),
    'description11': fields.text('Description4', ),
    'description12': fields.text('Description4', ),
    'description13': fields.text('Description4', ),
    'description14': fields.text('Description4', ),
    'description15': fields.text('Description4', ),
    'description16': fields.text('Description4', ),
    'description17': fields.text('Description4', ),
    'description18': fields.text('Description4', ),
    'description19': fields.text('Description4', ),
    'description20': fields.text('Description4', ),
    'description21': fields.text('Description4', ),
    'description22': fields.text('Description4', ),
    'description23': fields.text('Description4', ),
    'description24': fields.text('Description4', ),
    'description25': fields.text('Description4', ),
    'description26': fields.text('Description4', ),
    'description27': fields.text('Description4', ),
    'description28': fields.text('Description4', ),
    'description29': fields.text('Description4', ),
    'description30': fields.text('Description4', ),
    'description31': fields.text('Description4', ),
    'description32': fields.text('Description4', ),
    'description33': fields.text('Description4', ),
    'description34': fields.text('Description4', ),
    'description35': fields.text('Description4', ),
    'description36': fields.text('Description4', ),
    'description37': fields.text('Description4', ),
    'description38': fields.text('Description4', ),
    'description39': fields.text('Description4', ),
    'description40': fields.text('Description4', ),
    'description41': fields.text('Description4', ),
    'description42': fields.text('Description4', ),
    'description43': fields.text('Description4', ),
    'description44': fields.text('Description4', ),
    'description45': fields.text('Description4', ),
    'description46': fields.text('Description4', ),
    'description47': fields.text('Description4', ),
    'description48': fields.text('Description4', ),
    'description49': fields.text('Description4', ),
    'description50': fields.text('Description4', ),
    'description51': fields.text('Description4', ),
    'description52': fields.text('Description4', ),
    'description53': fields.text('Description4', ),
    'description54': fields.text('Description4', ),
    'description55': fields.text('Description4', ),
    'description56': fields.text('Description4', ),
##tenaga ahli
    'description_ta': fields.text('Description', ),
    'description_ta2': fields.text('Description2', ),
    'description_ta3': fields.text('Description3', ),
    'description_ta4': fields.text('Description4', ),
    'description_ta5': fields.text('Description4', ),
    'description_ta6': fields.text('Description4', ),
    'description_ta7': fields.text('Description4', ),
    'description_ta8': fields.text('Description4', ),
    }
    
    _defaults={'description':'Perjanjian Kerja Waktu Tertentu ini (untuk \
                                            selanjutnya disebut "Perjanjian"), dibuat dan \
                                            ditandatangani di Jakarta pada hari Selasa \
                                            tanggal 1 Febuari 2017 oleh dan antara \
                                            PIHAK-PIHAK berikut ini:', 
                                      'description2':'I. PT IMMOBI SOLUSI PRIMA',
                                      'description3':'Suatu Perseroan Terbatas, didirikan pada tanggal 8-9-2014,\
                                              berdasarkan Akta Pendirian No. 3 Notaris Dwi Yulianti, S.H., di Jakarta, telah \
                                              disahkan dengan  Surat Keputusan  Menteri Hukum Dan HAM Republik Indonesia Hukum \
                                               dan HAM RI No. AHU-0101404.40.80.2014 Tahun 2014, berkedudukan di Gedung Tifa, \
                                               Lantai 8 Jalan Kuningan Barat No. 26, Jakarta 12710, dalam hal ini diwakili oleh \
                                               Heksantono Hartadi  dengan jabatan Direktur Utama pada PT. Immobi Solusi Prima, \
                                               dengan demikian sah dan berwenang bertindak untuk dan atas nama PT Immobi Solusi Prima,\
                                                selanjutnya disebut  "PIHAK KESATU";',
                                    'description4':'Dalam hal ini bertindak untuk diri sendiri, selanjutnya disebut  "PIHAK KEDUA"', 
                                    'description5':'Untuk  secara bersama-sama disebut "PARA PIHAK"',
                                    'description6':'PARA PIHAK telah sepakat untuk mengadakan hubungan kerja waktu tertentu dengan ketentuan sebagaimana tersebut dalam pasal-pasal berikut:',
                                    'description7':'PIHAK KESATU mengadakan ikatan kerja dengan PIHAK KEDUA, untuk masa waktu tertentu selama ',
                                    'description8':'(1) PIHAK KESATU akan menempatkan PIHAK KEDUA di lokasi kerja PIHAK PERTAMA, beralamat di Gedung Tifa Lt.8, Jl.Kuningan Barat kav.26 sebagai',     
                                    'description9':'(2) PIHAK KESATU berdasarkan pertimbangan tertentu berhak memindahkan ke bagian lain dan atau \
                                                    mengubah nama jabatan PIHAK KEDUA, dan karenanya PIHAK KEDUA bersedia untuk',
                                    'description10':'dipindahkan ke bagian lain dan atau diubah nama jabatannya sesuai kebutuhan PIHAK KESATU, dengan',                
                                    'description11':'pemberitahuan tertulis dari PIHAK KESATU kepada PIHAK KEDUA.' ,
                                    'description12':'(1) Selama perjanjian berlangsung, PIHAK KEDUA berhak untuk memperoleh:',
                                    'description13':'a. Gaji dan fasilitas dari PIHAK KESATU sebagaimana tercantum pada Lampiran 1 Perjanjian ini, merupakan kesatuan dan menjadi bagian yang tak terpisahkan dengan Perjanjian ini.',
                                    'description14':'b. Sarana pendukung dari PIHAK KESATU untuk menunjang Jenis Pekerjaan sebagaimana disebutkan dalam Pasal 2 ayat (1) Perjanjian ini, dan ditetapkan dalam Lampiran 1 Perjanjian ini yang merupakan kesatuan dan menjadi bagian yang tak terpisahkan dengan  Perjanjian ini.',
                                    'description15':'c. Akses kepada karyawan, data, informasi pada lingkungan perusahaan PIHAK KESATU terkait Jenis Pekerjaan sebagaimana disebutkan dalam Pasal 2 ayat (1) Perjanjian ini',
                                    'description16':'(2) Selama jangka waktu perjanjian sebagaimana tersebut dalam Pasal 1 Perjanjian ini , PIHAK KEDUA berkewajiban untuk: ',
                                    'description17':'a. Melaksanakan tugas dan kewajiban umum sesuai dengan kebijakan perusahaan, yakni:',
                                    'description18':'i. Melaksanakan tugas dengan sebaik-baiknya serta berusaha semaksimal mungkin ditujukan untuk kepentingan dan kemajuan perusahaan;',
                                    'description19':'ii. Memberikan dan menyampaikan segala gagasan, masukan, informasi, dan atau laporan yang dianggap penting dan relevan untuk kemajuan perusahaan;',
                                    'description20':'b. Melaksanakan tugas dan kewajiban khusus sebagaimana ditetapkan dalam Lampiran 2, Perjanjian ini, yang merupakan kesatuan dan menjadi bagian tak terpisahkan dalam Perjanjian ini.',
                                    'description21':'c. Mencurahkan waktu, perhatian dan kemampuannya pada perusahaan dan hal-hal lain yang menyangkut kepentingan perusahaan',
                                    'description22':'d. Terikat untuk tetap mandiri dari semua pihak dan bertindak untuk menjaga kepentingan perusahaan.',
                                    'description23':'e. Tidak terlibat baik secara langsung maupun tidak langsung dalam usaha maupun jabatan lain yang sejenis dengan Jenis Pekerjaan sebagaimana disebutkan dalam Pasal 2 ayat (1) Perjanjian ini.',
                                    'description24':'(3) PARA PIHAK mengadakan evaluasi setiap 3 (tiga) bulan atas kinerja dan realisasi dari pekerjaan dan tanggung jawab  yang telah ditetapkan pada Lampiran 2  Perjanjian ini.',
                                    'description25':'(4) Apabila hasil evaluasi yang tersebut dalam Pasal 3 ayat (3) Perjanjian ini PIHAK KEDUA tidak dapat meneruskan Perjanjian ini, maka PIHAK KEDUA dapat mengajukan permintaan untuk mengundurkan diri secara sukarela dengan tanpa memperoleh penggantian apapun dari PIHAK KESATU, dengan pemberitahuan tertulis paling lambat  30 hari  sebelum tanggal pengunduran diri.',
                                    'description26':'(1) Hari Kerja normal adalah Senin sampai dengan Jumat, kecuali diperjanjikan lain sebagaimana pada Lampiran 2 Perjanjian ini.',
                                    'description27':'(2) Jam kerja normal dimulai jam 08.30 sampai dengan jam 17.30, dengan waktu istirahat maksimal 1 jam, kecuali diperjanjikan lain sebagaimana disebutkan dalam Lampiran 2 Perjanjian ini dan total jam kerja normal dalam 1 minggu adalah 40 jam.',
                                    'description28':'(3) Ketentuan waktu kerja ini dapat berubah sewaktu-waktu sesuai dengan kebutuhan PIHAK KESATU. Setiap perubahan tentang waktu kerja akan diberitahukan kepada PIHAK KEDUA dan bersifat mengikat.',
                                    'description29':'(1) Perjanjian ini tunduk pada Peraturan Perundangan Tentang Ketenagakerjaan di Indonesia.',
                                    'description30':'(2) PIHAK KEDUA setuju untuk patuh kepada segala peraturan dan tata tertib yang berlaku pada perusahaan PIHAK KESATU, dan taat pada tatanan hukum yang berlaku di Negara Republik Indonesia.',
                                    'description31':'(3) PIHAK KEDUA tidak berhak dan dilarang keras menyebarkan semua data dan/atau informasi yang bersifat rahasia dalam bentuk dan alasan apapun seperti dan tidak terbatas pada keterangan pelanggan, pemasok, formula, contoh barang, rencana kerja, metode dan rahasia dagang, yang diketahuinya baik secara langsung, maupun tidak langsung sehubungan dengan pekerjaannya kepada pihak lain tanpa seizin tertulis dari PIHAK KESATU, baik selama Perjanjian ini berlangsung, maupun 60 (enam puluh) bulan setelah berakhirnya jangka waktu Perjanjian ini.',
                                    'description32':'(1) PIHAK KESATU berhak secara sepihak mengakhiri Perjanjian ini setiap waktu, jika terjadi hal-hal sebagaimana disebutkan di bawah ini:',
                                    'description33':'a. PIHAK KEDUA secara berturut-turut selama 5 (lima) hari telah meninggalkan pekerjaannya tanpa pemberitahuan secara tertulis dan tanpa alasan yang dapat dipertanggungjawabkan.',
                                    'description34':'b. PIHAK KEDUA dijatuhi hukuman oleh Instansi yang berwajib karena tindakan kriminal yang dilakukan.',
                                    'description35':'c. PIHAK KEDUA meninggal dunia, mengalami gangguan kesehatan kronis atau berada dalam penanganan dokter karena gangguan kesehatan kronis.',
                                    'description36':'d. PIHAK KEDUA tidak cakap melakukan pekerjaannya walaupun sudah diberi peringatan.',
                                    'description37':'e. Pada saat kesepakatan kerja diadakan, PIHAK KEDUA memberikan keterangan palsu atau dipalsukan.',
                                    'description38':'f. Apabila PIHAK KEDUA melakukan pelanggaran ringan dan telah diberikan 3 (tiga) kali surat peringatan, namun tidak memperbaiki diri.',
                                    'description39':'(2) Apabila, karena satu dan lain hal Perjanjian ini berakhir sebagaimana disebutkan dalam Pasal 3 ayat (4), Pasal 5 ayat (3), Pasal 6 ayat (1) Perjanjian ini,  maka PIHAK KEDUA harus mengembalikan fasilitas dan sarana penunjang yang diberikan oleh perusahaan sebagaimana disebutkan pada Lampiran 1 Perjanjian ini.',
                                    'description40':'(3) Pada saat  Perjanjian ini berakhir, PIHAK KEDUA wajib menyerahkan seluruh catatan, memorandum, surat-menyurat dan dokumen lain serta barang-barang milik perusahaan, baik secara fisik maupun data digital, kecuali hasil penelitian-penelitian serta tulisan-tulisan ilmiah yang dibuat oleh PIHAK KEDUA selama jangka waktu berlakunya Perjanjian ini yang merupakan hak cipta pribadi dari PIHAK KEDUA.  PIHAK KEDUA tidak akan menahan salinan dari dokumen-dokumen milik perusahaan serta tidak akan mempergunakannya untuk kepentingan sendiri dan atau untuk orang/pihak lain.',
                                    'description41':'(4) Apabila Perjanjian ini berakhir karena alasan-alasan sebagaimana tersebut dalam Pasal 5 ayat (3) dan Pasal  6 ayat (1) Perjanjian ini, PIHAK KEDUA tidak lagi mempunyai hubungan kerja atau kaitan apapun dengan PIHAK KESATU, dan oleh karenanya PIHAK KEDUA tidak akan mengajukan segala tuntutan, klaim, gugatan dan ganti rugi dalam bentuk apapun kepada PIHAK KESATU sehubungan dengan berakhirnya hubungan kerja tersebut dan/ atau Perjanjian ini.',
                                    'description42':'(5) Apabila masa berlakunya Perjanjian ini telah selesai atau sekalipun diperpanjang dan berakhir pula masa berlakunya, maka hubungan kerja PIHAK KESATU dengan PIHAK KEDUA putus dengan sendirinya, kecuali PARA PIHAK menginginkan perpanjangan masa Perjanjian ini.',
                                    'description43':'(6) PIHAK KESATU tidak berhak membayar kewajiban dalam bentuk apapun kepada PIHAK KEDUA bilamana jangka waktu Perjanjian ini berakhir, termasuk jika terdapat perpanjangan atau perubahan terhadap Perjanjian ini, kecuali upah PIHAK KEDUA pada bulan berjalan.',
                                    'description44':'(1) Perjanjian ini ditafsirkan, tunduk dan diatur serta dilaksanakan menurut Hukum Negara Republik Indonesia.',
                                    'description45':'(2) Perjanjian ini tidak dapat diubah atau dimodifikasi kecuali dengan persetujuan tertulis bersama PARA PIHAK.',
                                    'description46':'(3) Kecuali disetujui secara tegas dalam suatu dokumen terpisah, Perjanjian ini menggantikan semua perjanjian dan kesepakatan lain yang ada dan atau telah dibuat sebelum tanggal penjanjian ini, baik tertulis maupun tidak tertulis, yang dibuat oleh PARA PIHAK mengenai pokok masalah yang sama.',
                                    'description47':'(4) Jika ada salah satu atau lebih ketentuan Perjanjian ini dinyatakan atau menjadi tidak sah atau tidak dapat dilaksanakan, maka tidak absahnya atau tidak dapat dilaksanakannya ketentuan-ketentuan tersebut tidak akan mempengaruhi keabsahan Perjanjian ini secara keseluruhan dan dapat dilaksanakannya ketentuan lainnya dari Perjanjian ini. PARA PIHAK wajib untuk mengganti ketentuan yang dinyatakan atau menjadi tidak sah atau tidak dapat dilaksanakan tersebut dengan ketentuan lain yang sah yang dapat dilaksanakan yang memiliki maksud dan pengertian yang terdekat dengan ketentuan yang digantikan tersebut.',
                                    'description48':'(5) Judul Perjanjian ini dan setiap pasal-pasal yang terkandung di dalamnya dinyatakan demikian untuk maksud kemudahan saja dan tidak akan mempengaruhi penafsiran dari perjanjian dan masing-masing pasal yang bersangkutan. ',
                                    'description49':'(1) Setiap pemberitahuan atau komunikasi yang menyangkut Perjanjian ini wajib dilakukan secara tertulis dalam bahasa Indonesia dan diserahkan langsung atau dengan jasa kurir atau fax atau email yang dialamatkan kepada:',
                                    'description50':'(2) Perubahan atas nama, alamat, telepon, fax, atau email yang tercantum dalam ayat (1) wajib diberitahukan kepada PIHAK lainnya dalam waktu 7 (tujuh) hari kerja setelah perubahan tersebut efektif.',
                                    'description51':'(3) Segala macam perselisihan yang mungkin timbul dalam perjanjian ini atau dalam pelaksanaannya akan diselesaikan secara musyawarah mufakat terlebih dahulu dengan atasan langsung dan/ atau pimpinan perusahaan yang diwakilkan.',
                                    'description52':'(4) Apabila dalam tahap penyelesaian dengan atasan langsung tersebut belum juga terselesaikan, maka perselisihan dan perbedaan pendapat tersebut dapat diajukan secara tertulis kepada pimpinan perusahaan guna dicarikan jalan keluar yang layak dan adil sesuai kondisi yang berlaku secara umum serta mengacu kepada ketentuan perundang-undangan yang berlaku.',
                                    'description53':'(5) Apabila penyelesaian sebagaimana termaksud dalam Pasal 8 ayat (4) Perjanjian ini tidak berlangsung, maka PARA PIHAK sepakat meminta penyelesaiannya kepada kantor Departemen Tenaga Kerja setempat.',
                                    'description54':'Demikian Perjanjian ini dibuat, ditandatangani pada hari dan tanggal sebagaimana disebutkan pada awal Perjanjian ini dibuat tanpa ada paksaan dari siapapun dan dibuat dalam keadaan sadar, sehat jasmani dan rohani. Setelah dibaca dan dipahami serta disetujui isinya yang kemudian ditandatangani oleh PARA PIHAK, dalam rangkap 2, yang sama isi dan ketentuan hukumnya, masing-masing untuk PARA PIHAK, dan diberlakukan pada hari dan tanggal sebagaimana disebutkan terlebih dahulu di bagian depan Perjanjian ini.',
                              ##tenaga ahli
                                    'description_ta':'Perjanjian Pelayanan Jasa ini (untuk selanjutnya disebut "Perjanjian"), dibuat dan ditandatangani di Jakarta pada hari Jumat tanggal 19 bulan Mei tahun dua ribu tujuh belas (19- 5 - 2017) oleh dan antara PIHAK-PIHAK sebagai berikut :',           
                                    'description_ta2':'1. PT. IMMOBI SOLUSI PRIMA, berkedudukan di Gedung Tifa, lantai 8 suite 803, Jalan Kuningan Barat No.26, Jakarta Selatan-12710, didirikan menurut hukum negara Republik Indonesia berdasarkan Akta Pendirian No.03 tanggal 8 September 2014, yang dibuat oleh/di hadapan Dwi Yulianti, S.H., Notaris di Jakarta Selatan, dan telah mendapatkan pengesahan sebagai Badan Hukum melalui Surat Keputusan Menteri Hukum Dan Hak Asasi Manusia Republik Indonesia No. AHU-27695.40.10.2014 tanggal 2 Oktober 2014, dan terakhir telah mengalami perubahan melalui Akta No.05 tanggal 10 Maret 2016 yang dibuat oleh/di hadapan Notaris yang sama tersebut. Dalam hal ini diwakili oleh Asiyah dalam jabatannya selaku Head Of HR & GA, dengan demikian sah bertindak atas nama dan untuk kepentingan PT. Immobi Solusi Prima. Untuk selanjutnya disebut "PIHAK PERTAMA".',
                                    'description_ta3':'Dalam hal ini bertindak atas nama dan untuk kepentingan diri sendiri. Untuk selanjutnya disebut "PIHAK KEDUA"',
                                    'description_ta4':'Dengan ini PARA PIHAK telah sepakat untuk membuat, menandatangani dan melaksanakan Perjanjian ini dengan syarat-syarat dan ketentuan-ketentuan sebagaimana berikut :',
                                    'description_ta5':'tempat/kedudukan lain dari lokasi kerja atau lokasi project perusahaan, maupun mengubah tugas dan tanggung jawab nya, dan oleh karenanya PIHAK KEDUA bersedia untuk dipindahkan ke tempat/kedudukan lain dari lokasi kerja atau lokasi project perusahaan, maupun diubah tugas dan tanggung jawabnya sesuai kebutuhan PIHAK PERTAMA.',
                                    'description_ta6':'Mei (05) dua ribu tujuh belas (2017) dan akan berakhir pada tanggal Dua  Puluh Delapan   (28) Agustus  (08) dua ribu tujuh belas (2017). ',
                                    'description_ta7':'Perjanjian ini, yang merupakan satu kesatuan dan menjadi bagian yang tak terpisahkan dalam perjanjian ini;',
                                    'description_ta8':'perjanjian ini, yang dibayarkan berdasarkan sistem reimbursement atas dasar bukti-bukti pembayaran asli dan resmi;',
                                    }
    
class res_company(osv.osv):
    _inherit="res.company"
    
    _columns={'logo_header_immobi':fields.binary('Logo Header Immobi'),}