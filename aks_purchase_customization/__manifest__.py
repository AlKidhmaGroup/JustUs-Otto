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
    'name': "Purchase Customization",
    'version': '15.0.0.1',
    'category': 'Purchase',
    'summary': 'Purchase Customization',
    'live_test_url': 'Add youtube video Link',
    'author': 'Al Khidma Systems',
    'license': 'OPL-1',
    'price': '',
    'currency': 'USD',
    'maintainer': 'Al Khidma Systems',
    'support': 'tech@alkhidmasystems.com',
    'website': "http://alkhidmasystems.com",
    'depends': ['contacts', 'project', 'purchase', ],
    'data': [
        'report/purchase_report.xml',
        'report/purchase_order_template_inherit.xml',
        'views/purchase_inherited_view.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': False,
}

