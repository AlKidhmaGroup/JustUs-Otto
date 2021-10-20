from odoo import models,fields


class Account_move(models.Model):
    _inherit = 'account.move'
    
    
    lpo_num = fields.Char(string='LPO Number')
    job_num = fields.Many2one(comodel_name='project.project', string='Job Number',copy=False,track_visibility='always')
    brand = fields.Char(string='Brand')
    assembled_by = fields.Many2one('res.partner', string='Assembled By')
    invoice_you_for = fields.Char(string='We Invoice You For')
    payment_term_id = fields.Many2one('account.payment.term', string='Payment Term')
    
    def incl_vat_amount(self,subtotal,tax):
        amount = 0
        for i in tax:
            amount += int(i.amount)
        vat_amount = (subtotal * amount)/100
        total_amount = vat_amount + subtotal        
        return total_amount
    
    def tax_percent(self,tax):
        amount = 0
        for i in tax:
            amount += int(i.amount)
        return amount