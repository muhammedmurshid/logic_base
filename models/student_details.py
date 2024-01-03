from odoo import fields, models, api, _
from odoo.exceptions import UserError
import base64
from odoo.modules.module import get_module_resource


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

    upaya_std_ids = fields.One2many('students.attendance.upaya', 'upaya_std_id')
    bring_buddy_attendance_ids = fields.One2many('bring.buddy.students.attendance', 'bring_std_id')
    yes_plus_att_ids = fields.One2many('students.attendance.yes_plus', 'yes_attendance_id')
    # adm_no_id = fields.Many2one('res.admission', string='Admission Number')
    state = fields.Many2one('res.country.state', 'Fed. State', domain="[('country_id', '=?', country)]")
    country = fields.Many2one('res.country')
    stud_id = fields.Integer()
    batch_id = fields.Many2one('logic.base.batch', string='Batch',
                               domain=['&', ('state', '=', 'done'), ('active_state', '=', 'active')])
    # status = fields.Selection([('draft', 'Draft'), ('linked', 'Linked'), ('discontinue', 'Discontinued')],
    #                           default='draft', string='Status', tracking=True)
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
    day_four_cip = fields.Date('Date')
    day_four_cip_attendance = fields.Selection(
        [('full_day', 'Full Day'), ('half_day', 'Half Day'), ('absent', 'Absent')], 'Attendance')
    day_five_cip = fields.Date('Date')
    day_five_cip_attendance = fields.Selection(

        [('full_day', 'Full Day'), ('half_day', 'Half Day'), ('absent', 'Absent')], 'Attendance')
    day_six_cip = fields.Date('Date')
    day_six_cip_attendance = fields.Selection(
        [('full_day', 'Full Day'), ('half_day', 'Half Day'), ('absent', 'Absent')], 'Attendance')
    day_seven_cip = fields.Date('Date')
    day_seven_cip_attendance = fields.Selection(
        [('full_day', 'Full Day'), ('half_day', 'Half Day'), ('absent', 'Absent')], 'Attendance')

    # students Bank details
    bank_name = fields.Char('Bank Name')
    account_number = fields.Char('Account Number')
    ifsc_code = fields.Char('IFSC Code')
    branch = fields.Char('Branch')
    holder_name = fields.Char('Account Holder Name')
    image_field = fields.Binary('Image Field', default=lambda self: self._get_default_image(), readonly=False)
    attempt = fields.Selection(
        selection=[('first', 'First'), ('second', 'Second'), ('third', 'Third'), ('fourth', 'Fourth')],
        string="Attempt")
    recording_status = fields.Selection(selection=[('recording', 'Recording'), ('not_recording', 'Not Recording')],
                                        string="Recording/Not")

    # presentation
    presentation_date = fields.Date('Date')
    presentation_rating = fields.Selection(
        selection=[('0', 'No rating'), ('1', 'Very Poor'), ('2', 'Poor'), ('3', 'Average'), ('4', 'Good'),
                   ('5', 'Very Good')], string="Rating", default='0')
    presentation_feedback = fields.Text(string="Feedback")

    # sfc
    sfc_ids = fields.One2many('students.faculty.club.data', 'sfc_id', string='SFC')

    # mock interview
    mock_date = fields.Date('Date')

    mock_communication_skill = fields.Selection(
        [('0', 'None'), ('1', 'Poor'), ('2', 'Fair'), ('3', 'Good'), ('4', 'Very Good'), ('5', 'Excellent')],
        string='Communication Skill',
    )
    mock_language_skill = fields.Selection(
        [('0', 'None'), ('1', 'Poor'), ('2', 'Fair'), ('3', 'Good'), ('4', 'Very Good'), ('5', 'Excellent')],
        string='Language Skill',
    )
    mock_presentation_skill = fields.Selection(
        [('0', 'None'), ('1', 'Poor'), ('2', 'Fair'), ('3', 'Good'), ('4', 'Very Good'), ('5', 'Excellent')],
        string='Presentation Skill',
    )
    mock_confidence_level = fields.Selection(
        [('0', 'None'), ('1', 'Poor'), ('2', 'Fair'), ('3', 'Good'), ('4', 'Very Good'), ('5', 'Excellent')],
        string='Confidence Level',
    )
    mock_body_language = fields.Selection(
        [('0', 'None'), ('1', 'Poor'), ('2', 'Fair'), ('3', 'Good'), ('4', 'Very Good'), ('5', 'Excellent')],
        string='Body Language',
    )
    mock_dressing_pattern = fields.Selection(
        [('0', 'None'), ('1', 'Poor'), ('2', 'Fair'), ('3', 'Good'), ('4', 'Very Good'), ('5', 'Excellent')],
        string='Dressing Pattern',
    )
    mock_attitude = fields.Selection(
        [('0', 'None'), ('1', 'Poor'), ('2', 'Fair'), ('3', 'Good'), ('4', 'Very Good'), ('5', 'Excellent')],
        string='Attitude',
    )
    mock_quality_of_resume = fields.Selection(
        [('0', 'None'), ('1', 'Poor'), ('2', 'Fair'), ('3', 'Good'), ('4', 'Very Good'), ('5', 'Excellent')],
        string='Quality of Resume',
    )
    mock_friendliness = fields.Selection(
        [('0', 'None'), ('1', 'Poor'), ('2', 'Fair'), ('3', 'Good'), ('4', 'Very Good'), ('5', 'Excellent')],
        string='Friendliness',
    )

    # results

    result_sc = fields.Binary('Result Screenshot')
    qualification_status = fields.Selection(
        [('semi_qualified', 'Semi Qualified'), ('fully_qualified', 'Fully Qualified'),
         ('both_qualified_in_single_window', 'Both Qualified in Single Window')], string='Qualification Status')

    #placements

    placement_company_name = fields.Char('Company Name')
    placement_job_position = fields.Char('Job Position')
    placement_starting_salary = fields.Float('Starting Salary')
    placement_joining_date = fields.Date('Joining Date')

    # FPP

    day_one_fpp = fields.Date('Day 1')
    fpp_present_one = fields.Selection([('present', 'Present'), ('absent', 'Absent')], 'Attendance')
    day_two_fpp = fields.Date('Day 2')
    fpp_present_two = fields.Selection([('present', 'Present'), ('absent', 'Absent')], 'Attendance')
    fpp_certificate = fields.Boolean('FPP Certificate')

    # admission status
    admission_officer = fields.Many2one('res.users', string='Admission Officer')
    admission_fee = fields.Float('Admission Fee')
    pending_amount = fields.Char('Pending Amount')
    adm_fee_due_amount = fields.Float('Due Amount')
    paid_amount = fields.Float('Paid Amount')

    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.user.company_id.currency_id)

    # course fee details
    course_fee = fields.Float('Course Fee')
    paid_course_fee = fields.Float('Paid Course Fee')
    course_due_amount = fields.Float('Due Course Fee')
    course_pending_amount = fields.Char('Pending Course Fee')

    @api.model
    def _get_default_image(self):
        image_path = get_module_resource('hr', 'static/src/img', 'default_image.png')
        return base64.b64encode(open(image_path, 'rb').read())

    def _compute_image(self):
        for student in self:
            # We have to be in sudo to have access to the images
            student_id = self.sudo().env['logic.students'].browse(student.id)
            student.image_field = student_id.image_field

    @api.model
    def create(self, vals):
        if vals.get('reference', _('New')) == _('New'):
            vals['reference'] = self.env['ir.sequence'].next_by_code(
                'logic.students') or _('New')
        res = super(LogicStudents, self).create(vals)
        return res

    def action_open_admission_custom(self):
        print("ooooooooooooooooooo")
        ff = self.env['admission.fee.collection'].search([])

        for i in self:
            return {
                'type': 'ir.actions.act_window',
                'name': 'Admission',
                'res_model': 'admission.fee.collection',
                'view_mode': 'tree,form',
                'target': 'current',
                'domain': [('name.id', '=', i.id)],
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

    # def link_partner(self):
    #     ss = self.env['res.partner'].search([])
    #     if not self.stud_id:
    #         raise UserError('Student do not match')
    #
    #     for i in ss:
    #         print(self.stud_id, 'stud')
    #         print(i.part_id, 'paar')
    #         if i.part_id == self.stud_id:
    #             print('ya')
    #             i.related_student = self.id
    #             self.student_id = i.reference
    #             self.related_partner = i.id
    #             self.status = 'linked'
    #         else:
    #             print('ll')
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

    # def return_draft(self):
    #     self.status = 'draft'

    # @api.onchange('active')
    # def _compute_current_student_status(self):
    #     for rec in self:
    #         if rec.active == False:
    #             rec.status = 'discontinue'
    #             inactive_date = fields.Date.today()
    #             rec.inactive_date = str(inactive_date)
    #             print(rec.inactive_date, 'inactive_date')
    #         else:
    #             rec.status = 'draft'

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
        print(self.batch_id, 'batch')
        already_allocated_stud_ids = []
        for class_id in self.batch_id.class_ids:
            for stud_line in class_id.line_base_ids:
                already_allocated_stud_ids.append(stud_line.student_id.id)
        return {'domain': {
            'student_ids': [('batch_id', '=', self.batch_id.id), ('id', 'not in', already_allocated_stud_ids)]}}

    # @api.depends('batch_id')
    # def get_current_batch_students(self):
    #     print('work')
    #     students = self.env['logic.students'].sudo().search([('batch_id', '=', self.batch_id.id)])
    #     std = []
    #     for stud in students:
    #         print(stud.id, 'student ids')
    #         std.append(stud.id)
    #     print(std, 'std')
    #     domain = [('id', 'in', std)]
    #     return {'domain': {'student_ids': domain}}

    student_ids = fields.Many2many('logic.students', string="Students")
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


class StudentsFacultyClubDatas(models.Model):
    _name = 'students.faculty.club.data'
    _description = 'Students Faculty Club Data'

    sfc_start_time = fields.Datetime('Start Time')
    sfc_end_time = fields.Datetime('End Time')
    sfc_topic = fields.Char('Topic')
    sfc_duration = fields.Float('Duration')
    sfc_id = fields.Many2one('logic.students', string="Student", ondelete='cascade')
