# -*- coding: utf-8 -*-
##############################################################################
#
#    This module you will Follow flow contract. Report contract. Review the status of a Contract.
#    Check the Contract List. Management Employee, Agreement.
#    Generate contract from Sale Order/ Product (type=Service).
#    It will process the data entered and return a message indicating whether
#    the company is eligible or not.
#
#    Copyright (C) 2020- TODOOWEB.ES (https://www.todooweb.es)
#    @author ToDOO (https://www.linkedin.com/company/todooweb)
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################
{
    'name': "Validation Data Employee",
    'summary': """Validation Data Employee european (SP)""",
    'description': """Validation Data Employee: DNI/NIE. Validation IBAN. Code INEN/SS for model Europe, Spain (SP).
    """,
    'version': '10.0.0.1.1',
    'category': 'Human Resources',
    'license': 'LGPL-3',
    'author': "ToDOO (www.todooweb.es)",
    'website': "https://todooweb.es/",
    'contributors': [
        "Equipo Dev <devtodoo@gmail.com>",
        "Edgar Naranjo <edgarnaranjof@gmail.com>",
        "Tatiana Rosabal <tatianarosabal@gmail.com>",
    ],
    'support': 'devtodoo@gmail.com',
    'depends': [
        'base',
        'sale',
        'account',
        'mail',
        'hr_contract',
        'hr',
        'crm',
        'management_contract'
    ],
    'data': [
        'views/validation_data.xml',
    ],
    'images': [
        'static/description/screenshot_validation.png'
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
