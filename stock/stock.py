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


class stock_picking(osv.osv):

	_name = "stock.picking"
	_inherit = "stock.picking"

	def unlink(self, cr, uid, ids, context=None):
		# ----- Cicla gli indici per scrivere nella tabella di recupero protocolli
		for stock_id in ids:
			protocollo = self.browse(cr, uid, stock_id).ddt_number
			if protocollo:
				data = self.browse(cr, uid, stock_id).date
				self.pool.get('ir.protocolli_da_recuperare').create(cr, uid,
					{'name':'stock.ddt', 'protocollo':protocollo, 'data':data})
		return super(stock_picking, self).unlink(cr, uid, ids, context=None)

stock_picking()
