from odoo import api, fields, models


class PropertyTag(models.Model):

	_name = "property.tag"
	_description = "model for model relation"

	name = fields.Char(string='Name', required=True)