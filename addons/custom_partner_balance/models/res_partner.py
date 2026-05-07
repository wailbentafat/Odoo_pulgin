from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    balance = fields.Float(string="Customer Balance")