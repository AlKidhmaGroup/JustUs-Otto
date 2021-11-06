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


from odoo import models, fields, api,_

class AccountMove(models.Model):
    _inherit = 'account.move'

    project_id = fields.Many2one(comodel_name="project.project", string="Project", ondelete="cascade", copy=False)
    sale_payment_term_id = fields.Many2one('sale.payment.term',string="Sale Payment Term")
    sale_payment_term_perc = fields.Float(string="Sale Payment Term Percentage")

    def _post(self, soft=True):
        res = super(AccountMove, self)._post()
        for mov in res:
            for line in mov.line_ids:
                if line.account_id.user_type_id.type in ('receivable', 'payable'):
                    if  mov.sale_payment_term_perc and mov.project_id:
                        line.name = str(mov.sale_payment_term_perc) + " % of " + mov.project_id.name + " - " + mov.project_id.sale_order_ref_id.name + " - " + mov.name
        return res

    def write(self, vals):
        if vals.get('state') and vals.get('state') == 'cancel':
            self.sale_payment_term_id.pay_term_inv_status = 'cancel'
        return super(AccountMove, self).write(vals)


