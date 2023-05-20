from odoo import api, fields, models
from datetime import datetime, timedelta
from odoo.exceptions import UserError, ValidationError


class EstateProperties(models.Model):

	_name = "estate.property"
	_description = "Model for Real-Estate Properties"

	name = fields.Char(string='Name')
	description = fields.Text(string='Descrition')
	postcode = fields.Char(string='Post Code')
	date_availability = fields.Date(default=lambda self: datetime.today() + timedelta(days=90), copy=False)
	expected_price = fields.Float()
	selling_price = fields.Float(readonly=True, copy=False)
	bedrooms = fields.Integer(default='2')
	living_area = fields.Integer()
	facades = fields.Integer()
	garage = fields.Boolean()
	garden = fields.Boolean()
	garden_area = fields.Integer()
	garden_orientation = fields.Selection([
		('north', 'North'),
		('south', 'South'),
		('east', 'East'),
		('west', 'West')
	], string='Garden Orientation')
	last_seen = fields.Datetime("Last Seen", default=lambda self: fields.Datetime.now())
	state = fields.Selection([('new', 'New'), ('offer received', 'Offer Received'), ('offer accepted', 'Offer Accepted'), ('sold', 'Sold'), ('cancelled', 'Cancelled')], string='Garden Orientation')
	property_type_id = fields.Many2one('property.type', string='Property Type')
	buyer_id = fields.Many2one('res.partner', string='Buyer', copy=False)
	salesperson_id = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.user.id)
	property_tag_id = fields.Many2many('property.tag', string='Property Tag')
	offer_ids = fields.One2many('property.offers', "partner_id", string="Offers")
	total_area = fields.Float(compute="_compute_area")
	best_offer = fields.Float(string='Best Offer', compute='_compute_best_offer')
	status = fields.Char(default='active', copy=False)




	@api.depends('offer_ids', 'offer_ids.price')
	def _compute_best_offer(self):
		for offer in self:
			offer.best_offer = max(offer.offer_ids.mapped('price')) if offer.offer_ids else 0.0

	@api.depends('living_area', 'garden_area')
	def _compute_area(self):
		for area in self:
			area.total_area = area.garden_area + area.living_area

	@api.onchange('garden')
	def _onchange_garden(self):
		if self.garden:
			self.garden_area = 10
			self.garden_orientation = 'north'

	def button_sold(self):
		for record in self:
			if record.status == 'Cancelled':
				raise UserError("Property is already cancelled and cannot be sold.")
			record.status = 'Sold'

	def button_cancelled(self):
		for record in self:
			if record.status == 'Sold':
				raise UserError("Property is already sold and cannot be cancelled.")
			record.status = 'Cancelled'

	@api.constrains('selling_price', 'expected_price')
	def _check_selling_price(self):
		for record in self:
			if record.selling_price and record.expected_price:
				min_selling_price = record.expected_price * 0.9
				if record.selling_price < min_selling_price:
					raise ValidationError("Selling price cannot be lower than 90% of the expected price.")

	_sql_constraints = [
		('positive_expected_price', 'CHECK (expected_price >= 0)', 'Expected price must be positive.'),
		('positive_selling_price', 'CHECK (selling_price >= 0)', 'Selling price must be positive.'),
		('unique_name', 'UNIQUE(name)', 'Property name must be unique.')
		]
