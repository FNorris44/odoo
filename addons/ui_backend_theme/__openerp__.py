# -*- coding: utf-8 -*-
{
    'name': "Theme Customizer",

    'summary': """
        This modules offers you customization in the odoo backend theme according to user's configuration.""",

    'description': """
        Theme Customizer
    """,

    'author': "CIS",
    'website': "http://www.cisin.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'assets.xml',
        'views/views.xml',
        'views/templates.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
