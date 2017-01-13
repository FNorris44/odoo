# -*- coding: utf-8 -*-
from datetime import date, datetime, timedelta
from openerp.exceptions import UserError
from openerp import models, fields, api, _, SUPERUSER_ID
#from odoo.exceptions import UserError
#from odoo import models, fields, api, _, SUPERUSER_ID


class autoservice(models.Model):
    _name = 'autoservice.autoservice'

    def _get_date_today(self):
        date_today = date.today().strftime('%Y-%m-%d') # timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return date_today

    name = fields.Char(string='Contract name', required=True, index=True, translate=True)
    contract_type_less = fields.Char(string='Type short description', index=True, translate=True)
    contract_type_descr = fields.Text(string='Type (contract) long description', translate=True)
    contract_created = fields.Date(string='Contract created', default=_get_date_today)
    contract_aproved = fields.Date(string='Contract aproved')
    contract_expired = fields.Date(string='Contract expired')
    contract_edit = fields.Date(string='Contract unlocked for revision')
    expired_reason = fields.Char(string='Expired reason')
    template_contract = fields.Boolean(string='Template contract', default=False, help='Template can not be set active, its purpose is to be duplicated')
    private_contract = fields.Boolean(string='is private contract', default=False)
    private_contract_partner = fields.Many2one('res.partner', string='Contract partner')
    contract_conditions = fields.Html(string='Contract general conditions', translate=True)
    priority = fields.Selection([('0', 'Normal'), ('1', 'High')], default='0', index=True)
    state = fields.Selection([('0', 'Draft'), ('1', 'Active'), ('2', 'Expired')], default='0', index=True)
    orders_ids = fields.One2many(comodel_name='autoservice.orders', inverse_name='id', string='Orders')
    contract_data_lock = fields.Boolean(string='Contract data lock', default=False)
    contract_operation_ids = fields.Many2many(comodel_name='autoservice.operation', string='Included operations')
    contract_sets_ids = fields.Many2many(comodel_name='autoservice.sets', string='Included operation sets')

    @api.one
    def action_aprove_contract(self):
        if self.private_contract is True and not self.private_contract_partner:
            raise UserError(_('For activating private contract select partner first.'))
        elif self.template_contract is True:
            raise UserError(_('Template can not be set active, its purpose is to be replicated'))
        else:
            self.write({
                'contract_aproved': date.today().strftime('%Y-%m-%d'),
                'contract_data_lock': True,
                'state': '1'
            })

    @api.one
    def action_expire_contract(self):
        self.write({
            'contract_expired': date.today().strftime('%Y-%m-%d'),
            'state': '2'
        })

    @api.one
    def action_edit_contract(self):
        self.write({
            'contract_edit': date.today().strftime('%Y-%m-%d'),
            'contract_data_lock': False,
            'state': '0'
        })


class asStages(models.Model):
    _name = 'autoservice.stages'
    _order = 'stage_sequence asc'

    stage = fields.Char('Name', size=16, required=True)
    stage_descr = fields.Text('Description')
    stage_sequence = fields.Integer('Sequence', required=True, help="Used to order the note stages")
    stage_value = fields.Integer()


    @api.multi
    def name_get(self):
        result = {}
        for autoservice.stages in self:
            result[autoservice.stages.id] = autoservice.stages.stage

        return result.items()


class asorders(models.Model):
    _name = 'autoservice.orders'
    _inherit = 'mail.thread'
    _description = "Auto service Order"
    _rec_name = 'nom'
    _order = 'nom desc'

    def _get_date_today(self):
        date_today = date.today().strftime('%Y-%m-%d')
        return date_today

    def _get_datetime_now(self):
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return now

    def get_default_stage(self):
        stage = self.env.ref('autoservice.stages_Draft', raise_if_not_found=False)
        return stage and stage.id or False

    nom = fields.Char('Service order', size=16, required=True, index=True)
    ref_nom = fields.Char('Referent number', size=32, index=True)
    vhk_id = fields.Many2one('autoservice.vehicles', string='Vehicle', required=True, delegate=True,
                             ondelete='restrict')
    project_id = fields.Many2one('project.project', string='Related project', ondelete='restrict')
    contract_id = fields.Many2one('autoservice.autoservice', string='Contract', ondelete='restrict', )
    resp_user_id = fields.Many2one('res.users', string='Responsible manager')
    customer_id = fields.Many2one('res.partner', string='Customer')
    stage_id = fields.Many2one('autoservice.stages', string='Stage', default=get_default_stage,
                               help='Current stage of Auto service order')
    date_set_new = fields.Date(string='Set as New')
    date_compleated = fields.Date(string='Set as Compleated')
    order_operations_ids = fields.Many2many(comodel_name='autoservice.operation', string='Auto service order operations')
    contract_operation_imported = fields.Boolean()
    order_sets_ids = fields.Many2many(
        'autoservice.sets',
        'autoservice_orders_autoservice_sets_rel',
        'autoservice_orders_id', 'autoservice_sets_id',
        string='Selected operation sets')
    accorder_sets_ids = fields.Many2many(
        'autoservice.sets',
        'autoservice_orders_autoservice_accpsets_rel',
        'autoservice_orders_id', 'autoservice_accpsets_id',
        string='Accepted operation sets')
    contract_operation_sets_imported = fields.Boolean()
    test_txt = fields.Char(string='test field')
    testt_txt = fields.Char(string='test field 2')
    oper_help = fields.Char(string='help field')
    accepted_sets = fields.Char(string='Accepted_sets')
    contact_person = fields.Many2one('res.partner', string='Contact person')
    order_created = fields.Date(string='Order created', default=_get_date_today)
    date_draft = fields.Date(string='Order creation date')
    date_planed = fields.Date(string='Planed date')
    date_realb = fields.Date(string='Start date')
    date_deadline = fields.Date(string='Deadline')
    date_reale = fields.Date(string='End date')
    date_paused = fields.Date(string='Stop date')
    date_released = fields.Date(string='Release date')
    date_canceled = fields.Date(string='Cancel date')
    date_uncanceled = fields.Date(string='Uncancel date')
    date_closed = fields.Date(string='Close date')
    date_reopen = fields.Date(string='Reopen date')  # default=fields.Datetime.now,\
    cancel_reason = fields.Char(string='Cancel reason')
    on_hold = fields.Boolean(string='Paused')
    priority = fields.Selection([
        ('0', 'Normal'),
        ('1', 'High')
    ], default='0', index=True)
    cancel = fields.Boolean(string='Canceled', default=False)
    closed = fields.Boolean(string='Closed', default=False)
    main_data_lock = fields.Boolean(string='Main data edit lock', default=False)
    form_data_lock = fields.Boolean(string='Form data edit lock', default=False)
    notes = fields.Text(string='Notes')
   
    order_contract_conditions = fields.Html(string='Contract general conditions', related='contract_id.contract_conditions')

    _sql_constraints = [('autoservice_orders_nom_unique', 'unique(nom)', 'Auto service order already exists')]

    @api.multi
    def _get_contr_operations(self):
        ct_id = self.contract_id.id
        ct_ids = []
        if ct_id:
            cta_ids = self.env['autoservice.autoservice'].sudo().browse(self.contract_id.id).mapped('contract_operation_ids').ids
            if cta_ids:
                ct_ids += cta_ids
            else: ct_ids = False
        else:
            raise UserError(_('Contract must be selected before perform this operation'))
        return ct_ids

    @api.multi
    def _import_contract_operations(self):
        opr_ids = []
        ctopr_ids = self._get_contr_operations()
        if ctopr_ids:
            opr_ids += ctopr_ids
            if opr_ids:
                self.order_operations_ids = opr_ids
                self.write({
                    'test_txt' : opr_ids,
                    'contract_operation_imported' : True
                })

        return True

    @api.multi
    def _get_contr_sets(self):
        ct_id = self.contract_id.id
        cts_ids = []
        if ct_id:
            cts_ids = self.env['autoservice.autoservice'].sudo().browse(self.contract_id.id).mapped('contract_sets_ids').ids

        return cts_ids

    @api.multi
    def _get_ord_sets(self):
        ordsets_ids = self.mapped('order_sets_ids').ids

        return ordsets_ids

    @api.multi
    def _import_contract_sets(self):
        sets_ids = []
        csets_ids = self._get_contr_sets()
        sets_ids += csets_ids
        if sets_ids:
            self.order_sets_ids = sets_ids
            self.write({
                'testt_txt' : sets_ids,
                'contract_operation_sets_imported' : True
            })

        return True

    @api.multi
    def _get_contr_sets_operations(self):
        ct_id = self.contract_id.id
        if ct_id:
            cts_ids = self.env['autoservice.autoservice'].sudo().browse(self.contract_id.id).mapped('contract_sets_ids').ids
            csts_ids = []
            if cts_ids:
                for tsk_id in cts_ids:
                    csts_id = self.env['autoservice.sets'].sudo().browse(tsk_id).mapped('asoperation_ids').ids
                    #csts_ids.append(csts_id)
                    csts_ids += csts_id
            else: csts_ids = False
        else:
            raise UserError(_('Contract must be selected before perform this operation'))

        return csts_ids

    @api.multi
    def import_contract_sets(self):
        a = self._get_contr_sets_operations()
        b = self._get_contr_operations()
        if a and b:                            #if not a and not b raise UserError
            self._import_contract_sets()
            self._import_contract_operations()
        elif a:
            self._import_contract_sets()
        elif b:
            self._import_contract_operations()
            self.write({
                'contract_operation_sets_imported' : True
            })
        else:
            raise UserError(_('Contract must have at least one operation or set with at least one operation'))

        return True

    @api.multi
    def _accept_set_operations(self, set_id):
        operation_ids = self.env['autoservice.sets'].sudo().browse(set_id).mapped('asoperation_ids').ids
        self.update({'order_operations_ids' : operation_ids})

        return True

    @api.multi
    def accept_operations_sets(self, ordsets_ids):
        ordsets_ids = self.mapped('order_sets_ids').ids
        accsets_ids = self.mapped('accorder_sets_ids').ids
        for set_id in ordsets_ids:
            if set_id not in accsets_ids:
                s = [set_id]
                self._accept_set_operations(set_id)
                accsets_ids += s
        self.accorder_sets_ids = accsets_ids
        self.write({
            'accepted_sets' : accsets_ids,
            'order_sets_ids': [(5, 0, 0)]
            })
        # return True

    @api.one
    def _get_rel_project(self):
        prj_id = self.project_id.id
        if prj_id:
            return prj_id
        else:
            raise UserError(_('Related project must be selected'))

    @api.one
    def get_customer(self):
        cst_id = self.customer_id.id
        if cst_id:
            return cst_id
        else:
            raise UserError(_('Order customer must be selected'))

    @api.multi
    def get_oper_vals(self, op_id):
       # op_vals = self.env['autoservice.operation'].browse(op_id).mapped('name') #, 'asoperation_code', 'asoperation_value', 'operation_order ')
        op_vals = self.env['autoservice.operation'].search([('id', '=', op_id)]).sorted(key=lambda r: r.name)

        return op_vals

    @api.multi
    def convert_operations_to_tasks(self):
        prid = self._get_rel_project()
        cstid = self.get_customer()
        op_ids = self.mapped('order_operations_ids').ids
        for op_id in op_ids:
            opr_vals = self.get_oper_vals(op_id)
            values = {'name' : opr_vals.name,
                      'sequence' : opr_vals.operation_order,
                      'planned_hours' : opr_vals.asoperation_value,
                      'project_id' : prid,
                      'user_id' : self.resp_user_id.id,
                      'partner_id': cstid,
                      }
            self.env['project.project'].search([('id', '=', prid)]).update({'task_ids' : [(0, 0, values)]})
        self.write({
            'oper_help' : 'OK',
            'order_operations_ids': [(5, 0, 0)]
        })

        return True
        
    @api.one
    def action_hold(self):
        self.write({
            'on_hold': True,
            'date_paused': date.today().strftime('%Y-%m-%d')
        })

    @api.one
    def action_unhold(self):
        self.write({
            'on_hold': False,
            'date_released': date.today().strftime('%Y-%m-%d')
        })

    @api.one
    def action_order_reopen(self):
        self.write({
            'closed': False,
            'date_reopen': date.today().strftime('%Y-%m-%d'),
            'form_data_lock': False,
            'stage_id': 3
        })

    @api.one
    def action_order_uncancel(self):
        self.write({
            'cancel': False,
            'date_uncanceled': date.today().strftime('%Y-%m-%d'),
            'form_data_lock': False
        })

    @api.one
    def action_order_close(self):
        self.write({
            'closed': True,
            'date_closed': date.today().strftime('%Y-%m-%d'),
            'form_data_lock': True
        })

    @api.one
    def action_order_cancel(self):
        self.write({
            'cancel': True,
            'date_canceled': date.today().strftime('%Y-%m-%d'),
            'form_data_lock': True
        })

    @api.one
    def action_set_stage_new(self):
        self.write({
            'date_set_new': date.today().strftime('%Y-%m-%d'),
            'main_data_lock': True,
            'stage_id': 2
        })

    @api.one
    def action_set_stage_inprogres(self):
        self.write({
            'date_realb': date.today().strftime('%Y-%m-%d'),
            'stage_id': 3
        })

    @api.one
    def action_set_stage_compleated(self):
        self.write({
            'date_compleated': date.today().strftime('%Y-%m-%d'),
            'stage_id': 4
        })

    @api.one
    def action_set_stage_finished(self):
        self.write({
            'date_reale': date.today().strftime('%Y-%m-%d'),
            'form_data_lock': True,
            'stage_id': 5
        })


class asvehicles(models.Model):
    _name = 'autoservice.vehicles'
    _inherit = 'mail.thread'
    _rec_name = 'vin'
    _order = 'make asc'

    order_ids = fields.One2many(comodel_name='autoservice.orders', inverse_name='id', string='Orders')
    vin = fields.Char('Chassis number-VIN:', size=32, required=True, index=True)
    body_no = fields.Char('Body number', size=32, index=True)
    eng_no = fields.Char('Engine number', size=32, index=True)
    make = fields.Char('Make', size=32)
    make_model = fields.Char('Model', size=32)
    submodel = fields.Char('Submodel', size=32)
    modification = fields.Char('Modification', size=32)
    license_plate = fields.Char('License plate', index=True)
    color = fields.Char('Color', size=32, index=True)
    color_effect = fields.Selection(
        selection=[('no effect', 'uni'), ('dl metal', 'metallik'), ('dl perl', 'perl'), ('ml', 'multi')])
    color_finish = fields.Selection(
        selection=[('lack', 'lack'), ('saten', 'saten'), ('matt', 'matt'), ('plastic', 'structure matt')])
    color_no = fields.Char('Color No', size=16)
    color_name = fields.Char('Color name', index=True)
    eng_type = fields.Selection(
        selection=[(1, 'Internal comb. engine'), (2, 'Electric engine'), (3, 'Steam engine'), ('other', 'other')])
    transmission_co = fields.Char('Count gears', size=4)
    transmission = fields.Selection(
        selection=[('man', 'manual'), ('semy', 'semi automatic'), ('auto', 'automatic'), ('other', 'other')])
    fuel = fields.Selection(
        selection=[('b', 'Benzin'), ('d', 'diesel'), ('lpg', 'LPG'), ('m', 'CNG'), ('h', 'Hidrogen'), ('a', 'Alcohol'),
                   ('e', 'Electro')])
    fuel_second = fields.Selection(
        selection=[('b', 'Benzin'), ('d', 'diesel'), ('lpg', 'LPG'), ('m', 'CNG'), ('h', 'Hidrogen'), ('a', 'Alcohol'),
                   ('e', 'Electro')])
    notes = fields.Text()
    owners = fields.Many2many('res.partner', string='Owners')

    _sql_constraints = [('autoservice_vehicles_vin_unique', 'unique(vin)', 'VIN nomber already exists')]

    @api.multi
    def name_get(self):
        result = {}
        for autoservice.vehicles in self:
            result[autoservice.vehicles.id] = str(autoservice.vehicles.make) + " > " + str(
                autoservice.vehicles.make_model) + " > " + str(autoservice.vehicles.vin)

        return result.items()


class asoperations(models.Model):
    _name = 'autoservice.operation'
    _order = 'operation_order'

    name = fields.Char(string='Operation name- unique', required=True, help='Create unique name for operation template')
    asoperation_code = fields.Char('Unique operation code', required=True)
    asoperation_value = fields.Integer('Operation Value', help='This value is multiplayer for operation unit', default='1')
    active = fields.Boolean(string='Active', default=True)
    operation_order = fields.Integer(string='Operation order', help='Integer value to resolve default order in operation list')

    _sql_constraints = [('autoservice_operation_asoperation_code_unique', 'unique(asoperation_code)', 'Auto service operation code already exists'),
                        ('autoservice_operation_name_unique', 'unique(name)', 'Auto service operation name already exists')]


class assets(models.Model):
    _name = 'autoservice.sets'
    _order = 'sets_order'

    name = fields.Char('Set name', required=True, help='Set contains operations, spare parts and consumatives')
    asoperation_ids = fields.Many2many(comodel_name='autoservice.operation', required=True, string='Operations')
    sets_order = fields.Integer(string='Set order', help='Integer value to resolve default order in sets list')

    _sql_constraints = [('autoservice_sets_name_unique', 'unique(name)', 'Set name already exists')]
