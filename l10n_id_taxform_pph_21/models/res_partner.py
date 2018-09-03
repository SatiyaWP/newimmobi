# -*- coding: utf-8 -*-
# Copyright 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, api, fields
from openerp.tools.translate import _


class ResPartner(models.Model):
    _inherit = "res.partner"

    ptkp_category_id = fields.Many2one(
        string="PTKP Category",
        comodel_name="l10n_id.ptkp_category",
    )

    @api.multi
    def compute_pph_21_2110001(
            self,
            period_amount=1,
            tanggal_pemotongan=False,
            gaji=0.0,
            tunjangan_pph=0.0,
            tunjangan_lain=0.0,
            jumlah_penghasilan_non_rutin=0.0,
            pensiun=0.0,
            jht=0.0,
    ):
        self.ensure_one()
        result = {
            "biaya_jabatan_rutin": 0.0,
            "biaya_jabatan_non_rutin": 0.0,
            "biaya_jabatan": 0.0,
            "pengurang": 0.0,
            "penghasilan_bruto_rutin_setahun": 0.0,
            "penghasilan_bruto_non_rutin_setahun": 0.0,
            "penghasilan_bruto_setahun": 0.0,
            "ptkp": 0.0,
            "pkp_rutin_setahun": 0.0,
            "pkp_setahun": 0.0,
            "pph_rutin_setahun": 0.0,
            "pph_non_rutin_setahun": 0.0,
            "pph_setahun": 0.0,
            "pph": 0.0,
            "pph_ta": 0.0,
        }
        ptkp_category = self.ptkp_category_id
        if not ptkp_category:
            raise models.ValidationError(
                _("Partner's PTKP Category is not configured"))

        jumlah_penghasilan_rutin = gaji + \
            tunjangan_pph + tunjangan_lain
        bruto_rutin_setahun = jumlah_penghasilan_rutin * period_amount
        bruto_non_rutin_setahun = bruto_rutin_setahun + jumlah_penghasilan_non_rutin
        
        obj_biaya_jabatan = self.env["l10n_id.pph_21_biaya_jabatan"]
        try:
            obj_biaya_jabatan_id = obj_biaya_jabatan.find(tanggal_pemotongan)
            perhitungan_biaya_jabatan = obj_biaya_jabatan.find(
                tanggal_pemotongan).get_biaya_jabatan(
                bruto_rutin_setahun,
                jumlah_penghasilan_non_rutin,
                period_amount,
            )
            biaya_jabatan_rutin = perhitungan_biaya_jabatan["biaya_jabatan_rutin"]
            biaya_jabatan_non_rutin = perhitungan_biaya_jabatan["biaya_jabatan_non_rutin"]
        except:
            biaya_jabatan_rutin = 0.0
            biaya_jabatan_non_rutin = 0.0
#         biaya_jabatan = perhitungan_biaya_jabatan["biaya_jabatan"]

        pengurang_rutin_setahun = biaya_jabatan_rutin + pensiun * period_amount + jht * period_amount
        pengurang_non_rutin_setahun = biaya_jabatan_non_rutin + pensiun * period_amount + jht * period_amount
        
        neto_rutin_setahun = bruto_rutin_setahun - pengurang_rutin_setahun
        neto_non_rutin_setahun = bruto_non_rutin_setahun - pengurang_non_rutin_setahun
        
        if gaji > 0.0:
            ptkp = ptkp_category.get_rate(tanggal_pemotongan)
        else:
            ptkp = 0.0
        
        pkp_rutin_setahun = neto_rutin_setahun - ptkp
        pkp_non_rutin_setahun = neto_non_rutin_setahun - ptkp
        
        obj_pph = self.env["l10n_id.pph_21_rate"]
        pph_setahun_rutin = obj_pph.find(tanggal_pemotongan).compute_tax(pkp_rutin_setahun)
        pph_setahun_non_rutin = obj_pph.find(tanggal_pemotongan).compute_tax(pkp_non_rutin_setahun)
        
        npwp = self.npwp or False
        if not npwp:
            obj_multiplier = self.env["l10n_id.pph_21_npwp_rate_modifier"]
            pph_setahun_rutin = (obj_multiplier.get_rate(tanggal_pemotongan) / 100.00) * pph_setahun_rutin
            pph_setahun_non_rutin = (obj_multiplier.get_rate(tanggal_pemotongan) / 100.00) * pph_setahun_non_rutin
        pph_setahun_rutin = float(int(pph_setahun_rutin))
        pph_setahun_non_rutin = float(int(pph_setahun_non_rutin))
        pph_non_rutin = pph_setahun_non_rutin - pph_setahun_rutin
        pph_rutin = pph_setahun_rutin / period_amount
        pph = pph_rutin + pph_non_rutin
        
        # hitung pph tenaga ahli
        dpp = gaji / 2
        pkp_ta = dpp - ptkp / 12
        akumulasi_pkp_ta = pkp_ta * period_amount
        obj_pph = self.env["l10n_id.pph_21_rate"]
        pph_ta_rate = obj_pph.find(tanggal_pemotongan).compute_rate(akumulasi_pkp_ta)
        pph_ta = pkp_ta * pph_ta_rate / 100
        
        result["biaya_jabatan_rutin"] = biaya_jabatan_rutin
        result["biaya_jabatan_non_rutin"] = biaya_jabatan_non_rutin
#         result["biaya_jabatan"] = biaya_jabatan
#         result["pengurang"] = pengurang
#         result["netto"] = netto
#         result["netto_setahun"] = netto_setahun
        result["ptkp"] = ptkp
#         result["pkp"] = pkp
#         result["pph_setahun"] = pph_setahun
        result["pph"] = pph
        result["pph_ta"] = pph_ta
        
        return result
