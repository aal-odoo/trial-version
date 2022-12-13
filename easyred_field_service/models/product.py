from odoo import api, fields, models,_
from odoo.exceptions import ValidationError
from odoo.tools import float_round


class Product(models.Model):
    _inherit = 'product.product'

    @api.model
    def _search_fsm_quantity(self, operator, value):
        if not (isinstance(value, int) or (isinstance(value, bool) and value is False)):
            raise ValueError(_('Invalid value: %s', value))
        if operator not in ('=', '!=', '<=', '<', '>', '>=') or (operator == '!=' and value is False):
            raise ValueError(_('Invalid operator: %s', operator))

        task = self._get_contextual_fsm_task()
        if not task:
            return []
        op = 'inselect'
        if value is False:
            value = 0
            operator = '>='
            op = 'not inselect'
        query = """
            SELECT material.product_id
              FROM fsm_matterial material
             WHERE task.id = %s
               AND material.product_uom_qty {} %s
        """.format(operator)
        return [('id', op, (query, (task.id, value)))]

    @api.depends_context('fsm_task_id')
    def _compute_fsm_quantity(self):
        task = self._get_contextual_fsm_task()
        if task:

            material = self.env['fsm.material']
            if self.user_has_groups('project.group_project_user'):
                task = task.sudo()
                material = material.sudo()

            products_qties = material._read_group(
                [('task_id', '=', task.id)],
                ['product_id', 'quantity'], ['product_id'])
            qty_dict = dict([(x['product_id'][0], x['product_uom_qty']) for x in products_qties if x['product_id']])
            for product in self:
                product.fsm_quantity = qty_dict.get(product.id, 0)
        else:
            self.fsm_quantity = False
    
    def set_fsm_quantity(self, quantity):
        task = self._get_contextual_fsm_task()
        if not task or quantity and quantity < 0 or not self.user_has_groups('project.group_project_user'):
            return
        self = self.sudo()
        self.fsm_quantity = float_round(quantity, precision_rounding=self.uom_id.rounding)
        return True
