# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Andrea Cometa - Perito informatico
#    All Rights Reserved
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
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


class ir_sequence_recovery(osv.osv):

    _name = "ir.sequence_recovery"
    _description = "ir.sequence_recovery"

    _columns = {
        'name': fields.char('Class Name', size=32),
        'sequence_id': fields.many2one('ir.sequence', 'Sequence'),
        'sequence': fields.char('Sequence Number', size=32),
        'date': fields.date('Date'),
    }

    _defaults = {
        'date': fields.date.context_today,
        }

    _order = "date, sequence asc"

    def set(self, cr, uid, ids, class_name, sequence_field='name',
            sequence_code='', sequence_id=False, context=None):
        # ----- init
        class_obj = self.pool.get(class_name)
        recovery_ids = []
        # ----- Extract the sequence id if it's not passed
        seq_id = sequence_id
        if sequence_code and not sequence_id:
            sequence_code_ids = self.pool.get('ir.sequence').search(
                cr, uid, [('name', '=', sequence_code)])
            if sequence_code_ids:
                seq_id = sequence_code_ids[0]
        # ----- For each record deleted save the parameters
        for id in ids:
            o = class_obj.browse(cr, uid, id)
            sequence = o[sequence_field]
            if sequence:
                vals = {
                    'name': class_name,
                    'sequence': sequence,
                    'sequence_id': seq_id,
                    }
                recovery_id = self.create(cr, uid, vals, context)
                recovery_ids.append(recovery_id)
        return recovery_ids

ir_sequence_recovery()


class ir_sequence(osv.osv):

    _name = "ir.sequence"
    _inherit = "ir.sequence"

    def next_by_id(self, cr, uid, sequence_id, context=None):
        recovery_obj = self.pool.get('ir.sequence_recovery')
        recovery_ids = recovery_obj.search(
            cr, uid, [('sequence_id', '=', sequence_id)])
        if recovery_ids:
            # ----- If found it, it recoveries the sequence and return it
            recovery_id = recovery_ids[0]
            sequence = recovery_obj.browse(cr, uid, recovery_id).sequence
            recovery_obj.unlink(cr, uid, recovery_id)
            return sequence
        else:
            return super(ir_sequence, self).next_by_id(
                cr, uid, sequence_id, context)

    def next_by_code(self, cr, uid, sequence_code, context=None):
        recovery_obj = self.pool.get('ir.sequence_recovery')
        recovery_ids = recovery_obj.search(cr, uid,
                                           [('name', '=', sequence_code)])
        if recovery_ids:
            # ----- If found it, it recoveries the sequence and return it
            recovery_id = recovery_ids[0]
            sequence = recovery_obj.browse(cr, uid, recovery_id).sequence
            recovery_obj.unlink(cr, uid, recovery_id)
            return sequence
        else:
            return super(ir_sequence, self).next_by_code(
                cr, uid, sequence_code, context)

ir_sequence()
