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


class ir_protocolli_da_recuperare(osv.osv):

    _name = "ir.protocolli_da_recuperare"
    _description = "ir.protocolli_da_recuperare"

    _columns = {
        'name': fields.char('Classe', size=32),
        'sequence_id': fields.many2one('ir.sequence', 'Sequence'),
        'protocollo': fields.char('Protocollo', size=32),
        'data': fields.date('Data'),
    }

    _order = "protocollo asc"

ir_protocolli_da_recuperare()


class ir_sequence(osv.osv):
    _name = "ir.sequence"
    _inherit = "ir.sequence"

    def next_by_id(self, cr, uid, sequence_id, context=None):
        recuperare_obj = self.pool.get('ir.protocolli_da_recuperare')
        recuperare_ids = recuperare_obj.search(cr, uid, [('sequence_id', '=', sequence_id)])
        if recuperare_ids:
            # ----- Se lo trova ne recupera il protocollo e lo cancella
            recuperare_id = recuperare_ids[0]
            protocollo = recuperare_obj.browse(cr, uid, recuperare_id).protocollo
            recuperare_obj.unlink(cr, uid, recuperare_id)
            return protocollo
        else:
            return super(ir_sequence, self).next_by_id(cr, uid, sequence_id, context)

    def next_by_code(self, cr, uid, sequence_code, context=None):
        recuperare_obj = self.pool.get('ir.protocolli_da_recuperare')
        recuperare_ids = recuperare_obj.search(
            cr, uid, [('name', '=', sequence_code)])
        if recuperare_ids:
            # ----- Se lo trova ne recupera il protocollo e lo cancella
            recuperare_id = recuperare_ids[0]
            protocollo = recuperare_obj.browse(
                cr, uid, recuperare_id).protocollo
            recuperare_obj.unlink(cr, uid, recuperare_id)
            return protocollo
        else:
            return super(ir_sequence, self).next_by_code(
                cr, uid, sequence_code, context)

ir_sequence()
