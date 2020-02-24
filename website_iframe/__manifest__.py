# -*- coding: utf-8 -*-
{
    'name': "Iframes Dashboard",
    'summary': """Extend the Odoo Virtual Office with the option to add external iFrames.""",
    'description': """
        This module allows Clients to view external content through iframes by accessing their personal account of the 
        Odoo Virtual Office. This can be used to add content from sources such as external report servers.
    """,
    'version': '10.0.0.0.1',
    'category': 'Website',
    'license': 'LGPL-3',
    'author': "ToDOO",
    'website': "https://todooweb.es/",
    'contributors': [
        "Equipo Dev <devtodoo@gmail.com>",
        "Edgar Naranjo <edgarnaranjof@gmail.com>",
        "Tatiana Rosabal <tatianarosabal@gmail.com>",
    ],
    'support': 'devtodoo@gmail.com',
    'depends': ['base',
                'sale',
                'account',
                'mail',
                'website',
                'website_portal_sale',
                'website_portal',
                ],
    'data': [
        'security/ir.model.access.csv',
        'views/website_iframe.xml',
    ],
    'images': [
        'static/description/iframe_screenshot.png'
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
