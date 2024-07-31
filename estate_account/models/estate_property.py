from odoo import fields, models, Command


class EstateProperty(models.Model):
    _inherit = "estate.property"
    
    def action_set_sold(self):
        partner = self.buyer_id.id
        move_type = 'out_invoice'
        house_name = self.name
        commission = self.selling_price * 0.06 
        self.env['account.move'].create(
            {
                'partner_id': partner,
                'move_type': move_type,
                'invoice_line_ids': [
                    Command.create({
                        'name': house_name,
                        'quantity': 1,
                        'price_unit': commission
                    }),
                    Command.create({
                        'name': 'Administrative fees',
                        'quantity': 1,
                        'price_unit': 100.00
                    })
                ]
            }
        )
        return super().action_set_sold()