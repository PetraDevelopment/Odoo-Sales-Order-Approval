{
    'name': 'Approve Sales Order',
    'author':'Petra Software',
    'company': 'Petra Software',
    'maintainer': 'Petra Software',
    'website':'www.t-petra.com',
     'license': 'LGPL-3',
    'summary':'Sale Order Approvel',
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
     'images': ['static/description/banner.png'],
      'price':10,
    'currency':'USD'
}
