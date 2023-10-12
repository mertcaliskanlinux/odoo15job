from odoo import models, fields, api, exceptions

class Appointment(models.Model):
    _name = "hospital.appointment"
    _description = "Appointment"


    appointment_date_time = fields.Datetime(string="Appointment Date & Time", required=True)
    code = fields.Char(string='Code', required=True, index=True, copy=False,
                       default=lambda self: self.env['ir.sequence'].next_by_code('hospital.appointment') or 'New')
    doctor_id = fields.Many2many(comodel_name="hospital.doctor", string="Doctor")
    patient_id = fields.Many2one(comodel_name="hospital.patient", string="Patient", required=True)
    stage = fields.Selection(string="Stage", selection=[('draft', 'Draft'), ('in_progress', 'In Progress'), ('done', 'Done'),('cancel', 'Cancel')], default='draft', required=True)

    treatment = fields.One2many('hospital.treatment', 'appointment', string='Treatments')
    patient_full_name = fields.Char(string="Patient Name", compute="_compute_patient_full_name", store=True)
    doctor_full_name = fields.Char(string="Doctor Name", compute="_compute_doctor_full_name", store=True)
    is_readonly = fields.Boolean(string="Is Readonly", compute="_compute_is_readonly")
    appointment_id = fields.Many2one(comodel_name="sale.order", string="Sale Order")

    total_amount = fields.Float(string="Total Amount", compute="_compute_total_amount", store=True)
    pending_amount = fields.Float(string="Pending Amount", compute="_compute_pending_amount", store=True)
    sale_order_line_ids = fields.One2many('sale.order.line', 'order_id', string="Sale Order Line")
    sale_order_count = fields.Integer(string="Sale Orders", compute="_compute_sale_order_count")
    invoice_count = fields.Integer(string="Invoices", compute="_compute_invoice_count")


    @api.depends('patient_id')
    def _compute_patient_full_name(self):
        for appointment in self:
            appointment.patient_full_name = appointment.patient.full_name if appointment.patient else ""

    @api.depends('doctor_id')
    def _compute_doctor_full_name(self):
        for appointment in self:
            appointment.doctor_full_name = ', '.join(
                appointment.doctor_id.mapped('full_name')) if appointment.doctor_id else ""

    def action_in_progress(self):
        self.write({'stage': 'in_progress'})

    @api.model
    def create(self, vals):
        if vals.get('code', 'New') == 'New':
            vals['code'] = self.env['ir.sequence'].next_by_code('hospital.appointment') or 'New'
        return super(Appointment, self).create(vals)

    @api.constrains('code')
    def _check_code_unique(self):
        for record in self:
            if self.env['dr_patients.appointment'].search_count([('code', '=', record.code)]) > 1:
                raise exceptions.ValidationError('The Code must be unique.')

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
