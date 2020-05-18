# -*- coding: utf-8 -*-

from operator import attrgetter
from os import listdir
from os.path import isfile, join, isdir

from odoo import models, fields, api
import odoo


class Module(models.Model):
    _inherit = "ir.module.module"

    obi_upgrades = fields.Integer('Obi Upgrades Counter', help="Used to sort the list on the front end.")

    @api.model
    def get_non_basic(self):
        non_basic_addons = []
        for addons_path in odoo.modules.module.ad_paths:
            onlydirs = [d for d in listdir(addons_path) if isdir(join(addons_path, d))]
            if 'web' in onlydirs and '__manifest__.py' in listdir(join(addons_path, 'web')):
                continue
            non_basic_addons.extend(onlydirs)
        res = []
        x = self.search([['state', 'in', ['installed', 'to upgrade', 'to remove']],
        ['name', 'in', non_basic_addons]], order='obi_upgrades')
        modules = sorted(x, key=attrgetter('obi_upgrades'), reverse=True)


        for module in modules:
            res.append({
                'id': module.id,
                'name': '{0} ({1})'.format(module.name, module.obi_upgrades),
            })
        return res

    @api.model
    def get_reports(self):
        non_basic_addons = []
        for addons_path in odoo.modules.module.ad_paths:
            onlydirs = [d for d in listdir(addons_path) if isdir(join(addons_path, d))]
            if 'web' in onlydirs and '__manifest__.py' in listdir(join(addons_path, 'web')):
                continue
            non_basic_addons.extend(onlydirs)
        res = []
        x = self.search([['state', 'in', ['installed', 'to upgrade', 'to remove']],
        ['name', 'in', non_basic_addons]], order='obi_upgrades')
        modules = sorted(x, key=attrgetter('obi_upgrades'), reverse=True)


        for module in modules:
            reports = self.env['ir.actions.report'].search([('report_name', 'ilike', '{0}%'.format(module.name))])
            for report in reports:
                res.append({
                    'id': module.id,
                    'name': 'http://localhost:8069/report/pdf/{0}/1'.format(report.report_name),
                })
        return res

    def _button_immediate_function(self, function):
        if self.env.context.get('obi_upgrade', False):
            self.obi_upgrades += 1
        return super(Module, self)._button_immediate_function(function)
