<<<<<<< HEAD
from odoo import api, fields, models


class Payment(models.Model):
    _inherit = "account.payment"

    appointment_id = fields.Many2one('dr_patients.appointment', string='Appointment')  # One2many another
    appointment_ids = fields.One2many('dr_patients.appointment', 'account_payment_id', compute='_compute_appointment_count')
    appointment_count = fields.Integer(string='Appointment', compute='_compute_appointment_count')
=======

from odoo import models, fields,api,_


class Payment(models.Model):

    _inherit = 'account.payment'

    appointment_id = fields.Many2one('dr_patients.appointment', string='Appointment') # Randevu /* Appointment */
    appointment_ids = fields.One2many('dr_patients.appointment', 'account_payment_id', string='Appointments') # Randevular /* Appointments */
    appointment_count = fields.Integer(string='Appointment Count', compute='_compute_appointment_count') # Randevu Sayısı /* Appointment Count */
        
>>>>>>> mert1

    @api.depends('appointment_id')
    def _compute_appointment_count(self):
        for rec in self:
<<<<<<< HEAD
            rec.appointment_ids = self.env['dr_patients.appointment'].search([('account_payment_id', '=', rec.id)])
            rec.appointment_count = len(rec.appointment_ids) if rec.appointment_ids else 0

=======
            rec.appointment_ids = rec.env['dr_patients.appointment'].search([('id', '=', rec.appointment_id.id)])
            rec.appointment_count = len(rec.appointment_ids) if rec.appointment_ids else 0

    
>>>>>>> mert1
    def action_view_appointment(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Appointment',
            'view_mode': 'tree,form',
            'res_model': 'dr_patients.appointment',
<<<<<<< HEAD
            'context': {'create': False, 'edit': False},
            'domain': [('id', '=', self.appointment_id.id)],
            'target': 'current',
        }

=======
            'domain': [('id', 'in', self.appointment_ids.ids)],
            'target': 'current',
        }



>>>>>>> mert1
    @api.model
    def create(self, vals):
        if 'ref' in vals and vals['ref']:
            account_move = self.env['account.move'].search([('name', '=', vals['ref'])])
            vals['appointment_id'] = account_move.appointment_id.id
        rec = super(Payment, self).create(vals)
        return rec
<<<<<<< HEAD
=======
    

    def action_view_payment(self):
        self.ensure_one()  # Ensure you're working with a single record.
        return {
            'type': 'ir.actions.act_window',
            'name': 'Payments',
            'res_model': 'account.payment',
            'view_mode': 'tree,form',
            'domain': [('appointment_id', '=', self.id)],  # Filter by appointment
            'context': {'default_appointment_id': self.id},  # Set the default appointment
            'stage': 'posted',
        }

    

>>>>>>> mert1
