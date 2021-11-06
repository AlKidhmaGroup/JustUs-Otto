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
from odoo.exceptions import ValidationError,Warning

class ProjectProject(models.Model):
    _inherit = 'project.project'

    sale_payment_term_ids = fields.One2many('sale.payment.term','project_id', string="Sale Payment Term")


    @api.onchange('sale_payment_term_ids')
    def _onchange_sale_payment_term_ids(self):
        for rec in self:
            pay_term_perc = 0.0
            for pt in rec.sale_payment_term_ids:
                if pt.pay_term_inv_status != 'cancel':
                    pay_term_perc += pt.payment_term_percentage
            if not 0.0 <= pay_term_perc <= 100:
                raise ValidationError(_("Enter total payment term percentage b/w 0 and 100"))




   
