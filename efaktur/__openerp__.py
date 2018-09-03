{
    "name"          : "E-Faktur",
    "version"       : "8.0",
    'license'       : 'AGPL-3',
    "depends"       : ["account"],
    'external_dependencies': {'python': ['xlwt']},
    'images'        : ['static/description/main_screenshot.jpg'],
    "author"        : "Alphasoft",
    "description"   : """This module aim to:
                    - Create Object Nomor Faktur Pajak
                    - Add Column Customer such as: 
                        * NPWP, RT, RW, Kelurahan, Kecamatan, Kabupaten, Province
                    - Just Import the file csv at directory data
                    - Export file csv for upload to efaktur""",
    "website"       : "https://www.alphasoft.co.id/",
    "category"      : "Accounting",
    "data"    : [
                "security/ir.model.access.csv",
                "data/res_country_data.xml",
                "base_view.xml",
                "res_partner_view.xml",
                "faktur_pajak_view.xml",
                "account_invoice_view.xml",
                "wizard/faktur_pajak_generate.xml",
                "report/efaktur_invoice_csv_view.xml",
    ],
    'price'         : 189.00,
    'currency'      : 'EUR',
    "init_xml"      : [],
    "demo_xml"      : [],
    'test'          : [],    
    "active"        : False,
    "installable"   : True,
    'live_test_url': 'https://efaktur.ju-san.net:9000/'
}