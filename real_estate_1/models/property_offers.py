from datetime import timedelta
from odoo import api, fields, models
from odoo.exceptions import UserError


class PropertyOffers(models.Model):

    _name = "property.offers"
    _rec_name = "partner_id"
    _description = "model for model relation One2many"

    price = fields.Float()
    status = fields.Selection([('accepted','Accepted'), ('rejected', 'Rejected')], copy=False)
    partner_id = fields.Many2one("res.partner", string="Partner ID", required=True)
    property_id = fields.Many2one("estate.property", string="Property ID", required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse='_inverse_date_deadline')
    created_date = fields.Date()

    @api.depends('validity', 'created_date')
    def _compute_date_deadline(self):
        for date in self:
            if date.validity and date.created_date:
                date.date_deadline = date.created_date + timedelta(days=date.validity)
            else:
                date.date_deadline = False

    def _inverse_date_deadline(self):
        for date in self:
            if date.date_deadline and date.created_date:
                delta = date.date_deadline - date.created_date
                date.validity = delta.days

    def button_accepted(self):
        for record in self:
            if record.status == 'Rejected':
                raise UserError("offer is already accepted.")
            record.status = 'Accepted'

    def button_rejected(self):
        for record in self:
            if record.status == 'Accepted':
                raise UserError("offer is already rejected.")
            record.status = 'Rejected'

    _sql_constraints = [
        ('positive_offer_price', 'CHECK (price >= 0)', 'Offer price must be positive.')
    ]
