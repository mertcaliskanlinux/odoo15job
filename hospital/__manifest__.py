# -*- coding: utf-8 -*-

{
    'name': 'Hostpital Training v1',
    'version': '1.0',
    'category': 'hospital',
    'author': 'Mert Ç.',
    'sequence': -100,
    'summary': """Hostpital Management Mert Ç.""",
    'description': "",
    'depends': ['sale','base'],
    'data': [
        'security/ir.model.access.csv',
        'views/menu.xml',
        'views/patient_view.xml',
        'views/doctor_view.xml',
        
    ],
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
