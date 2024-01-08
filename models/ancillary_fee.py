from odoo import models, fields, api, _


class AncillaryFeeReportBase(models.Model):
    _name = 'ancillary.fee.report.base'
    _description = 'Ancillary Fee Report Base'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    fee_type = fields.Char('Fee Type')
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id)
    amount = fields.Float('Amount')
    ancillary_student_id = fields.Many2one('logic.students', string='Student')
