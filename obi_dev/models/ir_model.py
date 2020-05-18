# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Model(models.Model):
    _inherit = "ir.model"

    action_ids = fields.One2many('ir.actions.act_window', compute="compute_actions", string="Window Actions")
    menu_ids = fields.One2many(related='action_ids.menu_ids')

    def compute_actions(self):
        for r in self:
            r.action_ids = self.env['ir.actions.act_window'].search([('res_model', '=', r.model)])


class WindowAction(models.Model):
    _inherit = "ir.actions.act_window"

    menu_ids = fields.One2many('ir.ui.menu', compute="compute_menus", string="Menu Items")

    def compute_menus(self):
        for r in self:
            r.menu_ids = self.env['ir.ui.menu'].search([('action', '=', 'ir.actions.act_window,{0}'.format(r.id))])
