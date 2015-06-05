# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (c) 2012 Andrea Cometa All Rights Reserved.
#                       www.andreacometa.it
#                       openerp@andreacometa.it
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from osv import fields, osv


class account_invoice(osv.osv):
    _name = "account.invoice"
    _inherit = "account.invoice"

    def unlink(self, cr, uid, ids, context=None):
        # --- Cicla gli indici per scrivere nella tabella di recupero protocolli
        for account_id in ids:
            protocollo_obj = self.browse(cr, uid, account_id)
            # print '============', protocollo_obj.internal_number
            protocollo = protocollo_obj.internal_number
            sequence_id = protocollo_obj.journal_id.sequence_id.id
            if protocollo:
                data = self.browse(cr, uid, account_id).date_invoice
                self.pool['ir.protocolli_da_recuperare'].create(
                    cr, uid, {
                        'name': ' account.journal',
                        'protocollo': protocollo,
                        'data': data,
                        'sequence_id': sequence_id, })
        return super(account_invoice, self).unlink(cr, uid, ids, context=None)

account_invoice()
