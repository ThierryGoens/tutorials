from odoo import fields, models, api, exceptions

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "this is an accurate description"
    
    name = fields.Char(required=True)
    
class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Regroup the different type of property"
    
    name = fields.Char(required=True)

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "This is a description that explains what it does."

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=fields.Date.add(fields.Date.today(), months=+3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string='Orientation',
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('west', 'West'),
            ('east', 'East'),
            ]
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('canceled', 'Canceled'),
        ],
        required=True,
        default='new',
        copy=False,
    )
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    user_id = fields.Many2one("res.users", string="Salesman", default=lambda self: self.env.user)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id")
    total_area = fields.Integer(compute="_compute_total_area")
    best_offer = fields.Float(compute="_compute_best_offer")
    
    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids")
    def _compute_best_offer(self):
        for record in self:
            record.best_offer = max(record.offer_ids.mapped("price"))
            
    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_orientation = "north"
            self.garden_area = 10
        else:
            self.garden_orientation = ""
            self.garden_area = 0

    def action_set_sold(self):
        for record in self:
            if record.state == "canceled":
                raise exceptions.UserError("A canceled property cannot be sold")
            else:
                record.state = "sold"
        return True

    def action_set_canceled(self):
        for record in self:
            if record.state == "sold":
                raise exceptions.UserError("A sold property cannot be canceled")
            else:
                record.state = "canceled"
        return True
    
    