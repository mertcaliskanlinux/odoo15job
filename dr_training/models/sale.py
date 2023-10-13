# -*- coding: utf-8 -*-
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
            'context': {'create': False},
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
            'context': {'create': True},
            'target': 'current',
        }

    def action_invoice(self):
        self.ensure_one()

        # Create a new invoice
        invoice = self.env['account.move'].create({
            'appointment_id': self.appointment_id.id,  # Set the appointment on the invoice
            # Other fields for the invoice, such as partner_id, product lines, etc.
        })

        # Optionally, you can manually post (confirm) the invoice
        invoice.post()

        return {
            'type': 'ir.actions.act_window',
            'name': 'Invoice',
            'res_model': 'account.move',
            'view_mode': 'form',
            'res_id': invoice.id,
            'context': {'create': False},
            'target': 'current',
        }

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    appointment = fields.Many2one('dr_patients.appointment', string='Appointment')
