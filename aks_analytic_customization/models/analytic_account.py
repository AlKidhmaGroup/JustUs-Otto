from odoo import models,fields,api
from odoo.osv import expression
    
class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'
    
    
    
    def name_get(self):
        res = super(AccountAnalyticAccount, self).name_get()
        res = []
        for analytic in self:
            name = analytic.name
            if analytic.code:
                name = '[' + analytic.code + '] ' + name
            if analytic.partner_id.commercial_partner_id.name:
                name = name + ' - ' + analytic.partner_id.commercial_partner_id.name
            if analytic.project_ids:
                name = name + ' - ' + analytic.project_ids[0].name 
            res.append((analytic.id, name))
        return res
    
    
    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        if operator not in ('ilike', 'like', '=', '=like', '=ilike', 'not ilike'):
            return super(AccountAnalyticAccount, self)._name_search(name, args, operator, limit, name_get_uid=name_get_uid)
        args = args or []
        if operator == 'ilike' and not (name or '').strip():
            domain = []
        else:
            # `partner_id` is in auto_join and the searches using ORs with auto_join fields doesn't work
            # we have to cut the search in two searches ... https://github.com/odoo/odoo/issues/25175
            partner_ids = self.env['res.partner']._search([('name', operator, name)], limit=limit, access_rights_uid=name_get_uid)
            domain_operator = '&' if operator == 'not ilike' else '|'
            domain = [domain_operator, domain_operator, domain_operator,('code', operator, name), ('name', operator, name), 
                      ('partner_id', 'in', partner_ids),('project_ids.name', operator, name)]
        return self._search(expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid)