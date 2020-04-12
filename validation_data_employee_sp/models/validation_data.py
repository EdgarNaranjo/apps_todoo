# -*- coding: utf-8 -*-

import logging

from odoo import api, fields, models, _
from odoo.exceptions import UserError, AccessError, ValidationError
from datetime import date, datetime, time, timedelta


def verify_iban(cuenta):
    letras = {"A": 10, "B": 11, "C": 12, "D": 13, "E": 14, "F": 15, "G": 16, "H": 17, "I": 18, "J": 19, "K": 20,
              "L": 21, "M": 22, "N": 23, "O": 24, "P": 25, "Q": 26, "R": 27, "S": 28, "T": 29, "U": 30, "V": 31,
              "W": 32, "X": 33, "Y": 34, "Z": 35}
    cuenta = cuenta.strip().upper()
    cuenta = cuenta.replace(" ", "").replace("-", "");
    if len(cuenta) == 24:
        valorLetra1 = letras[cuenta[0:1]]
        valorLetra2 = letras[cuenta[1:2]]
        siguienteNumeros = cuenta[2:4]
        valor = "%s%s%s%s" % (cuenta[4:], valorLetra1, valorLetra2, siguienteNumeros)
        if (int(valor) % 97) == 1:
            return True
        else:
            return False


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    iban = fields.Char('IBAN', size=24)
    identification_id = fields.Char('No. identification', size=12)
    mobile_phone = fields.Char('Mobile', size=9)
    pnafss = fields.Char('PNAFSS', size=2)
    nafss = fields.Char('NAFSS', size=10)
    document_type = fields.Selection([
        ('dni', 'DNI'),
        ('nie', 'NIE'),
        ('pass', 'Passport')], 'Type document', track_visibility='onchange')
    age = fields.Integer('Age')

    @api.model
    def create(self, vals):
        # Repeat identification
        if vals.get('identification_id'):
            repeated_identification = self.env['hr.employee'].search([('identification_id', '=', vals.get('identification_id'))])
            if repeated_identification:
                raise UserError(_('This identification is used by another employee'))
        if vals.get('mobile_phone'):
            mobile = vals.get('mobile_phone')
            if not (len(mobile) <= 9 and (mobile[0] == '6' or mobile[0] == '7')):
                raise UserError(_('Take a look over the mobile, the format does not look as correct'))
        if vals.get('birthday'):
            datetime_obj = datetime.strptime(vals.get('birthday'), '%Y-%m-%d').date()
            if (date.today() - datetime_obj).days > 31025 or datetime_obj >= date.today():
                raise UserError(_('Take a look over the Birthday date, does not look correct'))
        if (vals.get('identification_id') or self.identification_id) and (vals.get('document_type') or self.document_type):
            identification_id = False
            document_type = False
            if vals.get('identification_id'):
                identification_id = vals.get('identification_id')
            else:
                identification_id = self.identification_id
            if vals.get('document_type'):
                document_type = vals.get('document_type')
            else:
                document_type = self.document_type
            if document_type == 'nie':
                if len(identification_id) != 9:
                    raise UserError(_('The NIE structure is not correct'))
                elif not (identification_id[0] == 'X' or identification_id[0] == 'Y'):
                    raise UserError(_('The NIE structure is not correct'))
            if document_type == 'dni':
                if len(identification_id) != 9:
                    raise UserError(_('The DNI structure is not correct'))
                elif not (identification_id[0:8].isdigit() and identification_id[8].isdigit() == False):
                    raise UserError(_('The DNI structure is not correct'))
            if vals.get('pnafss'):
                if not len(vals.get('pnafss')) == 2:
                    raise UserError(_('Take a look over the PNAFSS, does not look as correct'))
                if not vals.get('pnafss').isdigit():
                    raise UserError(_('PNAFSS, its not digits'))
            if vals.get('nafss'):
                if not len(vals.get('nafss')) == 10:
                    raise UserError(_('Take a look over the NAFSS, does not look as correct'))
                if not vals.get('nafss').isdigit():
                    raise UserError(_('NAFSS, its not digits'))
            if vals.get('iban'):
                iban = vals.get('iban')
                validation = verify_iban(iban)
                if validation:
                    if not self.mapped('bank_account_id'):
                        account_id = self.mapped('bank_account_id')
                        account_id.create({'acc_number': iban})
                else:
                    raise UserError(_('Verify the IBAN number, does not look as correct'))
            if vals.get('birthday'):
                datetime_obj = datetime.strptime(vals.get('birthday'), '%Y-%m-%d').date()
                if (date.today() - datetime_obj).days > 31025 or datetime_obj >= date.today():
                    raise UserError(_('Take a look over the Birthday date, does not look correct'))
        sup = super(HrEmployee, self).create(vals)
        return sup

    @api.multi
    def write(self, vals):
        # Repeat identification
        if vals.get('identification_id'):
            repeated_identification = self.env['hr.employee'].search([('identification_id', '=', vals.get('identification_id'))])
            if repeated_identification:
                raise UserError(_('This identification is used by another employee'))
        if vals.get('mobile_phone'):
            mobile = vals.get('mobile_phone')
            if not (len(mobile) <= 9 and (mobile[0] == '6' or mobile[0] == '7')):
                raise UserError(_('Take a look over the mobile, the format does not look as correct'))
        if vals.get('birthday'):
            datetime_obj = datetime.strptime(vals.get('birthday'), '%Y-%m-%d').date()
            if (date.today() - datetime_obj).days > 31025 or datetime_obj >= date.today():
                raise UserError(_('Take a look over the Birthday date, does not look correct'))
        if (vals.get('identification_id') or self.identification_id) and (vals.get('document_type') or self.document_type):
            identification_id = False
            document_type = False
            if vals.get('identification_id'):
                identification_id = vals.get('identification_id')
            else:
                identification_id = self.identification_id
            if vals.get('document_type'):
                document_type = vals.get('document_type')
            else:
                document_type = self.document_type
            if document_type == 'nie':
                if len(identification_id) != 9:
                    raise UserError(_('The NIE structure is not correct'))
                elif not (identification_id[0] == 'X' or identification_id[0] == 'Y'):
                    raise UserError(_('The NIE structure is not correct'))
            if document_type == 'dni':
                if len(identification_id) != 9:
                    raise UserError(_('The DNI structure is not correct'))
                elif not (identification_id[0:8].isdigit() and identification_id[8].isdigit() == False):
                    raise UserError(_('The DNI structure is not correct'))
            if vals.get('pnafss'):
                if not len(vals.get('pnafss')) == 2:
                    raise UserError(_('Take a look over the PNAFSS, does not look as correct'))
                if not vals.get('pnafss').isdigit():
                    raise UserError(_('PNAFSS, its not digits'))
            if vals.get('nafss'):
                if not len(vals.get('nafss')) == 10:
                    raise UserError(_('Take a look over the NAFSS, does not look as correct'))
                if not vals.get('nafss').isdigit():
                    raise UserError(_('NAFSS, its not digits'))
            if vals.get('iban'):
                iban = vals.get('iban')
                validation = verify_iban(iban)
                if not validation:
                    raise UserError(_('Verify the IBAN number, does not look as correct'))
            if vals.get('birthday'):
                datetime_obj = datetime.strptime(vals.get('birthday'), '%Y-%m-%d').date()
                if (date.today() - datetime_obj).days > 31025 or datetime_obj >= date.today():
                    raise UserError(_('Take a look over the Birthday date, does not look correct'))
        sup = super(HrEmployee, self).write(vals)
        return sup

    @api.onchange('birthday')
    def onchange_age(self):
        for obj_contract in self:
            age = ''
            if obj_contract.birthday:
                dob = datetime.strptime(obj_contract.birthday, '%Y-%m-%d')
                today = date.today()
                age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
                obj_contract.age = int(age)
