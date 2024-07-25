from odoo import fields, models, api, exceptions

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Regroup the different type of property"
    _order = 'sequence, name'
    
    name = fields.Char(required=True)
    property_ids = fields.One2many('estate.property', "property_type_id")
    sequence = fields.Integer('Sequence', default=1, help="Used to order types. Lower is better.")
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id')
    offer_count = fields.Integer(compute='_compute_offer_count')
    
    _sql_constraints = [
        ('check_name', 'UNIQUE(name)',
         'The type name should be unique.'),
    ] 
    
    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
