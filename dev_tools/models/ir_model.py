# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Model(models.Model):
    _inherit = "ir.model"

    action_ids = fields.One2many('ir.actions.act_window', compute="compute_actions", string="Window Actions")
    menu_ids = fields.One2many('ir.ui.menu', compute="compute_actions")

    def compute_actions(self):
        for r in self:
            r.action_ids = self.env['ir.actions.act_window'].search([('res_model', '=', r.model)])
            r.menu_ids = r.action_ids.menu_ids
