from odoo import api, fields, models


class FsmMaterial(models.Model):
    _name = 'fsm.material'
    _description = 'FSM Material'

    product_id = fields.Many2one(
        comodel_name='product.product',
        string='Product'
    )
    quantity = fields.Float(string='Quantity')
    qty_on_hand = fields.Float(string='Quantity on Hand', related='product_id.qty_available')#related='product_id.qty_available'
    uom_id = fields.Many2one(
        comodel_name='uom.uom',
        string='UOM',
        related='product_id.uom_id'
    )
    task_id = fields.Many2one(
        comodel_name='project.task',
        string='Task'
    )
