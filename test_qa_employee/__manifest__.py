# -*- encoding: utf-8 -*-
##############################################################################
#
#    This module you will measure the reliability index of a company and the
#    job offers they publish.
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
    'name': "MLearning QA Employee",
    'summary': """Machine Learning QA Employee""",
    'description': """
        Measure the reliability index of a company and the job offers they publish and other functionalities using Machine Learning.
    """,
    'version': '10.1.0.1.2',
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
        'base_vat',
        'mail',
        'hr',
        'crm',
        'sales_team',
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/test_qa_employee.xml',
        'views/test_qa_employee_views.xml',
        'views/templates.xml',
        'data/test_qa_employee_data.xml',
    ],
    'images': [
        'static/description/screenshot_qa.png'
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
