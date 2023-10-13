from odoo import models, fields, api

class Invoice(models.Model):

    _name = 'account.move'
    _inherit = 'account.move'

    appointment_id = fields.Many2one('dr_patients.appointment', string='Appointment')
    appointment_count = fields.Integer(string='Appointments', compute='_compute_appointment_count')
    invoice_count = fields.Integer(string='Invoice', compute='_compute_invoice_count')
    invoice_ids = fields.One2many('account.move', 'appointment_id', string='Invoices')



    def action_view_sale_appointment(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Appointment',
            'view_mode': 'form',
            'res_model': 'dr_patients.appointment',
            'res_id': self.appointment_id.id,
            'context': {'create': False, 'edit': False},
            'target': 'current',
        }


    @api.depends('appointment_id')
    def _compute_appointment_count(self):
        for invoice in self:
            invoice.appointment_count = len(invoice.appointment_id) if invoice.appointment_id else 0


