# -*- coding: utf-8 -*-

##############################################################################
#
#    Author: Al Kidhma
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
from odoo.exceptions import AccessError, UserError


class ResCompany(models.Model):
    _inherit = 'res.company'

    # @api.model
    # def default_get(self, fields):
    #     res = super(ResCompany, self).default_get(fields)
    #
    #     res.update({'dynamic_content_ids': [
    #         (0, 0, {
    #             'name': 'Rights And Duties',
    #             'content': 'Upon the payment of remuneration for the above mentioned services under the terms of this quotation. For agency services in the amount of QAR XXXXXX and the three fold implementation by Just us & Otto, all rights of utilization and exploitation are transferred to XXXXXXX Provided that the contractor is mentioned by name, the client has the publication rights.',
    #         }),
    #
    #         (0, 0, {
    #             'name': 'General',
    #             'content': 'In the event of changes as to the extent of the assignment, fundamental changes of the concept, briefing corrections or changes made after approval, changes of the location, changes of the project timing or event date. Just us & Otto reserves the right to re-compute, if applicable. Hereunto, Just us & Otto will immediately notify the client. In case of cancellation of the contract, Just us & Otto has the right to invoice all expenses and fees which are incurred on the list until date.',
    #         }),
    #         (0, 0, {
    #             'name': 'Travel Expenses',
    #             'content': 'Necessary travel will be billed after prior consultation, according to receipts. For traveling outside the GCC Region will be billed business class tickets.',
    #         }),
    #         (0, 0, {
    #             'name': 'Subcontractors',
    #             'content': 'In the case of commissioning of vendors for services in the name of and billed to Just us & Otto, a price premium of 15% of the corresponding quote net amount, the customary agency mark-up, will be charged for the associated risks and expenditures.',
    #         }),
    #         (0, 0, {
    #             'name': 'Conditions Of Payment',
    #             'content': 'The parties to this agreement agree on paying 100% in advance.',
    #         }),
    #         (0, 0, {
    #             'name': 'Applicable Law, Jurisdiction',
    #             'content': 'Any dispute arising out of or in connection with this contract / agreement, including any question regarding its existence, validity or termination, shall be referred to and finally resolved by arbitration administered by Qatar International Center for Conciliation and Arbitration (QICCA) in accordance with the rules of Qatar International Center for Conciliation and Arbitration (QICCA) in force at the time the request for arbitration is submitted, which rules are deemed to be incorporated by reference in this clause.<br/><br/> - The applicable law is the law of the State of Qatar.<br/> - The seat of the arbitration shall be Qatar.<br/> - The Arbitral Tribunal shall consist of a sole arbitrator.<br/> - The language of the arbitration shall be English.<br/><br/> Any award and/or final decision of the arbitrators shall include a decision on costs, including, without limitation, fees of counsel. <br/><br/> The Competent Court of the arbitration shall be the First Instance Circuit of the Civil and Commercial Court of the Qatar Financial Centre and, in the case of enforcement, the QICCA Competent Judge shall be the Enforcement Judge of the First Instance Circuit of the Civil and Commercial Court of the Qatar Financial Centre.',
    #         }),
    #         (0, 0, {
    #             'name': 'Serverability Clause',
    #             'content': 'In the event any provision of this Agreement shall be determined to be invalid, the remainder of this Agreement shall continue in full force and effect.',
    #         }),
    #         (0, 0, {
    #             'name': 'Integration',
    #             'content': 'This Agreement constitutes the entire understanding between the parties, and supersedes any prior agreements (whether oral or written) with respect thereto. This Agreement may not be amended except in writing, signed by a duly authorized representative of both parties to this Agreement, and failure to enforce any provision of this agreement by a party shall not constitute a waiver of rights under that provision',
    #         }),
    #         (0, 0, {
    #             'name': 'Termination Policy',
    #             'content': 'In case of cancellation 5 days prior to the event, 50% of the charges will be invoiced.<br/>For any cancellation less than 5 days before the event, 100% of the charges will be invoiced.',
    #         }),
    #     ]})
    #
    #     return res

    # quotation_footer = fields.Binary(string=" Quotation Footer")
    # is_a_and_a = fields.Boolean(string='A & A')
    dynamic_content_ids = fields.One2many(comodel_name='dynamic.contents',inverse_name='sale_id_company',string='Dynamic Content')

    
