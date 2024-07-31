from odoo import fields, models, api, exceptions

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "this is an accurate description"
    _order = 'price desc'
    
    price = fields.Float()
    status = fields.Selection(copy=False, 
                              selection=[
                                  ("accepted", "Accepted"),
                                  ("refused", "Refused")])
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(default=7)
    create_date = fields.Date(default=fields.Date.today())
    date_deadline = fields.Date(compute="_compute_deadline", inverse="_inverse_deadline")
    property_type_id = fields.Many2one(related="property_id.property_type_id", store=True)
    
    _sql_constraints = [
        ('check_price', 'CHECK(price > 0)',
         'The expected price should never be negative nor null.'),
    ]
    
    @api.depends("validity")
    def _compute_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = fields.Date.add(record.create_date, days=+record.validity)
            else:
                record.date_deadline = fields.Date.add(fields.Date.today(), days=+record.validity)
                
    def _inverse_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date).days
            
    def action_accept_offer(self):
        if self.property_id.state == "offer_accepted":
            raise exceptions.UserError("This property has already a selling offer accepted")
        else:
            self.property_id.selling_price = self.price
            self.property_id.buyer_id = self.partner_id
            self.status = "accepted"
            self.property_id.state = "offer_accepted"
        return True

    def action_refuse_offer(self):
        if self.status == "accepted":
            self.property_id.selling_price = 0
        self.property_id.state = 'offer_received'
        self.status = "refused"
        return True
    
    @api.model
    def create(self, vals):
        self.env['estate.property'].browse(vals['property_id']).state = 'offer_received'
        return super().create(vals)
