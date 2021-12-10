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
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    api.model

    # def default_get(self, fields_list):
    #     res = super(classname, self).default_get(fields_list)
    #     vals = [(0, 0, {'field_1': value_1, 'field_2': value_2}),
    #             (0, 0, {'field_1': value_1, 'field_2': value_2})]
    #     res.update({'your_o2m_field': vals})
    #     return res

    @api.model
    def default_get(self, fields_list):
        res = super(SaleOrder, self).default_get(fields_list)
        contents = []
        for cont in self.env.user.company_id.dynamic_content_ids:
            contents.append((0, 0, {'name': cont.name,
                                    'content': cont.content}))
        res.update({'dynamic_content_ids': contents})
        return res

        # if 'rights_and_duties' in fields:
        #     res['rights_and_duties'] = """Upon the payment of remuneration for the above mentioned services under the terms of this quotation. For agency services in the amount of QAR
        #     106,700.00 and the threefold implementation by Just us & Otto, all rights of utilization and exploitation are transferred to Provided that the
        #     contractor is mentioned by name, the client has the publication rights."""
        # if 'travel_expenses' in fields:
        #     res['travel_expenses'] = """
        #     Necessary travel will be billed after prior consultation, according to receipts. For traveling outside the GCC Region will be billed business class tickets.
        #     """
        # if 'subcontracts' in fields:
        #     res['subcontracts'] = """
        #     In the case of commissioning of vendors for services in the name of and billed to Just us & Otto, a price premium of 15% of the corresponding quote net
        #     amount, the customary agency mark-up, will be charged for the associated risks and expenditures.
        #     """
        # if 'condition_of_payments' in fields:
        #     res['condition_of_payments'] = """
        #     The parties to this agreement agree on paying 100% in advance.
        #     """
        # if 'applicable_law_and_jurisdiction' in fields:
        #     res['applicable_law_and_jurisdiction'] = """
        #     Any dispute arising out of or in connection with this contract / agreement, including any question regarding its existence, validity or termination, shall be
        #     referred to and finally resolved by arbitration administered by Qatar International Center for Conciliation and Arbitration (QICCA) in accordance with the
        #     rules of Qatar International Center for Conciliation and Arbitration (QICCA) in force at the time the request for arbitration is submitted, which rules are
        #     deemed to be incorporated by reference in this clause.<br/><br/>
        #     - The applicable law is the law of the State of Qatar.<br/>
        #     - The seat of the arbitration shall be Qatar.<br/>
        #     - The Arbitral Tribunal shall consist of a sole arbitrator.<br/>
        #     - The language of the arbitration shall be English.<br/><br/>
        #     Any award and/or final decision of the arbitrators shall include a decision on costs, including, without limitation, fees of counsel.
        #     The Competent Court of the arbitration shall be the First Instance Circuit of the Civil and Commercial Court of the Qatar Financial Centre and, in the
        #     case of enforcement, the QICCA Competent Judge shall be the Enforcement Judge of the First Instance Circuit of the Civil and Commercial Court of the
        #     Qatar Financial Centre.
        #     """
        # if 'serverability_clause' in fields:
        #     res['serverability_clause'] = """
        #     In the event any provision of this Agreement shall be determined to be invalid, the remainder of this Agreement shall continue in full force and effect.
        #     """
        # if 'integration' in fields:
        #     res['integration'] = """
        #     This Agreement constitutes the entire understanding between the parties, and supersedes any prior agreements (whether oral or written) with respect
        #     thereto. This Agreement may not be amended except in writing, signed by a duly authorized representative of both parties to this Agreement, and failure
        #     to enforce any provision of this agreement by a party shall not constitute a waiver of rights under that provision
        #     """
        # if 'general' in fields:
        #     res['general'] = """
        #     In the event of changes as to the extent of the assignment, fundamental changes of the concept, briefing corrections or changes made after approval,
        #     changes of the location, changes of the project timing or event date. Just us & Otto reserves the right to re-compute, if applicable. Hereunto, Just us &
        #     Otto will immediately notify the client. In case of cancellation of the contract, Just us & Otto has the right to invoice all expenses and fees which are
        #     incurred on the list until date.
        #     """
        # if 'termination_policy' in fields:
        #     res['termination_policy'] = """
        #     In case of cancellation 5 days prior to the event, 50% of the charges will be invoiced.<br/>
        #     For any cancellation less than 5 days before the event, 100% of the charges will be invoiced.
        #     """

    # @api.depends('company_id','company_id.show_vat')
    # def _compute_vat_need(self):
    #     for rec in self:
    #         rec.is_vat_need = False
    #         if rec.company_id:
    #             rec.is_vat_need = rec.company_id.show_vat

    job_number = fields.Char(string='Job Number', track_visibility='always')
    subject = fields.Char(string='Subject', track_visibility='always')
    quotation_validity = fields.Char(string='Quotation Validity', track_visibility='always')
    project_managers_id = fields.Many2one('res.partner', string='Project Manager to be hide')
    project_manager_partner_id = fields.Many2one('res.partner', string='Project Manager')
    rights_and_duties = fields.Text(string="Rights and Duties")
    travel_expenses = fields.Text(string="Travel Expenses")
    subcontracts = fields.Text(string="Subcontractors ")
    condition_of_payments = fields.Text(string="Conditions of Payment")
    applicable_law_and_jurisdiction = fields.Text(string="Applicable Law, Jurisdiction’s")
    serverability_clause = fields.Text(string="Severability Clause")
    integration = fields.Text(string="Integration")
    general = fields.Text(string="General")
    termination_policy = fields.Text(string="Termination Policy")
    project_ref_id = fields.Many2one('project.project', string='Projects', copy=False)
    # is_vat_need = fields.Boolean("Is Vat Need",compute='_compute_vat_need',store=True)
    digital_signature = fields.Binary(string="Digital Signature", copy=False)
    res_partner_signed_by = fields.Many2one('res.partner', string='Signed By')

    dynamic_content_ids = fields.One2many(comodel_name='dynamic.contents', inverse_name='sale_id',
                                          string='Dynamic Content')

    def create_project_on_qt_creation(self, res):
        project_values = {
            'name': res.job_number,
            'partner_id': res.partner_id.id,
            'sale_order_ref_id': res.id,
            'active': True,
            'subject': res.subject,
            'company_id': res.company_id.id,
            'project_manager_partner_id': res.project_manager_partner_id and res.project_manager_partner_id.id or False,
            'sale_order_id': res.id,
        }

        project = self.env['project.project'].create(project_values)
        res.project_ids = [(4, project.id)]
        for line in res.order_line:
            line.project_id = project.id
        res.project_ref_id = project.id
        res.project_id = project.id
        res.create_analytic_acc_on_qt_creation(res)

    def create_analytic_acc_on_qt_creation(self, res):
        res._create_analytic_account(None)
        res.project_id.analytic_account_id = res.analytic_account_id and res.analytic_account_id.id or False

    @api.model
    def create(self, vals):
        if not vals.get('order_line'):
            raise ValidationError(_("You can't create sales order without orderlines"))
        job_num = self._prepare_job_number(vals)
        vals["job_number"] = job_num
        vals["subject"] = job_num + " -"
        res = super(SaleOrder, self).create(vals)

        res.create_project_on_qt_creation(res)
        #         for line in res.order_line:
        #             line._timesheet_service_generation()

        return res

    def _prepare_job_number(self, values):
        seq = self.env["ir.sequence"]
        company = values.get('company_id')
        # if values.get('company_id'):
        #     seq = seq.with_context(force_company=company)
        return seq.next_by_code("job.number.sequence") or "/"

    def write(self, vals):
        res = super(SaleOrder, self).write(vals)
        for rec in self:
            if 'subject' in vals and rec.project_ref_id:
                rec.project_ref_id.subject = vals.get('subject')
            if 'project_manager_partner_id' in vals and rec.project_ref_id:
                rec.project_ref_id.project_manager_partner_id = vals.get('project_manager_partner_id')
        return res

    def action_cancel(self):
        for rec in self:
            result = super(SaleOrder, self).action_cancel()
            if rec.project_ids:
                project_cancel_stage = rec.env['project.project.stage'].search([('is_cancel_stage', '=', True)])
                if project_cancel_stage:
                    for project in rec.project_ids:
                        project.stage_id = project_cancel_stage.id
            return result

    def action_draft(self):
        sequence_list = []
        res = super(SaleOrder, self).action_draft()
        if self.project_ids:
            stages = self.env['project.project.stage'].search([])
            for stage in stages:
                sequence_list.append(stage.sequence)
            min_seq = min(sequence_list)
            project_draft_stage = self.env['project.project.stage'].search([('sequence', '=', min_seq)])
            if project_draft_stage:
                for project in self.project_ids:
                    project.stage_id = project_draft_stage.id
        return res

    def get_total_values(self):
        for rec in self:
            order_line_dict = {}
            total_amount = 0
            section = ''
            for line in rec.order_line:
                total_tax = 0
                if line.product_types == 'common':
                    if line.tax_id:
                        amount = 0
                        total_tax = 0
                        for tax in line.tax_id:
                            amount += int(tax.amount)
                        total_tax = (line.price_subtotal * amount) / 100
                        total_amount += total_tax
                    total_amount += line.price_subtotal

            for line in rec.order_line:
                if line.display_type == 'line_section':
                    section = line.name
                if line.product_types == 'optional':
                    total_amt = 0
                    amount = 0
                    total_tax = 0
                    total_tax_amount = 0
                    for tax in line.tax_id:
                        amount += int(tax.amount)
                    total_tax = (line.price_subtotal * amount) / 100
                    total_tax_amount += total_tax
                    if section not in order_line_dict:
                        total_amt = line.price_subtotal + total_tax_amount + total_amount
                        order_line_dict.update({section: {'total': total_amt}})
                    else:
                        order_line_dict[section]['total'] += line.price_subtotal
                        order_line_dict[section]['total'] += total_tax_amount

            order_line_dict.update({'cmn': total_amount})
            return order_line_dict

    def _create_invoices(self, grouped=False, final=False, date=None):
        moves = super(SaleOrder, self)._create_invoices(grouped, final, date)
        for rec in self:
            if moves:
                moves.job_num = rec.project_ref_id and rec.project_ref_id.id or False
        return moves


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    product_types = fields.Selection([('common', 'Common'), ('optional', 'Optional')],
                                     required=True, default='common', string="Type")
    product_cost = fields.Float("Cost")

    @api.onchange('product_id')
    def product_id_change(self):
        res = super(SaleOrderLine, self).product_id_change()
        for rec in self:
            if rec.product_id:
                rec.product_cost = rec.product_id and rec.product_id.standard_price or 0.0
            if rec.product_id.detailed_type == 'service' or 'consumable':
                rec.name = '-'
        return res

    def get_taxes(self):
        for rec in self:
            taxes = self.tax_id and ', '.join(self.tax_id.mapped('name'))
        return taxes


class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"

    def _create_invoice(self, order, so_line, amount):
        invoice = super(SaleAdvancePaymentInv, self)._create_invoice(order, so_line, amount)
        if invoice:
            invoice.job_num = order.project_ref_id and order.project_ref_id.id or False
        return invoice


class DynamicContents(models.Model):
    _name = 'dynamic.contents'

    name = fields.Char("Name")
    content = fields.Text("Content")
    sale_id = fields.Many2one('sale.order', string='Sale Order Ref')
    sale_id_company = fields.Many2one('res.company', string='Company Ref')
