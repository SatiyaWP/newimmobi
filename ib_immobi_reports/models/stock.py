# -*- encoding: utf-8 -*-
# © 2017 Ibrohim Binladin | ibradiiin@gmail.com | +62-838-7190-9782 | http://ibrohimbinladin.wordpress.com
##########################################################################################################

from openerp import models, api


class StockMove(models.Model):
    _inherit = "stock.move"

    @api.model
    def _get_invoice_line_vals(self, move, partner, inv_type):
        res = super(StockMove, self)._get_invoice_line_vals(move, partner,
                                                            inv_type)
        if move.purchase_line_id:
            res['discount'] = move.purchase_line_id.discount
        elif move.origin_returned_move_id.purchase_line_id:
            res['discount'] = move.origin_returned_move_id.purchase_line_id.discount
        return res
