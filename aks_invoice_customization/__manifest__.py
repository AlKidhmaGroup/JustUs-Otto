# -*- coding: utf-8 -*-
{
    'name': "Invoice Customization",

    'summary': """
    """,

    'description': """
    """,

    'author': "Alkhidma",
    'website': "http://www.alkhidmasystems.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'invoice',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['account','aks_group_access'],

    # always loaded
    'data': [
        'views/account_move.xml',
        'views/company_view.xml',
        'reports/invoice_print_report.xml',
        'reports/invoice_print.xml',
    ],
}
