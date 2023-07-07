# -*- coding: utf-8 -*- 


{
    'name': 'Stock picking packaging control',
    'author': 'Soft-integration',
    'application': False,
    'installable': True,
    'auto_install': False,
    'qweb': [],
    'description': False,
    'images': [],
    'version': '1.0.1.4',
    'category': 'Stock',
    'demo': [],
    'depends': ['stock'],
    'data': [
        'views/stock_picking_views.xml',
        'views/stock_move_views.xml',
        'report/report_deliveryslip.xml'
    ],
    'license': 'LGPL-3',
}
