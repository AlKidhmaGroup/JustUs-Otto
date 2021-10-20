from odoo import models,fields


class ModuleName(models.Model):
    _inherit = 'res.company'


    bank_id = fields.Many2one(comodel_name='res.bank', string='Bank')
    bankaccount_id = fields.Many2one(comodel_name='res.partner.bank', string='Bank Account')
    swift = fields.Char(string='Swift')
    iban = fields.Char(string='Iban')
    