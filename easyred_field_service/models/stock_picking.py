from odoo import api, fields, models


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    service_id = fields.Many2one(comodel_name='project.task',string='Field Service')
    