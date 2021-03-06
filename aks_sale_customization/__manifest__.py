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

{
    'name': "Sale Customization",
    'version': '15.0.0.3',
    'category': 'Sale',
    'summary': 'Sale Customization',
    'live_test_url': 'Add youtube video Link',
    'author': 'Al Khidma Systems',
    'license': 'OPL-1',
    'price': '',
    'currency': 'USD',
    'maintainer': 'Al Khidma Systems',
    'support': 'tech@alkhidmasystems.com',
    'website': "http://alkhidmasystems.com",
    'depends': [
        'sale_project', 'aks_project_customization','aks_group_access'
    ],
    'data': [
        'data/sequence_data.xml',
        'security/ir.model.access.csv',
        'report/sale_report_templates.xml',
        # 'views/product_views.xml',
        'views/product_template_view.xml',
        'views/sales_order.xml',
        'views/res_company.xml',
        
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': False,
}
