from odoo.addons.industry_fsm_sale.tests.common import TestFsmFlowCommon

class TestEasyredFsmCommon(TestFsmFlowCommon):
    
    @classmethod
    def setUpClass(cls):
        super(TestEasyredFsmCommon, cls).setUpClass()

        cls.project_admin = cls.env['res.users'].create({
            'name': 'Test Project_admin',
            'login': 'Test',
            'email': 'test.project_admin@example.com',
            'groups_id': [(6, 0, [cls.env.ref('easyred_field_service.group_task_approval').id])]
        })

        cls.partner_a = cls.env['res.partner'].create({
            'name': 'partner_a',
            'company_id': False,
        })
        
        cls.task.write({
            'partner_id': cls.partner_a,
            'is_saleorder': False
        })

        cls.product_delivered = cls.env['product.product'].create({
            'name': 'Consommable product delivery',
            'list_price': 40,
            'detailed_type': 'product',
            'invoice_policy': 'delivery',
            'qty_available': 20,
            'uom_id': cls.env.ref('uom.product_uom_unit').id,
        })
