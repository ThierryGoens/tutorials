from odoo import fields, models


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "this is an accurate description"
    
    price = fields.Float()
    status = fields.Selection(copy=False, 
                              selection=[
                                  ("accepted", "Accepted"),
                                  ("refused", "Refused")])
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)