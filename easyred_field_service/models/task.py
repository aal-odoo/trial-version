from odoo import api, fields, models


class ProjectTask(models.Model):
    _inherit = 'project.task'

    material_ids = fields.One2many(
    comodel_name='fsm.material',
    inverse_name='task_id',
    string='Materials'
    )