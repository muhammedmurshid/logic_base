from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
from datetime import timedelta
from datetime import date


class LogicBaseBathes(models.Model):
    _name = 'logic.base.batch'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'
    _description = 'Batch'

    active = fields.Boolean(default=True)
    name = fields.Char(string="Batch Name", index=True, required=1)
    code = fields.Char(string="Batch Code", index=True)
    product_id = fields.Many2one('product.product', string="Product", index=True)
    company_id = fields.Many2one('res.company', string="Company", default=lambda self: self.env.company.id)
    branch_id = fields.Many2one('logic.base.branches', string="Branch", required=1)
    # location = fields.Many2one('res.company',string="Branch", index=True)
    tot_seats = fields.Integer(string="Total Seats", index=True)
    # batch_id = fields.Many2one('res.batch', string="Batch Name")
    student_id = fields.Many2one('res.partner', string="Student")
    # available_seats = fields.Integer(string="Available Seats",compute='_compute_seats', readonly="1", store=True)
    available_seats = fields.Integer(string="Available Seats", compute='_compute_seats', readonly="1", store=True)
    admission_count = fields.Integer(string="Student Count", compute='_compute_student_count', readonly="1")
    created_id = fields.Many2one('res.users', string="Created By", readonly="1")
    state = fields.Selection([('draft', 'Draft'),
                              ('marketing', 'Manager Approval'),
                              ('accounts', 'Accounts Approval'),
                              ('done', 'Done'),
                              ('cancel', 'Cancelled')], default='draft', string="Status")
    academic_year = fields.Char(string="Academic Year", required=1)
    academic_coordinator = fields.Many2one('res.users', string="Academic Coordinator")
    batch_window = fields.Selection(
        [('january', 'January'), ('february', 'February'), ('march', 'March'), ('april', 'April'), ('may', 'May'),
         ('june', 'June'), ('july', 'July'), ('august', 'August'), ('september', 'September'), ('october', 'October'),
         ('november', 'November'), ('december', 'December')], string="Month")
    from_date = fields.Date(string="Start Date")
    course_id = fields.Many2one('logic.base.courses', string="Course")
    to_date = fields.Date(string="End Date")
    class_ids = fields.One2many("logic.base.class", "batch_id", string="Classes")
    adm_id = fields.Many2one('res.admission', string="Admission")
    message_ids = fields.One2many('mail.message', 'res_id', string="Messages")
    create_date = fields.Datetime(string="Create Date", tracking=True, default=date.today())
    approve_date = fields.Date(string="Approve Date", tracking=True)
    active_state = fields.Selection([('active', 'Active'), ('inactive', 'Inactive')], string="Status", default='active')
    class_teacher_id = fields.Many2one('hr.employee', string="Class Teacher")
    fee_collection_id = fields.Many2one('hr.employee', string="Fee Collector")

    # fee details
    admission_fee = fields.Float(string="Admission Fee")
    course_fee = fields.Float(string="Course Fee")
    tax_id = fields.Many2one('account.tax', string="Tax")

    def action_direct_done(self):
        self.state = 'done'

    def name_get(self):
        result = []
        for record in self:
            if not self.env.context.get('custom_name_display'):
                result.append((record.id, record.name))
            else:
                students_count = self.env['logic.students'].search_count([('batch_id', '=', record.id)])
                if students_count == 1:
                    text = 'Student'
                else:
                    text = 'Students'
                result.append((record.id, f'{record.name} ({students_count} {text})'))
        return result

    @api.depends('make_visible_head_batch')
    def get_batch_head(self):
        print('kkkll')
        user_crnt = self.env.user.id

        res_user = self.env['res.users'].search([('id', '=', self.env.user.id)])
        if res_user.has_group('logic_base.academic_head_batch'):
            self.make_visible_head_batch = False

        else:
            self.make_visible_head_batch = True

    make_visible_head_batch = fields.Boolean(string="User", default=True, compute='get_batch_head')

    @api.depends('make_visible_accounts_batch')
    def get_batch_accounts(self):
        print('kkkll')
        user_crnt = self.env.user.id

        res_user = self.env['res.users'].search([('id', '=', self.env.user.id)])
        if res_user.has_group('logic_base.accounts_batch'):
            self.make_visible_accounts_batch = False

        else:
            self.make_visible_accounts_batch = True

    make_visible_accounts_batch = fields.Boolean(string="User", default=True, compute='get_batch_accounts')

    @api.depends('make_visible_manager_batch')
    def get_batch_manager(self):
        print('kkkll')
        user_crnt = self.env.user.id
        res_user = self.env['res.users'].search([('id', '=', self.env.user.id)])
        if res_user.has_group('logic_base.manager_batch'):
            self.make_visible_manager_batch = False
        else:
            self.make_visible_manager_batch = True

    make_visible_manager_batch = fields.Boolean(string="User", default=True, compute='get_batch_manager')

    def action_cancel(self):
        activity_id = self.env['mail.activity'].search(
            [('res_id', '=', self.id), (
                'activity_type_id', '=', self.env.ref('logic_base.mail_for_logic_base_batches').id)])
        activity_id.action_feedback(feedback=f'Rejected.')
        self.state = 'cancel'

    def action_approve(self):
        for i in self:
            print('ppp')
            users = self.env.ref('logic_base.marketing_manager_logic_base').users
            for user in users:
                i.activity_schedule('logic_base.mail_for_logic_base_batches', user_id=user.id,
                                    note=f'Batch is created Please add fee details and approve.')
            #     if user.has_group('logic_base.marketing_manager_logic_base'):
            #         print(user.name, 'user')

        self.state = 'marketing'
        for i in self:
            i.approve_date = date.today()
            i.created_id = self.env.user.id

    def manager_approve(self):
        if not self.course_fee:
            raise UserError(_("Please Enter Course Fee"))
        if not self.admission_fee:
            raise UserError(_("Please Enter Admission Fee"))
        if not self.tax_id:
            raise UserError(_("Please Enter Tax"))
        self.state = 'accounts'
        activity_id = self.env['mail.activity'].search(
            [('res_id', '=', self.id), ('user_id', '=', self.env.user.id), (
                'activity_type_id', '=', self.env.ref('logic_base.mail_for_logic_base_batches').id)])
        activity_id.action_feedback(feedback=f'Approved.')
        users = self.env.ref('logic_base.accounts_logic_base').users
        for user in users:
            self.activity_schedule('logic_base.mail_for_logic_base_batches', user_id=user.id,
                                   note=f'Batch is created Please check details and approve.')

    admission_plus_course_fee = fields.Float(string="Admission + Course Fee",
                                             compute='_compute_admission_plus_course_fee', store=True)

    @api.depends('admission_fee', 'course_fee')
    def _compute_admission_plus_course_fee(self):
        for i in self:
            i.admission_plus_course_fee = i.admission_fee + i.course_fee

    tax_amount = fields.Float(string="Tax Amount", compute='_compute_tax_amount', store=True)

    @api.depends('tax_id', 'admission_plus_course_fee')
    def _compute_tax_amount(self):
        for i in self:
            # print(i.tax_id.amount_type, 'tax')
            if i.tax_id.amount_type:
                if i.tax_id.amount_type == 'percent':
                    if i.admission_plus_course_fee != 0:
                        i.tax_amount = (i.admission_plus_course_fee * i.tax_id.amount) / 100

    batch_fee = fields.Float(string="Batch Fee", compute='_compute_batch_fee', store=True)
    currency_id = fields.Many2one('res.currency', string='Currency', required=True,
                                  default=lambda self: self.env.user.company_id.currency_id)
    price_tax = fields.Float(string='Taxes', readonly=True, compute='_compute_amount')
    price_total = fields.Float(string='Total', readonly=True, compute='_compute_amount')
    price_subtotal = fields.Float(string='Subtotal', readonly=True, compute='_compute_amount')

    @api.depends('course_fee', 'admission_fee', 'tax_amount', 'admission_plus_course_fee', 'tax_id')
    def _compute_batch_fee(self):
        for i in self:
            i.batch_fee = i.tax_amount + i.admission_plus_course_fee

    @api.depends('admission_fee', 'tax_id')
    def _compute_amount(self):
        """
        Compute the amounts of the SO line.
        """
        for line in self:
            price = line.admission_fee * (1 - (0.0) / 100.0)
            taxes = line.tax_id.compute_all(price, line.currency_id)
            line.update({
                'price_tax': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
                'price_total': taxes['total_included'],
                'price_subtotal': taxes['total_excluded'],
            })


    def accounts_approve(self):
        activity_id = self.env['mail.activity'].search(
            [('res_id', '=', self.id), (
                'activity_type_id', '=', self.env.ref('logic_base.mail_for_logic_base_batches').id)])
        activity_id.action_feedback(feedback=f'Approved.')
        self.state = 'done'
        # for i in self:
        #     i.approve_date = date.today()
        #     i.created_id = self.env.user.id

    @api.model
    def test_logic_cron_code(self):
        res = self.env['logic.batch'].search([])
        for i in res:
            if i.state in 'active' and i.to_date == date.today() + timedelta(days=1):
                i.state = 'inactive'

    def _compute_student_count(self):
        admission_ids = self.env['logic.base.class'].search_count([('batch_id', '=', self.id)])
        print(admission_ids, 'eb')
        if admission_ids:
            self.admission_count = admission_ids
        else:
            self.admission_count = 0
        # for i in admission_ids:
        #     print(len(i.batch_id), 'count')

    @api.depends('tot_seats')
    def _compute_seats(self):
        for i in self:
            count = self.env['res.admission'].sudo().search_count([('batch_id', '=', i.id), ('state', '=', 'confirm')])
            # if count:
            #     i.admission_count = count
            if i.tot_seats:
                i.available_seats = i.tot_seats - count
            if i.available_seats < 0:
                raise ValidationError(
                    _("This Batch is Already Filled"))

    def action_class_view(self):
        ss = self.env['logic.base.class'].search([('batch_id.id', '=', self.id)])
        print(self.id, 'sel')
        print(ss.batch_id, 'selffff')

        return {
            'name': _('Students'),
            'view_mode': 'kanban,tree,form',
            'res_model': 'logic.base.class',
            # 'view_mode': 'tree,form',
            'domain': [('batch_id', 'in', ss.mapped('batch_id').ids)],
            'type': 'ir.actions.act_window',
            'context': {'create': False, 'active_test': False}}

        # partner_ids = ss.mapped('batch_id')
        # print(partner_ids, 'dd')
        # student_ids = ss.mapped('batch_id')
        # for i in ss:
        #     print(i.name, 'll')

    # def action_allocation(self):
    #     crm = self.env['classroom.allocate.student'].search([('class_id', '=', self.id)])
    #     return {
    #         'name': _('Task'),
    #         'view_mode': 'form',
    #         'res_model': 'classroom.allocate.student',
    #         'type': 'ir.actions.act_window',
    #         'target': 'new',
    #         "context": {
    #             'default_batch_id': self.id,
    #             'default_student_ids': self.student_id.id,
    #             # 'default_revenue': self.expected_revenue,
    #             # 'default_no_person': self.no_of_persons_package,
    #
    #         },
    #     }
