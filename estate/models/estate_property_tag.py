from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "this is an accurate description"
    
    name = fields.Char(required=True)