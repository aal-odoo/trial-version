from odoo import api, fields, models,_
from odoo.exceptions import ValidationError


class Product(models.Model):
    _inherit = 'product.product'

    def set_fsm_quantity(self, quantity):
        task = self._get_contextual_fsm_task()
        # project user with no sale rights should be able to change material quantities
        if not task or quantity and quantity < 0 or not self.user_has_groups('project.group_project_user'):
            return
        self = self.sudo()
        return ValidationError(_("in product fsm quantity"))