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

    @api.depends('sale_payment_term_ids', 'sale_payment_term_ids.invoice_id')
    def _get_invoiced(self):
        res = super(SaleOrder, self)._get_invoiced()
        # The invoice_ids are obtained thanks to the invoice lines of the SO
        # lines, and we also search for possible refunds created directly from
        # existing invoices. This is necessary since such a refund is not
        # directly linked to the SO.
        for order in self:
            sale_payment_terms_ids = order.project_id.sale_payment_term_ids
            for payment_term in sale_payment_terms_ids:
                if payment_term.invoice_id and payment_term.invoice_id.id not in order.invoice_ids.ids :
                    order.invoice_ids = [(4,payment_term.invoice_id.id)]

            order.invoice_count = len(order.invoice_ids)



class SalePaymentTerm(models.Model):
    _name = 'sale.payment.term'
    _description = "Model for sale payment"

    name = fields.Char(string="Payment Term")
    payment_term_percentage = fields.Float(string="Percentage")
    amount_to_invoice = fields.Float(string="Amount")

    payment_term_date = fields.Date(string="Date")
    sale_order_id = fields.Many2one('sale.order')
    project_id = fields.Many2one('project.project',"Project")
    invoice_id = fields.Many2one("account.move", string="Invoice")
    is_invoiced = fields.Boolean(string="Invoiced")
    payment_term_date = fields.Date(string="Date")
    pay_term_inv_status = fields.Selection([('invoiced', 'Invoiced'), ('not_invoiced', 'Not Invoiced'), ('cancel', 'Cancelled')], string="Status", default='not_invoiced')
    is_final_invoice = fields.Boolean(string="Final Invoice")
    
    
    def get_invoiceable_lines(self,order_line):
        res = {}
        res = {
            'display_type': order_line.display_type,
            'sequence': order_line.sequence,
            'name': order_line.name,
            'product_id': order_line.product_id.id,
            'product_uom_id': order_line.product_uom.id,
            'discount': order_line.discount,
            'price_unit': order_line.price_unit,
            'tax_ids': [(6, 0,order_line.tax_id.ids)],
            'analytic_account_id': order_line.order_id.analytic_account_id.id,
            'analytic_tag_ids': [(6, 0, order_line.analytic_tag_ids.ids)],
            'product_types':order_line.product_types,
            'product_cost':order_line.product_cost,
            'quantity':order_line.product_uom_qty,
            
        }
#         if optional_values:
#             res.update(optional_values)
        if order_line.display_type:
            res['account_id'] = False
        return res
    
    
    def create_payment_term_invoice(self):

        for pay in self:
            price_unit = 0.0

            final_invoice_count = 0
            for paymen_term in pay.project_id.sale_payment_term_ids:
                if paymen_term.is_final_invoice == True and paymen_term.pay_term_inv_status not in ('cancel') :
                    final_invoice_count += 1
            if final_invoice_count >  1:
                raise ValidationError(_("Multiple of Final Invoice Lines"))


            
            if pay.amount_to_invoice > 0.0  and pay.amount_to_invoice > pay.project_id.sale_order_ref_id.amount_total:
                raise ValidationError(_("Entered Amount is Greater Than Sale Amount"))
            if pay.payment_term_percentage != 0.00 and pay.amount_to_invoice !=0.00:
                raise ValidationError(_(" System accept only one value (Percentage or Amount). So please clear the value from any one of this "))

            if pay.payment_term_percentage < 0.00 and   pay.amount_to_invoice == 0.00:
                raise ValidationError(_(" Negative Percentage "))

            if pay.payment_term_percentage == 0.00 and   pay.amount_to_invoice < 0.00:
                raise ValidationError(_(" Negative Amount "))


            if  pay.is_final_invoice == True:
                total_price_unit = 0.00
                for line_pay in  pay.project_id.sale_payment_term_ids.filtered(lambda p: p.pay_term_inv_status != 'cancel'):
                    
                    if line_pay.payment_term_percentage > 0.00:
                        total_price_unit += (line_pay.project_id.sale_order_ref_id.amount_total * paymen_term.payment_term_percentage) / 100.0
                    
                    if line_pay.amount_to_invoice > 0.00:
                        total_price_unit += line_pay.amount_to_invoice
                if total_price_unit != line_pay.project_id.sale_order_ref_id.amount_total:

                    raise ValidationError(_(" Total Amount of Final is not matching with Sale Amount"))
                
                acc_mov_lines = []
                total_amt_val = {}
#                 total_amt_val = {
#                                     'name': pay.name,
#                                     'analytic_account_id':pay.project_id.sale_order_ref_id and pay.project_id.sale_order_ref_id.analytic_account_id  and \
#                                                           pay.project_id.sale_order_ref_id.analytic_account_id.id or False,
#                                     'quantity': 1,
#                                     'price_unit': pay.project_id.sale_order_ref_id.amount_total,
#                                 
#                                 }
                sale_order_lines = self.env['sale.order.line']
                sale_order_lines = pay.project_id.sale_order_ref_id.order_line
                if pay.project_id.sale_order_ref_id and  sale_order_lines:
                    for order_line in sale_order_lines:
                        total_amt_val = {}
                        total_amt_val = pay.get_invoiceable_lines(order_line)
                        acc_mov_lines.append((0,0,total_amt_val))
                sub_seq =  max(sale_order_lines.mapped('sequence')) if sale_order_lines.mapped('sequence') and max(sale_order_lines.mapped('sequence')) > 0 else 10
                for paymen_term in pay.project_id.sale_payment_term_ids:
                    if  paymen_term.is_final_invoice != True:
                        if paymen_term.pay_term_inv_status not in ('cancel','not_invoiced'):
                            sub_seq += 1
                            price_unit = 0.00
                            if paymen_term.amount_to_invoice > 0.00:
                                price_unit = paymen_term.amount_to_invoice

                            elif  paymen_term.payment_term_percentage > 0.00:
                                price_unit = (paymen_term.project_id.sale_order_ref_id.amount_total * paymen_term.payment_term_percentage) / 100.0
                            
                            move_line = {}
                            move_line = {
                                            'name': paymen_term.name,
                                            'sequence': sub_seq,
                                            
                                            'analytic_account_id':pay.project_id.sale_order_ref_id and pay.project_id.sale_order_ref_id.analytic_account_id  and \
                                                                  pay.project_id.sale_order_ref_id.analytic_account_id.id or False,
                                            'quantity': -1,
                                            'price_unit': price_unit,
                                            
                                        
                                        }
                            acc_mov_lines.append((0,0,move_line))
                            
                               
                
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
                        'sale_payment_term_amt':pay.amount_to_invoice,
                        'invoice_line_ids': acc_mov_lines,
                    })
                    pay.is_invoiced = True
                    pay.pay_term_inv_status = 'invoiced'
                    pay.invoice_id = invoice.id
                        
            elif pay.is_final_invoice == False:
                if pay.project_id.sale_order_ref_id.amount_total !=0.0:
                    price_unit = 0.00
                    if pay.amount_to_invoice > 0.00:
                        price_unit = pay.amount_to_invoice

                    elif  pay.payment_term_percentage > 0.00:
                        price_unit = (pay.project_id.sale_order_ref_id.amount_total * pay.payment_term_percentage) / 100.0
                
                    if not pay.is_invoiced:
                        invoice = self.env['account.move'].create({
                            'partner_id': pay.project_id.partner_id and pay.project_id.partner_id.id or False,
                            'currency_id': pay.project_id.currency_id and pay.project_id.currency_id.id or False,
                            'move_type': 'out_invoice',
                            'invoice_origin': pay.project_id.name,
                            'invoice_date': pay.payment_term_date or fields.date.today(),
                            'project_id':pay.project_id.id,
                            'job_num': pay.project_id.id,
    #                         'res_partner_user_id': pay.project_id.res_partner_user_id and pay.project_id.res_partner_user_id.id or False,
                            'sale_payment_term_id':pay.id,
                            'sale_payment_term_perc':pay.payment_term_percentage,
                            'sale_payment_term_amt':pay.amount_to_invoice,
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

    @api.onchange('amount_to_invoice')
    def _onchange_amount_to_invoice(self):
        for rec in self:
            if not 0.0 <= rec.amount_to_invoice <= rec.project_id.sale_order_ref_id.amount_total:
                raise ValidationError(_("Enter total payment term percentage b/w 0 and 100"))
            
            

    
