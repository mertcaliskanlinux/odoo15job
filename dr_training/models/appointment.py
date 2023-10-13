# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
from .sale import  SaleOrder



class Appointment(models.Model):

    _name = "dr_patients.appointment"
    _description = "Appointment"

    appointment_date_time = fields.Datetime(string="Appointment Date & Time", required=True)
    code = fields.Char(string='Code', required=True, index=True, copy=False, default=lambda self: self.env['ir.sequence'].next_by_code('dr_patients.appointment') or 'New')
    doctor_id = fields.Many2many(comodel_name="dr_patients.doctor", string="Doctor")
    patient = fields.Many2one(comodel_name="dr_patients.patient", string="Patient", required=True)
    stage = fields.Selection(string="Stage", selection=[('draft', 'Draft'), ('in_progress', 'In Progress'), ('done', 'Done'),('cancel', 'Cancel')], default='draft', required=True)
    treatment = fields.One2many('dr_patients.treatment', 'appointment', string='Treatments')
    patient_full_name = fields.Char(string="Patient Name", compute="_compute_patient_full_name", store=True)
    doctor_full_name = fields.Char(string="Doctor Name", compute="_compute_doctor_full_name", store=True)
    is_readonly = fields.Boolean(string="Is Readonly", compute="_compute_is_readonly")
    total_amount = fields.Float(string="Total Amount", compute="_compute_total_amount", store=True)
    sale_order_count = fields.Integer(string="Sale Orders", compute="_compute_sale_order_count")
    sale_order_id = fields.Many2one(comodel_name="sale.order", string="Sale Order")
    appointment_id = fields.Many2one('dr_patients.appointment', string='Appointment')
    invoice_ids = fields.One2many('account.move', 'appointment_id', string='Invoice', compute='_compute_invoice_ids')
    invoice_count = fields.Integer(string='Invoice Count', compute='_compute_invoice_count')


    @api.depends('invoice_ids')
    def _compute_invoice_ids(self):
        for appointment in self:
            appointment.invoice_ids = self.env['account.move'].search([('appointment_id', '=', appointment.id)])

    @api.depends('invoice_count')
    def _compute_invoice_count(self):
        for appointment in self:
            appointment.invoice_count = len(appointment.invoice_ids)

    def action_view_invoices(self):

        invoices = self.invoice_ids
        print(f"invoices: {invoices}")



        return {
            'name': 'Invoices',
            'view_mode': 'tree,form',
            'res_model': 'account.move',
            'domain': [('id', 'in', invoices.ids)],
            'type': 'ir.actions.act_window',
        }

    @api.depends('patient')
    def _compute_patient_full_name(self):
        for appointment in self:
            appointment.patient_full_name = appointment.patient.full_name if appointment.patient else ""

    @api.depends('doctor_id')
    def _compute_doctor_full_name(self):
        for appointment in self:
            appointment.doctor_full_name = ', '.join(
                appointment.doctor_id.mapped('full_name')) if appointment.doctor_id else ""

    @api.depends('appointment_id')
    def _compute_sale_order_count(self):
        for appointment in self:
            sale_order_count = self.env['sale.order'].search_count([('appointment_id', '=', appointment.id)])
            appointment.sale_order_count = sale_order_count

    def action_in_progress(self):
        self.write({'stage': 'in_progress'})

    def action_done(self):
        self.write({'stage': 'done'})

    def action_draft(self):
        self.write({'stage': 'draft'})

    def action_cancel(self):
        self.write({'stage': 'cancel'})

    def unlink(self):
        if self.filtered(lambda appointment: appointment.stage == 'done'):
            raise exceptions.ValidationError("You cannot delete a done appointment")
        return super(Appointment, self).unlink()


    @api.model
    def create(self, vals):
        if vals.get('code', 'New') == 'New':
            vals['code'] = self.env['ir.sequence'].next_by_code('dr_patients.appointment') or 'New'
        return super(Appointment, self).create(vals)

    @api.constrains('code')
    def _check_code_unique(self):
        for record in self:
            if self.env['dr_patients.appointment'].search_count([('code', '=', record.code)]) > 1:
                raise exceptions.ValidationError('The Code must be unique.')

    def action_sale_order(self):
        self.ensure_one()  # Ensure that it works for a single record.

        # Create a new Sale Order record in the 'draft' state
        created_sale_order = self.env['sale.order'].create({
            'partner_id': self.patient.id,
            'appointment_id': self.id,  # Link the Sale Order to the current appointment
        })

        # Open the created Sale Order for further editing
        action = {
            'type': 'ir.actions.act_window',
            'name': 'Sale Orders',
            'res_model': 'sale.order',
            'view_mode': 'form',
            'res_id': created_sale_order.id,
            'context': {
                'default_appointment_id': self.id,  # Set the appointment for reference
            },
        }

        return action