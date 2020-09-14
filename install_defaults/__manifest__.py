# -*- coding: utf-8 -*-
{
    'name': "Install Common Modules",

    'summary': "",

    'description': """
        Icons made by https://www.flaticon.com/authors/freepik Freepik from https://www.flaticon.com""",
    'author': "Ubay",
    'website': "http://www.github.com/obayit",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'purchase', 'account_accountant', 'hr_holidays', 'hr_payroll', 'purchase', 'sale_management','stock'],

    # always loaded
    'data': [
    ],
}
