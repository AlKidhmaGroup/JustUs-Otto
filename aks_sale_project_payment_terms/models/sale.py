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

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError,Warning


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    
    sale_payment_term_ids = fields.One2many('sale.payment.term','sale_order_id', string="Sale Payment Term")
    
    
    def get_project_payment_terms(self):
        for rec in self:
            rec.sale_payment_term_ids.write({'project_id':rec.project_id and rec.project_id.id or False})
        
    def action_confirm(self):
        for rec in self:
            if not rec.sale_payment_term_ids:
                raise ValidationError(_("Please Add Sale Payment Terms!!"))
        res = super(SaleOrder, self).action_confirm()
        for sale in self:
            sale.get_project_payment_terms()
        return res
    
    


class SalePaymentTerm(models.Model):
    _name = 'sale.payment.term'
    _description = "Model for sale payment"

    name = fields.Char(string="Payment Term")
    payment_term_percentage = fields.Float(string="Percentage")
    payment_term_date = fields.Date(string="Date")
    sale_order_id = fields.Many2one('sale.order')
    project_id = fields.Many2one('project.project',"Project")
    invoice_id = fields.Many2one("account.move", string="Invoice")
    is_invoiced = fields.Boolean(string="Invoiced")
    payment_term_date = fields.Date(string="Date")
    pay_term_inv_status = fields.Selection([('invoiced', 'Invoiced'), ('not_invoiced', 'Not Invoiced'), ('cancel', 'Cancelled')], string="Status", default='not_invoiced')

    def create_payment_term_invoice(self):
        # sale_order_rec = self.env['sale.order'].search([('sale_payment_term_ids', '!=', False)])
        # for rec in sale_order_rec:
        # for pay in rec.sale_payment_term_ids:
        for pay in self:
            # if fields.date.today() == pay.payment_term_date:
            price_unit = 0.0
            if pay.project_id.sale_order_ref_id.amount_total !=0.0:
                price_unit = (pay.project_id.sale_order_ref_id.amount_total * pay.payment_term_percentage) / 100.0
            if pay.payment_term_percentage:
                if not pay.is_invoiced:
                    invoice = self.env['account.move'].create({
                        'partner_id': pay.project_id.partner_id and pay.project_id.partner_id.id or False,
                        'currency_id': pay.project_id.currency_id and pay.project_id.currency_id.id or False,
                        'move_type': 'out_invoice',
                        'invoice_origin': pay.project_id.name,
                        'invoice_date': pay.payment_term_date or fields.date.today(),
                        'project_id':pay.project_id.id,
#                         'res_partner_user_id': pay.project_id.res_partner_user_id and pay.project_id.res_partner_user_id.id or False,
                        'sale_payment_term_id':pay.id,
                        'sale_payment_term_perc':pay.payment_term_percentage,
                        'invoice_line_ids': [(0, 0, {
                            'name': pay.name,
                            'analytic_account_id':pay.project_id.sale_order_ref_id and pay.project_id.sale_order_ref_id.analytic_account_id  and \
                                                  pay.project_id.sale_order_ref_id.analytic_account_id.id or False,
                            'quantity': 1,
                            'price_unit': price_unit,
                            
                        })],
                    })
                    pay.is_invoiced = True
                    pay.pay_term_inv_status = 'invoiced'
                    pay.invoice_id = invoice.id
            else:
                raise ValidationError(_("Enter total payment term percentage b/w 0 and 100"))
    
    
    @api.onchange('payment_term_percentage')
    def _onchange_payment_term_percentage(self):
        for rec in self:
            if not 0.0 <= rec.payment_term_percentage <= 100.0:
                raise ValidationError(_("Enter total payment term percentage b/w 0 and 100"))

    