# -*- coding: utf-8 -*-
import threading
from odoo import api, fields,  tools, models, _
from odoo.exceptions import UserError, AccessError, ValidationError
from odoo.modules import get_module_resource

TYPE_COMPANY = [
	('0', 'Recruitment and Selection'),
	('1', 'Formation HR Consultant'),
	('2', 'Internal Communication Consultant'),
	('3', 'Employer Branding Consultant'),
	('4', 'Performance Evaluation Consultant'),
]

TYPE_SECTOR = [
	('0', 'Primary sector'),
	('1', 'Secondary sector'),
	('2', 'Third sector'),
]

TYPE_SIZE = [
	('0', 'Small company'),
	('1', 'Medium company'),
	('2', 'Big company'),
]

STATE = [
	('draft', 'Draft'),
	('open', 'Open'),
	('close', 'Close'),
	('cancel', 'Cancel'),
]

TYPE_CONTRACT = [
	('10', 'Undefined'),
	('5', 'Scholarship'),
	('1', 'Practices (FCT and similar)'),
	('-10', 'Not specified in the offer'),
]

TYPE_LOCATION = [
	('10', '< 30 min'),
	('5', '30 min < x >= 60 min'),
	('0', '> 60 min'),
]

TYPE_REQUIREMENT = [
	('10', 'Client communicates with clear clarity what he needs and the functions and responsibilities of the employee'),
	('5', 'Client accurately mentions the tools with which it works'),
	('0', 'Client does not specify anything in particular'),
]

TYPE_HOLIDAY = [
	('10', 'Superior to what is established in the agreement'),
	('5', 'Exactly what the agreement indicates'),
	('0', 'What the agreement indicates but forcing them to take them in specific periods'),
]

TYPE_SALARY = [
	('10', 'Salary above market'),
	('5', 'Salary at market level'),
	('0', 'Lower salary at market level'),
	('-10', 'Not specified / outsourced'),
]

TYPE_HOURS = [
	('10', 'Intensive day all year'),
	('5', 'Intensive day in summer'),
	('0', 'Standard office hours all year round'),
]

TYPE_TELECOM = [
	('10', 'Possibility of teleworking every day'),
	('5', 'Possibility of teleworking more than one day a week'),
	('0', 'No telecommuting'),
]

PORTAL_EMPLOYEE = [
	('0', 'Infojobs'),
	('1', 'Infoempleo'),
	('2', 'Indeed'),
	('3', 'LinkedIn'),
	('4', 'Primer empleo'),
	('5', 'Student Job'),
	('6', 'Bizneo'),
	('7', 'Others'),
]

PROFESSIONAL_CATEGORY = [
	('1', 'Engineers and Graduates. Senior management staff'),
	('2', 'Technical Engineers, Experts and Certified Assistants'),
	('3', 'Administrative and Workshop Chiefs'),
	('4', 'Untitled Assistants'),
	('5', 'Administrative Officers'),
	('6', 'Juniors'),
	('7', 'Administrative Assistants'),
	('8', 'First and Second Officers'),
	('9', 'Third Officers and Specialists'),
	('10', 'Pawns'),
	('11', 'Workers under eighteen, whatever their professional category'),
]


class TagCompetitions(models.Model):
	_name = 'tag.competition'
	_inherit = ['mail.thread', 'ir.needaction_mixin']
	_description = 'Competitions'

	def _default_category(self):
		return self.env['res.partner.category'].browse(self._context.get('category_id'))

	name = fields.Char('Name', track_visibility='onchange', required=True, index=True)
	active = fields.Boolean('Active', default='True')
	color = fields.Integer('Color Index', default=0)
	note = fields.Text('Notes')
	type_company = fields.Selection(TYPE_COMPANY, string='Type company', track_visibility='onchange', help='Type Company of the RRHH')
	type_sector = fields.Selection(TYPE_SECTOR, string='Type sector', track_visibility='onchange', help='Type sector')
	type_size = fields.Selection(TYPE_SIZE, string='Type size', track_visibility='onchange', help='Type organization size')
	street = fields.Char('Street')
	street2 = fields.Char('Street2')
	city = fields.Char('City')
	zip = fields.Char('Code zip', onchange='True')
	state_id = fields.Many2one("res.country.state", string='State', ondelete='restrict')
	country_id = fields.Many2one('res.country', string='Country', ondelete='restrict')
	website = fields.Char('Website', help="Website of Competition")
	category_id = fields.Many2one('res.partner.category', string='Category', index=True, track_visibility='onchange', default=_default_category)
	tag_cnae_id = fields.Many2one('tag.cnae.category', string='CNAE', index=True, track_visibility='onchange', help='Groups CNAE.')
	sector_cnae = fields.Many2one('tag.ine.category', 'Sector', track_visibility='onchange')
	template_client = fields.Integer('Template', help='Template on period.')
	offer_ids = fields.One2many('competition.offer', 'competition_id', ondelete='restrict', string='Offers')
	# image: all image fields are base64 encoded and PIL-supported
	image = fields.Binary("Image", attachment=True, help="This field holds the image used as avatar for this contact, limited to 1024x1024px", )
	image_medium = fields.Binary("Medium-sized image", attachment=True, help="Medium-sized image of this contact. It is automatically resized as a 128x128px image. Use this field in form views or some kanban views.")
	image_small = fields.Binary("Small-sized image", attachment=True, help="Small-sized image of this contact. It is automatically resized as a 64x64px image. Use this field anywhere a small image is required.")

	@api.model
	def _get_default_image(self):
		if getattr(threading.currentThread(), 'testing', False) or self._context.get('install_mode'):
			return False
		colorize, img_path, image = False, False, False
		if not image:
			img_path = get_module_resource('base', 'static/src/img', 'avatar.png')
			colorize = True
		if img_path:
			with open(img_path, 'rb') as f:
				image = f.read()
		if image and colorize:
			image = tools.image_colorize(image)
		return tools.image_resize_image_big(image.encode('base64'))

	@api.model
	def create(self, vals):
		if not vals.get('image'):
			vals['image'] = self._get_default_image()
		tools.image_resize_images(vals)
		partner = super(TagCompetitions, self).create(vals)
		return partner


class TagCategoryCNAE(models.Model):
	_name = 'tag.cnae.category'
	_description = 'Categories CNAE'

	name = fields.Char('Name', required=True, index=True)
	code_cnae = fields.Char('Code')
	active = fields.Boolean('Active', default='True')
	code_general = fields.Boolean('General')
	parent_id = fields.Many2one('tag.cnae.category', 'Parent')
	category_ine_id = fields.Many2one('tag.ine.category', 'INE')
	note = fields.Text('Notes')

	# heredo el create para modificar name
	@api.model
	def create(self, vals):
		request = super(TagCategoryCNAE, self).create(vals)
		code_cnae = request.code_cnae
		if request.name:
			request.name = code_cnae + ' - ' + request.name
		if not request.category_ine_id:
			obj_ine_tag = self.env['tag.ine.category'].search([('active', '=', True)])
			for obj_ine in obj_ine_tag:
				code_ine = obj_ine.code_ine
				code_spl = code_ine.replace(" ", "").split(',')
				if code_cnae in code_spl:
					request.category_ine_id = obj_ine.id
		if len(code_cnae) > 2:
			if len(code_cnae) == 4:
				request.code_general = 'True'
				cont_min = code_cnae[:3]
			elif len(code_cnae) == 3:
				cont_min = code_cnae[:2]
			obj_tag = self.env['tag.cnae.category'].search([('code_cnae', '=', cont_min)])
			for obj in obj_tag:
				request.parent_id = obj.id
		if len(code_cnae) == 2:
			list_cnae = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U']
			obj_tag = self.env['tag.cnae.category'].search([('code_cnae', 'in', list_cnae)])
			for obj in obj_tag:
				request.parent_id = obj.id
		return request

	# heredo el write para modificar name
	@api.multi
	def write(self, vals):
		if vals and 'code_cnae' in vals:
			code_cnae = vals.get('code_cnae')
			if len(code_cnae) > 2:
				if len(code_cnae) == 4:
					self.code_general = 'True'
					cont_min = code_cnae[:3]
				elif len(code_cnae) == 3:
					self.code_general = 'False'
					cont_min = code_cnae[:2]
				obj_tag = self.env['tag.cnae.category'].search([('code_cnae', '=', cont_min)])
				for obj in obj_tag:
					self.parent_id = obj.id
			if len(code_cnae) == 2:
				self.code_general = 'False'
				list_cnae = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U']
				obj_tag = self.env['tag.cnae.category'].search([('code_cnae', 'in', list_cnae)])
				for obj in obj_tag:
					self.parent_id = obj.id
		res = super(TagCategoryCNAE, self).write(vals)
		return res


class TagCategoryINE(models.Model):
	_name = 'tag.ine.category'
	_description = 'Categories INE'

	name = fields.Char('Name', required=True, index=True)
	code_ine = fields.Char('Code')
	active = fields.Boolean('Active', default='True')
	note = fields.Text('Notes')


class CompetitionOffer(models.Model):
	_name = 'competition.offer'
	_inherit = ['mail.thread', 'ir.needaction_mixin']
	_description = 'Competition Offer'

	name = fields.Char('Name offer', required=True, index=True)
	active = fields.Boolean('Active', default='True')
	color = fields.Integer('Color Index', default=0)
	competition_id = fields.Many2one('tag.competition', 'Competition')
	state = fields.Selection(STATE, string='State', track_visibility='onchange', help='Status of the offer', default='draft')
	tag_cnae_id = fields.Many2one('tag.cnae.category', string='CNAE', index=True, track_visibility='onchange', help='Groups CNAE.')
	sector_cnae = fields.Many2one('tag.ine.category', 'Sector', track_visibility='onchange')
	name_company = fields.Char('Name company', related='competition_id.name')
	note_type_contract = fields.Selection(TYPE_CONTRACT, string='Type contract', track_visibility='onchange', required='True')
	note_location = fields.Selection(TYPE_LOCATION, string='Location', track_visibility='onchange', help='Customer location relative to your home', required='True')
	note_requirement = fields.Selection(TYPE_REQUIREMENT, string='Requirement', track_visibility='onchange', help='Requirements of the client', required='True')
	note_holiday = fields.Selection(TYPE_HOLIDAY, string='Holiday', track_visibility='onchange', required='True')
	note_salary = fields.Selection(TYPE_SALARY, string='Salary', track_visibility='onchange', help='Salary expectations', required='True')
	note_hours = fields.Selection(TYPE_HOURS, string='Schedule', track_visibility='onchange', required='True')
	note_telecom = fields.Selection(TYPE_TELECOM, string='Telecommuting', track_visibility='onchange', help='Telecommuting (if it makes sense in the professional category of the offer)', required='True')
	note_general = fields.Char('Note', help='Final Note')
	media_general = fields.Float('Average', help='Average Note')
	portal_employee = fields.Selection(PORTAL_EMPLOYEE, string='Portal', track_visibility='onchange')
	category_professional = fields.Many2one("professional.profile", string='Professional profile', ondelete='restrict')
	net_salary = fields.Float('Salary net')
	brut_salary = fields.Float('Salary brut')
	description = fields.Text('Description')
	registered = fields.Integer('Registered number')
	sanity_benefit = fields.Boolean('Private healthcare')
	car_benefit = fields.Boolean('Company car')
	baby_benefit = fields.Boolean('Babycare servicee')
	food_benefit = fields.Boolean('Food ticket')
	other_benefits = fields.Text('Others benefit')
	date_published = fields.Date(string='Published Date', required=True, index=True, default=fields.Datetime.now)
	state_id = fields.Many2one("res.country.state", string='State', ondelete='restrict')
	# calculator
	todo_benefit_count = fields.Integer(compute='_compute_todo_benefit')

	@api.one
	@api.depends('sanity_benefit', 'car_benefit', 'baby_benefit', 'food_benefit', 'other_benefits')
	def _compute_todo_benefit(self):
		tmp_cont = 0
		if self.sanity_benefit:
			tmp_cont += 1
		if self.car_benefit:
			tmp_cont += 1
		if self.baby_benefit:
			tmp_cont += 1
		if self.food_benefit:
			tmp_cont += 1
		if self.other_benefits:
			tmp_cont += 1
		self.todo_benefit_count = tmp_cont

	@api.multi
	def action_set_active(self):
		return self.write({'active': True})

	@api.multi
	def action_set_unactive(self):
		return self.write({'active': False})

	@api.multi
	def action_validate_offer(self):
		for obj_offer in self:
			note = self.calculate_media(obj_offer)
			state = ''
			if note < 5:
				state = "Reprobate"
				self.color = '2'
			elif 5 <= note <= 6:
				state = "Approved"
				self.color = '7'
			elif note <= 7:
				state = "Notable"
				self.color = '9'
			elif 7 < note <= 10:
				state = "Perfect"
				self.color = '5'
			else:
				print("You must enter consistent values")
				exit(1)
			print "The offer is: " + str(state)
			print "With a note of: " + str(note)
			self.note_general = state
			self.media_general = note * 100 / 10
			self.write({'state': 'open'})

	@api.multi
	def action_cancel_offer(self):
		self.write({'state': 'cancel'})

	@api.multi
	def action_draft_offer(self):
		self.write({'state': 'draft'})

	@api.multi
	def action_close_offer(self):
		self.write({'state': 'close'})

	def calculate_media(self, obj_offer):
		paramsList = []
		total = 0
		media = 0
		if obj_offer:
			if obj_offer.competition_id:
				name_company = obj_offer.name_company.strip()
				paramsList.append(name_company)
			if obj_offer.note_type_contract:
				note_type_contract = int(obj_offer.note_type_contract.strip())
				paramsList.append(note_type_contract)
			if obj_offer.note_location:
				note_location = int(obj_offer.note_location.strip())
				paramsList.append(note_location)
			if obj_offer.note_requirement:
				note_requirement = int(obj_offer.note_requirement.strip())
				paramsList.append(note_requirement)
			if obj_offer.note_holiday:
				note_holiday = int(obj_offer.note_holiday.strip())
				paramsList.append(note_holiday)
			if obj_offer.note_salary:
				note_salary = int(obj_offer.note_salary.strip())
				paramsList.append(note_salary)
			if obj_offer.note_hours:
				note_hours = int(obj_offer.note_hours.strip())
				paramsList.append(note_hours)
			if obj_offer.note_telecom:
				note_telecom = int(obj_offer.note_telecom.strip())
				paramsList.append(note_telecom)
			for a in range(2, len(paramsList)):
				total = total + paramsList[a]
			if total == 0:
				print("No hay datos suficientes")
			else:
				media = total / 7
			print "La puntuación media obtenida es:" + str(media)
		return media


class ProfessionalProfile(models.Model):
	_name = 'professional.profile'
	_description = 'Professional Profile'

	name = fields.Char('Name', required=True, index=True)
	active = fields.Boolean('Active', default='True')
	note = fields.Text('Notes')
	code = fields.Char('Code')
