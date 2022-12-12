from odoo import api, fields, models,_
from odoo.exceptions import ValidationError


class ProjectTask(models.Model):
    _inherit = 'project.task'

    material_ids = fields.One2many(
    comodel_name='fsm.material',
    inverse_name='task_id',
    string='Materials'
    )

    to_supervisor = fields.Boolean(string='To supervisor', default=False, copied=False)
    parent_id = fields.Many2one(comodel_name='project.task', string='Parent Task')

    def action_send_to_supervisor(self):
        for rec in self:
            rec.to_supervisor = True
    
    def action_approved(self):
        if self.parent_id:
            self.parent_id.action_approved()
        # picking = self.env['stock.picking']

        # vals = {

        # }
        #look into how sale.order creates stock.picking
        raise ValidationError(_('Went thru')) 

    def action_denied(self):
        service = self.copy()
        service.write({
            'name':'Review materials and send to validate',
            'parent_id': self.id
        })
        return
