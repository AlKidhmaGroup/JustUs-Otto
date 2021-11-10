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


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    job_number = fields.Many2one('project.project', string="Job Number", copy=False,track_visibility="always")
    date = fields.Datetime(string="Date", copy=False)
    subject = fields.Char(string="Subject", copy=False)
    dynamic_content = fields.Html(string="Dynamic Content", copy=False)
    office_finance_manager = fields.Many2one('res.partner', string="Office & Finance Manager", copy=False)
    delivery_date = fields.Datetime(string="Delivery Date", copy=False)
    delivery_place = fields.Char(string="Delivery Place", copy=False)

    @api.onchange('job_number')
    def _onchange_job_number(self):
        if self.job_number:
            self.subject = self.job_number.name + ' - '

    @api.model
    def default_get(self, fields):
        result = super(PurchaseOrder, self).default_get(fields)
        if 'dynamic_content' in fields:
            dynamic_test = """
                This order was electronically generated and is valid without signature. It is effective with the customers' reception of an order
                acceptance.<br/><br/>
                
                Invoices can only be handled and balanced stating the complete address of us, reference (PO) number and job number,
                account manager name as mentioned in this PO and your (Supplier) complete address & complete bank details with IBAN no.<br/><br/>
                
                Subject to our general terms and conditions.<br/><br/>
                
                All invoices against this PO need to be submitted with complete details via email to Joby Thomas,
                <joby@justusandotto.com> Finance Manager. Any other submissions will be not accepted or processed.
            """
            result['dynamic_content'] = dynamic_test
        return result
    
    def _prepare_invoice(self):
        
        res  = super(PurchaseOrder, self)._prepare_invoice()
        for rec in self:
            res.update({'job_num':rec.job_number and rec.job_number.id or False})
        return res

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'
    
    
    
    def get_taxes(self):
        for rec in self:
            taxes = self.taxes_id and ', '.join(self.taxes_id.mapped('name'))
            # if rec.taxes_id:
            #     for tax in rec.taxes_id:
        return taxes