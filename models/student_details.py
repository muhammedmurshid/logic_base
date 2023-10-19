from odoo import fields, models, api, _
from odoo.exceptions import UserError


class LogicStudents(models.Model):
    _name = 'logic.students'
    _inherit = 'mail.thread'
    _description = 'Student Profile'

    active = fields.Boolean(default=True)
    name = fields.Char(string='Name', copy=False, required=True)
    dob = fields.Date(string="Date of Birth")
    gender = fields.Selection(selection=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], string="Gender")
    email = fields.Char(string='Email address')
    phone_number = fields.Char(string='Mobile No')
    whatsapp_no = fields.Char(string="Whatsapp No")
    admission_fee = fields.Float(string='Admission fee')
    admission_no = fields.Char(string="Admission No")
    reference = fields.Char(string="Reference", readonly=True,
                            copy=False, default=lambda self: 'Adv/')
    student_id = fields.Char(string='Student ID')
    joining_date = fields.Date(string='Joining Date')
    aadhar_number = fields.Char(string='Aadhar Number')
    parent_name = fields.Char(string='Parent Name')
    father_name = fields.Char(string='Father Name')
    father_number = fields.Char(string='Father Number')
    mother_name = fields.Char(string='Mother Name')
    mother_number = fields.Char(string='Mother Number')
    parent_whatsapp = fields.Char(string='Parent Whatsapp')
    parent_email = fields.Char(string="Parent Email")
    course_studied = fields.Char(string='Course Studied')
    last_institute_studied = fields.Char(string='Last Institute Studied')
    mode_of_study = fields.Selection([('online', 'Online'), ('offline', 'Offline')], string='Mode of Study')
    street = fields.Char()
    street2 = fields.Char()
    zip = fields.Char()
    city = fields.Char()
    current_status = fields.Boolean(string='Active', default=True,
                                    help="If this student is discontinued disable this field", widget='active_circle')
    upaya_std_ids = fields.One2many('students.attendance.upaya', 'upaya_std_id')
    bring_buddy_attendance_ids = fields.One2many('bring.buddy.students.attendance', 'bring_std_id')
    yes_plus_att_ids = fields.One2many('students.attendance.yes_plus', 'yes_attendance_id')
    # adm_no_id = fields.Many2one('res.admission', string='Admission Number')
    state = fields.Many2one('res.country.state', 'Fed. State', domain="[('country_id', '=?', country)]")
    country = fields.Many2one('res.country')
    stud_id = fields.Integer()
    batch_id = fields.Many2one('logic.base.batch', string='Batch')
    status = fields.Selection([('draft', 'Draft'), ('linked', 'Linked'), ('discontinue', 'Discontinued')],
                              default='draft', string='Status', tracking=True)
    related_partner = fields.Many2one('res.partner', string='Related Partner')
    class_id = fields.Integer(string='Class')
    adm_id = fields.Integer(string='Admission ID')

    # logic yes plus fields

    day_one_date = fields.Date('Date')
    day_one = fields.Selection([('present', 'Present'), ('absent', 'Absent')], 'Attendance')
    day_two_date = fields.Date('Date')
    day_two = fields.Selection([('present', 'Present'), ('absent', 'Absent')], 'Attendance')
    day_three_date = fields.Date('Date')
    day_three = fields.Selection([('present', 'Present'), ('absent', 'Absent')], 'Attendance')
    day_four_date = fields.Date('Date')
    day_four = fields.Selection([('full_day', 'Full Day'), ('half_day', 'Half Day'), ('absent', 'Absent')],
                                'Attendance')
    day_five_date = fields.Date('Date')
    day_five = fields.Selection([('full_day', 'Full Day'), ('half_day', 'Half Day'), ('absent', 'Absent')],
                                'Attendance')

    # logic excel attendance fields
    day_one_excel = fields.Date('Date')
    day_one_excel_attendance = fields.Selection(
        [('full_day', 'Full Day'), ('half_day', 'Half Day'), ('absent', 'Absent')], 'Attendance')
    day_two_excel = fields.Date('Date')
    day_two_excel_attendance = fields.Selection(
        [('full_day', 'Full Day'), ('half_day', 'Half Day'), ('absent', 'Absent')],
        'Attendance')
    day_three_excel = fields.Date('Date')
    day_three_excel_attendance = fields.Selection(
        [('full_day', 'Full Day'), ('half_day', 'Half Day'), ('absent', 'Absent')],
        'Attendance')

    # logic cip attendance fields
    day_one_cip = fields.Date('Date')
    day_one_cip_attendance = fields.Selection(
        [('full_day', 'Full Day'), ('half_day', 'Half Day'), ('absent', 'Absent')], 'Attendance')
    day_two_cip = fields.Date('Date')
    day_two_cip_attendance = fields.Selection(
        [('full_day', 'Full Day'), ('half_day', 'Half Day'), ('absent', 'Absent')],
        'Attendance')
    day_three_cip = fields.Date('Date')
    day_three_cip_attendance = fields.Selection(
        [('full_day', 'Full Day'), ('half_day', 'Half Day'), ('absent', 'Absent')],
        'Attendance')

    # students Bank details
    bank_name = fields.Char('Bank Name')
    account_number = fields.Char('Account Number')
    ifsc_code = fields.Char('IFSC Code')
    branch = fields.Char('Branch')
    holder_name = fields.Char('Account Holder Name')
    attempt = fields.Selection(selection=[('first','First'),('second','Second'),('third','Third'),('fourth','Fourth')], string="Attempt")
    recording_status = fields.Selection(selection=[('recording','Recording'),('not_recording','Not Recording')], string="Recording/Not")

    @api.model
    def create(self, vals):
        if vals.get('reference', _('New')) == _('New'):
            vals['reference'] = self.env['ir.sequence'].next_by_code(
                'logic.students') or _('New')
        res = super(LogicStudents, self).create(vals)
        return res

    def action_open_admission_custom(self):
        print("ooooooooooooooooooo")
        ff = self.env['res.admission'].search([])
        # for i in ff:
        #     print(i.admission_id)
        for i in self:
            return {
                'type': 'ir.actions.act_window',
                'name': 'Admission',
                'res_model': 'res.admission',
                'view_mode': 'tree,form',
                'target': 'current',
                'domain': [('crm_lead_id', '=', i.stud_id)],
                # 'domain' : 'admission_id'= self.partner_id
            }

    def action_open_class_custom(self):
        print(self.batch_id.name, 'self')

        data = self.env['logic.base.class'].search([])
        for i in data:
            print(i.batch_id.name, 'selfff')
            return {
                'type': 'ir.actions.act_window',
                'name': 'Class',
                'res_model': 'logic.base.class',
                'view_mode': 'tree,form',
                'target': 'current',
                'domain': [('batch_id.id', '=', self.batch_id.id)]
            }

    def action_admission(self):
        student_name = self.env['logic.students'].sudo().create({

            'name': self.student_name,
            'phone_number': self.phone,
            'email': self.email_from,
            'stud_id': self.id,
            # 'student_id': self.street2,
            # 'city': self.city,
            # 'aadhar_number': 111,
            'parent_name': self.parent_name,
            'mother_name': self.mother_name,
            'mother_number': self.mother_no,
            'father_name': self.father_name,
            'father_number': self.father_no,
            'course_studied': self.course_studied,
            'last_institute_studied': self.last_institution,
            'mode_of_study': self.mode_of_study,
            'street': self.street,
            'street2': self.street2,
            'city': self.city,
            'state_id': self.state_id.id,
            'zip': self.zip,
            'country_id': self.country_id.id,

        })
        res = super(LogicStudents, self).action_admission(vals)
        return res

    def link_partner(self):

        ss = self.env['res.partner'].search([])
        if not self.stud_id:
            raise UserError('Student do not match')

        for i in ss:
            print(self.stud_id, 'stud')
            print(i.part_id, 'paar')
            if i.part_id == self.stud_id:
                print('ya')
                i.related_student = self.id
                self.student_id = i.reference
                self.related_partner = i.id
                self.status = 'linked'
            else:
                print('ll')
        # else:
        #     raise UserError('Students do not match')

    def action_open_exam_results(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Exam Results',
            'res_model': 'logic.student.result',
            'view_mode': 'tree',
            'target': 'current',
            'domain': [('student_id', '=', self.id)],
        }

    def action_open_student_attendances(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Attendances',
            'res_model': 'student.attendance',
            'view_mode': 'tree',
            'target': 'current',
            'domain': [('student_id', '=', self.id)],
            'context': {'search_default_class_id': 1}
        }

    def return_draft(self):
        self.status = 'draft'

    @api.onchange('current_status')
    def _compute_current_student_status(self):
        for rec in self:
            if rec.current_status == False:
                rec.status = 'discontinue'
                inactive_date = fields.Date.today()
                rec.inactive_date = str(inactive_date)
                print(rec.inactive_date, 'inactive_date')
            else:
                rec.status = 'draft'

    inactive_date = fields.Char(string='Inactive Date')


class StudentRelationCustom(models.Model):
    _inherit = "res.partner"

    # related_student = fields.Char(string='Related Student')
    related_student = fields.Many2one('logic.students', string='Related Student', readonly=True)


class ClassRoomallocateStudent(models.TransientModel):
    _name = 'class.base.allocate.student'
    _description = 'Allocate students to class room'

    batch_id = fields.Many2one('logic.base.batch', string="Batch", readonly=True)

    @api.onchange('batch_id')
    def get_students_domain(self):
        already_allocated_stud_ids = []
        for class_id in self.batch_id.class_ids:
            for stud_line in class_id.line_base_ids:
                already_allocated_stud_ids.append(stud_line.student_id.id)
        return {'domain': {
            'student_ids': [('batch_id', '=', self.batch_id.id), ('id', 'not in', already_allocated_stud_ids)]}}

        # return [('id','not in',already_allocated_stud_ids),('batch_id','=',self.batch_id.id)]

    student_ids = fields.Many2many('logic.students', string="Students", copy=True)
    # admission_ids = fields.Many2many('res.admission', string="Admision")
    class_id = fields.Many2one('logic.base.class', string="Class", readonly=True)

    def action_allocation(self):

        for student in self.student_ids:
            student_line = self.env['student.base.lines'].create({
                'class_base_id': self.class_id.id,
                'student_id': student.id,
                'batch_id': self.batch_id.id,

            })
            self.class_id.write({
                'line_base_ids': [(4, student_line.id)]
            })


class ReallocateBase(models.TransientModel):
    _name = "classroom.base.reallocate.student"

    batch_id = fields.Many2one('logic.base.batch', string="Batch")
    student_ids = fields.Many2many('logic.students', string="Students")
    # admission_ids = fields.Many2many('res.admission', string="Admision")
    allocate_class_id = fields.Many2one('logic.base.class', string="Allocate to Class", required=True)
    current_class_id = fields.Many2one('logic.base.class', domain="[('batch_id','=',batch_id)]", string="Current Class",
                                       required=True)

    @api.onchange('batch_id')
    def get_students_domain(self):
        already_allocated_stud_ids = []
        for stud_line in self.current_class_id.line_base_ids:
            already_allocated_stud_ids.append(stud_line.student_id.id)
        return {'domain': {'student_ids': [('id', 'in', already_allocated_stud_ids)]}}

    def action_reallocation(self):
        for student in self.student_ids:
            allocated_student_line = self.env['student.base.lines'].search(
                [('class_base_id', '=', self.current_class_id.id), ('student_id', '=', student.id)])
            allocated_student_line.unlink()
            new_student_line = self.env['student.base.lines'].create({
                'class_base_id': self.allocate_class_id.id,
                'student_id': student.id,
                'batch_id': self.batch_id.id,
            })
            self.allocate_class_id.write({
                'line_base_ids': [(4, new_student_line.id)]
            })

    # @api.onchange('batch_id')
    # def onchange_batch_id(self):
    #     dd = self.env['logic.students'].search([('batch_id.id', '=', self.batch_id.id)])
    #     # self.student_ids = dd
    #     return {'domain': {'student_ids': [('batch_id.id', 'in', dd.mapped('batch_id').ids)]}}

    # adc = self.env['logic.students'].search([])
    # admission = self.env['res.admission'].search([])
    # print('hhi')
    # # print(self.student_ids)
    # res = []
    # adm = []
    # for i in self:
    #     for j in i.student_ids:
    #         if j.id in adc.ids:
    #             aad = self.env['logic.students'].search([('id', '=', j.id)])
    #             aad.class_id = self.class_id
    #             print(aad, 'ye')
    #         else:
    #             print('no')

    #         res_list = {
    #             'student_id': j.id,
    #             # 'class_base_id': i.class_id.id,
    #             'batch_id': self.batch_id.id,
    #             # 'pending_fee': 100,
    #             # 'ad_id': j.adm_id,
    #         }
    #         res.append((0, 0, res_list))
    # print(adm, 'admission')
    # aa = self.env['logic.base.class'].search([('id', '=', self.class_id.id)])
    # print(res, 'res')
    # for ii in aa:
    #     if aa:
    #         ii.line_base_ids = res


class UpayaAttendanceStudent(models.Model):
    _name = 'students.attendance.upaya'

    name = fields.Char('Name', required=True)
    attendance = fields.Boolean(string="Attendance")
    date = fields.Date('Date')
    stud_id = fields.Integer()
    upaya_std_id = fields.Many2one('logic.students', string="Student", ondelete='cascade')


class YesPlusAttendanceStudent(models.Model):
    _name = 'students.attendance.yes_plus'

    name = fields.Char('Name', required=True)
    day_one = fields.Selection([('full_day', 'Full Day'), ('half_day', 'Half Day'), ('absent', 'Absent')], 'Day 1')
    day_two = fields.Selection([('full_day', 'Full Day'), ('half_day', 'Half Day'), ('absent', 'Absent')], 'Day 2')
    day_three = fields.Selection([('full_day', 'Full Day'), ('half_day', 'Half Day'), ('absent', 'Absent')], 'Day 3')
    day_four = fields.Selection([('full_day', 'Full Day'), ('half_day', 'Half Day'), ('absent', 'Absent')], 'Day 4')
    day_five = fields.Selection([('full_day', 'Full Day'), ('half_day', 'Half Day'), ('absent', 'Absent')], 'Day 5')
    date = fields.Date('Date')
    stud_id = fields.Integer()
    yes_attendance_id = fields.Many2one('logic.students', string="Student", ondelete='cascade')


class BringBuddyStudentAttendance(models.Model):
    _name = 'bring.buddy.students.attendance'

    name = fields.Char('Name', required=True)
    attendance = fields.Boolean(string="Attendance")
    stud_id = fields.Integer()
    bring_std_id = fields.Many2one('logic.students', string="Student", ondelete='cascade')
    date = fields.Date('Date')
