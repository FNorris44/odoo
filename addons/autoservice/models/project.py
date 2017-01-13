# -*- coding: utf-8 -*-
#from datetime import date, datetime, timedelta
#from openerp.exceptions import Warning
from openerp import models, fields, api, _


class project(models.Model):
    _inherit = 'project.project'

    x_autoservice_orders_ids = fields.One2many(comodel_name='autoservice.orders', inverse_name='id',
                                             string='Auto service order')
    '''TODO prepend x_  , move to project.py, import in __init__.py'''