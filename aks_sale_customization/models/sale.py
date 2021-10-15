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


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.model
    def default_get(self, fields):
        res = super(SaleOrder, self).default_get(fields)
        print("res", res)
        if 'rights_and_duties' in fields:
            res['rights_and_duties'] = """Upon the payment of remuneration for the above mentioned services under the terms of this quotation. For agency services in the amount of QAR
            106,700.00 and the threefold implementation by Just us & Otto, all rights of utilization and exploitation are transferred to Provided that the
            contractor is mentioned by name, the client has the publication rights."""
        if 'travel_expenses' in fields:
            res['travel_expenses'] = """
            Necessary travel will be billed after prior consultation, according to receipts. For traveling outside the GCC Region will be billed business class tickets.
            """
        if 'subcontracts' in fields:
            res['subcontracts'] = """
            In the case of commissioning of vendors for services in the name of and billed to Just us & Otto, a price premium of 15% of the corresponding quote net
            amount, the customary agency mark-up, will be charged for the associated risks and expenditures.
            """
        if 'condition_of_payments' in fields:
            res['condition_of_payments'] = """
            The parties to this agreement agree on paying 100% in advance.
            """
        if 'applicable_law_and_jurisdiction' in fields:
            res['applicable_law_and_jurisdiction'] = """
            Any dispute arising out of or in connection with this contract / agreement, including any question regarding its existence, validity or termination, shall be
            referred to and finally resolved by arbitration administered by Qatar International Center for Conciliation and Arbitration (QICCA) in accordance with the
            rules of Qatar International Center for Conciliation and Arbitration (QICCA) in force at the time the request for arbitration is submitted, which rules are
            deemed to be incorporated by reference in this clause.<br/><br/>
            - The applicable law is the law of the State of Qatar.<br/>
            - The seat of the arbitration shall be Qatar.<br/>
            - The Arbitral Tribunal shall consist of a sole arbitrator.<br/>
            - The language of the arbitration shall be English.<br/><br/>
            Any award and/or final decision of the arbitrators shall include a decision on costs, including, without limitation, fees of counsel.
            The Competent Court of the arbitration shall be the First Instance Circuit of the Civil and Commercial Court of the Qatar Financial Centre and, in the
            case of enforcement, the QICCA Competent Judge shall be the Enforcement Judge of the First Instance Circuit of the Civil and Commercial Court of the
            Qatar Financial Centre.
            """
        if 'serverability_clause' in fields:
            res['serverability_clause'] = """
            In the event any provision of this Agreement shall be determined to be invalid, the remainder of this Agreement shall continue in full force and effect.
            """
        if 'integration' in fields:
            res['integration'] = """
            This Agreement constitutes the entire understanding between the parties, and supersedes any prior agreements (whether oral or written) with respect
            thereto. This Agreement may not be amended except in writing, signed by a duly authorized representative of both parties to this Agreement, and failure
            to enforce any provision of this agreement by a party shall not constitute a waiver of rights under that provision
            """
        if 'general' in fields:
            res['general'] = """
            In the event of changes as to the extent of the assignment, fundamental changes of the concept, briefing corrections or changes made after approval,
            changes of the location, changes of the project timing or event date. Just us & Otto reserves the right to re-compute, if applicable. Hereunto, Just us &
            Otto will immediately notify the client. In case of cancellation of the contract, Just us & Otto has the right to invoice all expenses and fees which are
            incurred on the list until date.
            """
        if 'termination_policy' in fields:
            res['termination_policy'] = """
            In case of cancellation 5 days prior to the event, 50% of the charges will be invoiced.<br/>
            For any cancellation less than 5 days before the event, 100% of the charges will be invoiced.
            """
        return res

    job_number = fields.Char(string='Job Number')
    subject = fields.Char(string='Subject')
    quotation_validity = fields.Char(string='Quotation Validity')
    project_manager_id = fields.Many2one('res.partner', string='Project Manager')
    rights_and_duties = fields.Text(string="Rights and Duties")
    travel_expenses = fields.Text(string="Travel Expenses")
    subcontracts = fields.Text(string="Subcontractors ")
    condition_of_payments = fields.Text(string="Conditions of Payment")
    applicable_law_and_jurisdiction = fields.Text(string="Applicable Law, Jurisdiction’s")
    serverability_clause = fields.Text(string="Severability Clause")
    integration = fields.Text(string="Integration")
    general = fields.Text(string="General")
    termination_policy = fields.Text(string="Termination Policy")

    @api.model
    def create(self, vals):
        # if vals.get('number', '/') == '/':
        job_num = self._prepare_job_number(vals)
        vals["job_number"] = job_num
        vals["subject"] = job_num + " -"
        res = super(SaleOrder, self).create(vals)

        return res

    def _prepare_job_number(self, values):
        seq = self.env["ir.sequence"]
        if "company_id" in values:
            seq = seq.with_context(force_company=values["company_id"])
        return seq.next_by_code("job.number.sequence") or "/"


