{
    'name' : 'Auto service',
    'version' : '0.9.5 beta',
    'author' : 'Antoan Georgieff',
    'category': 'Auto sevice',
    'license' : 'AGPL-3',
    'website': 'http://www.avtosmetalo.com',
    'summary': 'Auto sevice managment solution for odoo',
    'description': 'Auto sevice vertical solution',
    # any module necessary for this one to work correctly
    'depends': ['base', 'mail', 'project', 'stock'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        #'views.xml',
        'templates.xml',
        'views/autoservice.xml',
        'security/ir.model.access.csv',
        #'security/autoservice_security.xml',
        #'controllers/controllers.py',
        #'data/autoservice_data.xml',
        'data/autoservice_sequence.xml',
        'data/autoservice_stages_data.xml',
        #'data/autoservice_contract_data.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/autoservice_demo.xml',
    ],

    'installable' : True,
    'application' : True,
}
