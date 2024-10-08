from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
# from datetime import datetime
from datetime import timedelta
from datetime import date, timezone


# from dateutil.relativedelta import relativedelta

class ClassMaster(models.Model):
    _name = 'logic.base.class'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'
    _description = 'Class'

    active = fields.Boolean(default=True)
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company.id)
    date = fields.Date(string="Date", index=True)
    batch_id = fields.Many2one('logic.base.batch', string="Batch Name")
    line_base_ids = fields.One2many('student.base.lines', 'class_base_id', string='Students')
    name = fields.Char(string="Class Room", index=True)
    code = fields.Char(string="Code", index=True)
    note = fields.Text(string='Notes')
    state = fields.Selection(selection=[
        ('draft', 'Draft'),
        ('inactive', 'Inactive'),
        ('active', 'Active')], default='draft')
    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")
    coordinator_id = fields.Many2one('res.users', string="Academic Coordinator")
    approve_id = fields.Many2one('res.users', string="Approved By", default=lambda self: self.env.user.id, readonly="1",
                                 tracking=True)
    tutor_id = fields.Many2one('res.users', string="Faculty",domain=[('faculty_check','=',True)])
    tot_seats = fields.Integer(string="Total Seats", index=True)
    student_id = fields.Many2one('res.partner', string="Student")
    total_seats = fields.Integer(string="Total Seats")
    available_seats = fields.Integer(string="Available Seats", compute='_compute_seats', readonly="1")
    create_date = fields.Datetime(string="Create Date", tracking=True, default=date.today())
    approve_date = fields.Datetime(string="Approve Date", tracking=True)
    balance = fields.Float(string='Pending Fee', compute='_compute_balance', store=True)
    batch_check_id = fields.Integer(string="Batch Check", compute='_compute_batch_id', store=True)
    admission_count = fields.Integer(string="Student Count", compute='_compute_student_count', readonly="1")
    allocated_studs_count_display = fields.Char(string="Allocated Students", compute="_compute_allocated_studs_count_display")
    
    @api.onchange('batch_id')
    def _onchange_batch_id(self):
        if self.batch_id:
            self.coordinator_id = self.batch_id.academic_coordinator.id

    @api.depends('line_base_ids')
    def _compute_allocated_studs_count_display(self):
        for record in self:
            if self.line_base_ids:
                record.allocated_studs_count_display = str(len(record.line_base_ids)) + " / " + str(record.total_seats)
            else:
                record.allocated_studs_count_display = "0" / str(record.total_seats)
    
    @api.depends('batch_id')
    def _compute_batch_id(self):
        for i in self:
            self.batch_check_id = i.batch_id.id

    def action_in_active(self):
        self.state = 'inactive'

    def action_approve(self):
        self.state = 'active'
        for i in self:
            i.approve_date = date.today()

    def rfq_approve(self):
        print("kkkkkkkkkkkkkkkkk")

    @api.model
    def test_logic_cron_code(self):
        res = self.env['res.class'].search([])
        for i in res:
            if i.state in 'active' and i.to_date == date.today() + timedelta(days=1):
                i.state = 'inactive'

    def action_students(self):
        ss = self.env['logic.base.class'].search([])

        # partner_ids = self.line_ids.mapped('student_id')
        return {
            'name': _('Students'),
            'view_mode': 'kanban,tree,form',
            # 'view_mode': 'tree,form',
            'domain': [('class_id', '=', self.id)],
            'res_model': 'logic.students',
            'type': 'ir.actions.act_window',
            'context': {'create': False, 'active_test': False},
        }

    @api.depends('total_seats', 'line_base_ids')
    def _compute_seats(self):
        # num = 0
        for k in self:
            k.available_seats = k.total_seats - len(k.line_base_ids)
    #
    # @api.depends('line_base_ids.pending_fee')
    # def _compute_balance(self):
    #     self.balance = 0
    #     for x in self:
    #         for z in x.line_base_ids:
    #             x.balance += z.pending_fee
    #         if x.available_seats < 0:
    #             raise ValidationError(_("This class is already filled"))

    def action_allocation(self):
        print('te')
        crm = self.env['classroom.allocate.student'].sudo().search([('class_id', '=', self.id)])
        return {
            'name': _('Allocation'),
            'view_mode': 'form',
            'res_model': 'class.base.allocate.student',
            'type': 'ir.actions.act_window',
            'target': 'new',
            "context": {
                'default_class_id': self.id,
                'default_batch_id': self.batch_id.id,
                # 'default_student_ids': self.student_id.id,
                # 'default_revenue': self.expected_revenue,
                # 'default_no_person': self.no_of_persons_package,
            },
        }
    
    def action_reallocation(self):
        print('te')
        return {
            'name': _('Reallocation'),
            'view_mode': 'form',
            'res_model': 'classroom.base.reallocate.student',
            'type': 'ir.actions.act_window',
            'target': 'new',
            "context": {
                'default_current_class_id': self.id,
                'default_batch_id': self.batch_id.id,
                # 'default_student_ids': self.student_id.id,
                # 'default_revenue': self.expected_revenue,
                # 'default_no_person': self.no_of_persons_package,
            },
        }
    #



class StudentLines(models.Model):
    _name = "student.base.lines"

    class_base_id = fields.Many2one('logic.base.class')
    student_id = fields.Many2one('logic.students', string="Student")
    batch_id = fields.Many2one('logic.base.batch', string="Batch")
    # pending_fee = fields.Float(string='Pending Fee', compute="onchange_ad_id", store=True)
    # admission_id = fields.Many2one('res.admission', string='Admission Number')
    # state = fields.Selection([
    #     ('draft', 'Draft'),
    #     ('confirm', 'Confirmed'),
    #     ('transfer', 'Transfer'), ('cancel', 'Cancel'), ('drop', 'Dropped')], related='ad_id.state', default='draft',
    #     string='Status',
    #     store=True)

    # @api.depends('admission_id')
    # def onchange_ad_id(self):
    #     for i in self:
    #         if i.admission_id:
    #             i.pending_fee = i.admission_id.balance


