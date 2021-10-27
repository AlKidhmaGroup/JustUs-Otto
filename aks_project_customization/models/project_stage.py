# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ProjectProjectStage(models.Model):
    _inherit = 'project.project.stage'

    is_cancel_stage = fields.Boolean(string='Is Cancel Stage')

    @api.constrains('is_cancel_stage')
    def _check_is_cancel_stage(self):
        stage_count = self.env['project.project.stage'].search_count([
            ('is_cancel_stage', '=', True)])
        if stage_count > 1:
            raise ValidationError(_("You can't set more than one cancel stage"))

    @api.model
    def create(self, vals):
        self.check_stage_values(vals)
        res = super(ProjectProjectStage, self).create(vals)
        return res

    def write(self, vals):
        self.check_stage_values(vals)
        res = super(ProjectProjectStage, self).write(vals)
        return res

    def check_stage_values(self, vals):
        if vals.get('sequence'):
            stages = self.env['project.project.stage'].search([])
            for stage in stages:
                if stage.sequence == vals.get('sequence'):
                    raise ValidationError(_("No two stages have the same sequence"))
