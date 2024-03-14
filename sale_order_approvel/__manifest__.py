{
    'name': 'Approve Sales Order',
    'author': 'omar hassan',
    'website': 'www.t-petra.com',
    'summary': 'Odoo 16 Developer',
    'depends': ['base', 'sale', 'mail'],
    'data': [
        'secuirty/sale_order_approvel_secuirty.xml',
        "secuirty/ir.model.access.csv",
        "views/menu.xml",
        "views/quotation_reject.xml",
        'views/sale_approvel_inherit.xml',
        'wizard/reason_wizerd_reject.xml'
    ],
    'application': True,
}
