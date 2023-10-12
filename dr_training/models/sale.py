from odoo import models, fields, api

class SaleOrder(models.Model):

    _inherit = 'sale.order'

    appointment_id = fields.Many2one('dr_patients.appointment', string='Appointment')
    appointment_count = fields.Integer(string='Appointment', compute='_compute_appointment_count')
    invoice_ids = fields.One2many('account.move', 'appointment_id', string='Invoice', compute='_compute_invoice_ids')
    invoice_count = fields.Integer(string='Invoice Count', compute='_compute_invoice_count')

    @api.depends('invoice_ids', 'appointment_id')
    def _compute_appointment_count(self):
        for order in self:
            order.appointment_count = len(order.appointment_id) if order.appointment_id else 0

    @api.depends('appointment_id')
    def _compute_invoice_ids(self):
        for appointment in self:
            appointment.invoice_ids = self.env['account.move'].search([('appointment_id', '=', appointment.id)])

    @api.depends('invoice_ids')
    def _compute_invoice_count(self):
        for appointment in self:
            appointment.invoice_count = len(appointment.invoice_ids)

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

    def action_view_appointment(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Appointment',
            'view_mode': 'form',
            'res_model': 'dr_patients.appointment',
            'res_id': self.appointment_id.id,
            'context': {'create': True, 'edit': False},
            'target': 'current',
        }

    @api.depends('invoice_ids')
    def _compute_invoice_count(self):
        for appointment in self:
            appointment.invoice_count = len(appointment.invoice_ids)


    def action_invoice(self):
        self.ensure_one()  # Tek bir kayıt için çalıştığından emin olun.

        return {
            'type': 'ir.actions.act_window',
            'name': 'Invoices',
            'res_model': 'account.move',
            'view_mode': 'tree,form',
            'domain': [('appointment_id', '=', self.id)],
            'context': {'default_appointment_id': self.id},
        }