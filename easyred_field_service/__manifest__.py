{
    'name': "Easyred field service",

    'summary': "Easyred field service",

    'description': """
    task id: 3054030
The client is a company that sells field service projects, and they currently 
handle two types of processes that are essential for them to exist in Odoo, 
this dev request is for steps 1-7:

Scenario 1

The final customer submits a ticket with a specific requirement (installation/maintenance service).

Request enters ODOO.

The contract manager follows up on the ticket.

From the ticket, the contract manager creates the task, designates technicians, and adds the materials that are needed.

The contract Manager sends the material request for approval.

The supervisor approves or rejects the material request.

The warehouse receives requests for materials associated with the task.

    """,

    'author': "Odoo, Inc",
    'website': "http://www.odoo.com",
    'category': 'Custom Developments',
    'version': '0.1',
    'license': 'OPL-1',
    'depends': [
        'project',
        'product',
        'industry_fsm_sale',
        'stock'
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/approval_group.xml',
        'views/field_service_form.xml'
    ],
}
