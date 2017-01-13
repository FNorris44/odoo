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

{
    'name': 'POS Sending Emails',
    'version': '1.0',
    'category': 'customized',
    'description': """POS Sending EMails.""",
    'author':'73Lines',
    'website': 'http://www.73lines.com',
    'depends': ['base', 'mail', 'point_of_sale'],
    'installable': True,
    'auto_install': False,
    'data': [
        'edi/pos_order.xml',
        'edi/pos_order_email.xml',
        'views/point_of_sale_view.xml',
        'views/pos_config_view.xml',
        'views/pos_order_view.xml',
    ],
     'images': [
        'static/description/pos_email_receipt.jpg',
    ],
    'price': 0,
    'currency': 'EUR',
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
