from odoo import models, fields, api, _


class LogicBranches(models.Model):
    _name = 'logic.base.branches'
    _description = 'Branch'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'branch_name'

    branch_name = fields.Char()

    def _compute_display_name(self):
        for record in self:
            record.display_name = 'Branch' + '-' + record.branch_name
