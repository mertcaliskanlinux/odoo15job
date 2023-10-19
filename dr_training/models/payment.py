
from odoo import models, fields


class Payment(models.Model):

    _inherit = 'account.payment'

    appointment_id = fields.Many2one('dr_patients.appointment', string='Appointment') # Randevu /* Appointment */




    

