from odoo import api, fields, models


class LogicBaseCourses(models.Model):
    _name = 'logic.base.courses'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Course'
    active = fields.Boolean(default=True)
    name = fields.Char(string='Name', required=True)
    course_fee = fields.Float(string='Course Fee')
    type = fields.Selection([('indian', 'Indian'), ('international', 'International'), ('crash', 'Crash')],
                            string='Type')
    board_registration = fields.Boolean(string='Board Registration')
    company_id = fields.Many2one('res.company', string="Branch", default=lambda self: self.env.company.id)
    currency_id = fields.Many2one('res.currency', string='Currency', required=True,
                                  default=lambda self: self.env.user.company_id.currency_id)
    course_levels = fields.Many2many('course.levels', string='Course Levels')
    papers = fields.Many2many('course.papers', 'paper_id', string='Papers')
    state = fields.Selection([('draft', 'Draft'), ('done', 'Done')], default='draft')
    academic_head = fields.Many2one('res.users', string='Academic Head')

    def create_course(self):
        self.state = 'done'
        self.env['product.product'].create({
            'name': self.name,
            'type': 'service',
            'categ_id': 1,
            'uom_id': 1,
            'uom_po_id': 1,
            'lst_price': self.course_fee,
        })

    def return_menu(self):
        self.state = 'draft'


class CoursePapers(models.Model):
    _name = 'course.papers'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Course'

    name = fields.Char(string='Paper', required=True)
    course_id = fields.Many2one('logic.base.courses', string='Course')
    paper_id = fields.Many2one('logic.base.courses', string='Course')
    group_ids = fields.Many2many('course.groups', string='Groups')


class CourseLevels(models.Model):
    _name = 'course.levels'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Course Level'

    name = fields.Char(string='Level', required=True)
    groups_ids = fields.Many2many('course.groups', string='Groups')
    course_id = fields.Many2one('logic.base.courses', string='Course')


class CourseGroups(models.Model):
    _name = 'course.groups'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Course Group'

    name = fields.Char(string='Group', required=True)
    level_ids = fields.Many2many('course.levels', string='Levels')
