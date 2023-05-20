from odoo import api, fields, models


class PropertyType(models.Model):

	_name = "property.type"
	_description = "model for model relation"

	name = fields.Char(string='Name', required=True)