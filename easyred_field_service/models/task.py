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
        picking = self.env['stock.picking']
        move = self.env['stock.move']
        picking_type = self.env['stock.picking.type'].search([('code','=','outgoing')])
        cust_location = self.env['stock.location'].search([('usage','=','customer')])
        if len(picking_type)>1:
            picking_type = picking_type[0]
        vals = {
            'partner_id': self.parent_id.id,
            'location_id':picking_type.default_location_src_id.id,
            'picking_type_id':picking_type.id,
            'origin': self.name,
            'service_id': self.id,

        }
        picking_id = picking.create(vals)

        for material in self.material_ids:
            move.create({
                'product_id' :material.product_id.id,
                'name': material.product_id.name,
                'product_uom_qty': material.quantity,
                'product_uom': material.uom_id.id,
                'picking_id': picking_id.id,
                'location_id':picking_type.default_location_src_id.id,
                'location_dest_id': picking_type.default_location_dest_id.id or cust_location.id,
            })
        #look into how sale.order creates stock.picking
        return

    def action_denied(self):
        service = self.copy()
        service.write({
            'name':'Review materials and send to validate',
            'parent_id': self.id,
            'material_ids': [(6,0,material_ids.ids)],
            'to_supervisor':False,
            'description': 'Review materials and send to validate - ' + self.name
        })
        return
