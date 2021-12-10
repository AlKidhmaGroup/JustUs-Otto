# -*- coding: utf-8 -*-

##############################################################################
#
#    Author: ALKIDHMA
#    you can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#
#    It is forbidden to publish, distribute, sublicense, or sell copies
#    of the Software or modified copies of the Software.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    GENERAL PUBLIC LICENSE (LGPL v3) along with this program.
#    If not, see <https://www.gnu.org/licenses/>.
#
##############################################################################

from odoo import models, fields, api


class ProjectProject(models.Model):
    _inherit = 'project.project'

    subject = fields.Char(string="Subject", copy=False)
    sale_order_ref_id = fields.Many2one('sale.order', string='Sale Order Ref')
    project_manager_id = fields.Many2one('res.partner', string='Project Manager to hide')
    project_manager_partner_id = fields.Many2one('res.partner', string='Project Manager',track_visibility='always')

    @api.model
    def create(self, vals):
        if self.sale_order_ref_id:
            vals['sale_order_id'] = self.sale_order_ref_id
        res = super(ProjectProject, self).create(vals)
        return res

    def open_so_smart_button_project(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Sale Order',
            'view_mode': 'tree,form',
            'res_model': 'sale.order',
            'domain': [('id', '=', self.sale_order_ref_id.id)],
            'context': "{'create': False}"
        }
