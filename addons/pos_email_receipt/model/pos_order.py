 # -*- coding: utf-8 -*-
##############################################################################
#
#    73Lines Development Pvt. Ltd.
#    Copyright (C) 2009-TODAY 73Lines(<http://www.73lines.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
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
from openerp.osv import osv
from openerp.osv import orm
from openerp.osv import fields


class pos_order(osv.osv):
    _name = 'pos.order'
    _inherit = ['pos.order','mail.thread', 'ir.needaction_mixin']

    def create_picking(self, cr, uid, ids, context=None):
        result = super(pos_order, self).create_picking(
            cr, uid, ids, context=context)
        obj = self.browse(cr, uid, ids[0], context=context)
        conf_pool = self.pool.get('pos.config')
        conf_ids = conf_pool.search(cr, uid, [('auto_mail', '=', True)],
                                    context=context)
        if conf_ids and obj.partner_id and obj.partner_id.email:
            ir_model_data = self.pool.get('ir.model.data')
            template_id = ir_model_data.get_object_reference(
                cr, uid, 'pos_email_receipt', 'email_template_edi_pos_order')[1]
            self.pool.get('mail.template').send_mail(
                cr, uid, template_id, obj.id, force_send=True, context=context)
        return result

    def send_mail_customer(self, cr, uid, order, email):
        if not order:
            return True
        if not email:
            return True
        order_ids = self.pool.get('pos.order').search(
            cr, uid, [('pos_reference', '=', order)])
        if not order_ids:
            return True
        order = self.browse(cr, uid, order_ids[0])
        ir_model_data = self.pool.get('ir.model.data')
        template_id = ir_model_data.get_object_reference(
            cr, uid, 'pos_email_receipt', 'email_template_edi_pos_order_email')[1]
        self.pool.get('mail.template').write(cr, uid, template_id, {
            'email_to': email
        })
        self.pool.get('mail.template').send_mail(
            cr, uid, template_id, order.id, force_send=True, context={})
        return True
