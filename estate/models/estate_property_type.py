from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Regroup the different type of property"
    
    name = fields.Char(required=True)