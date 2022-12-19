from odoo import Command
from odoo.tests import tagged
from .common import TestEasyredFsmCommon


@tagged('post_install', '-at_install')
class TestFsmAprovalFlow(TestEasyredFsmCommon):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.material = cls.env['fsm.material'].create({
            'product_id': cls.product_delivered.id,
            'quantity': 5,
            'task_id':cls.task.id,
        })

    def test_fsm_approval_flow(self):

        self.task.with_user(self.project_user).action_approved()
        self.assertFalse(self.task.picking_ids,"Should not be picking because task has not been approved by boss")

        self.task.with_user(self.project_admin).action_approved()
        self.assertFalse(self.task.picking_ids,"Should not create picking because task has not went through first approval")

        self.task.with_user(self.project_user).action_send_to_supervisor()
        self.assertTrue(self.task.to_supervisor,'First approval round')

        self.task.with_user(self.project_admin).action_approved()
        self.assertTrue(self.task.picking_ids,'Picking gets created')

        self.assertEqual(self.material.quantity,self.picking_ids.move_ids_without_package.product_uom_qty,"quantity on material and stock move should be equal")
