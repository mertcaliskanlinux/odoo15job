from odoo import models, fields, api, exceptions

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
    appointment_id = fields.Many2one(comodel_name="sale.order", string="Sale Order")

    total_amount = fields.Float(string="Total Amount", compute="_compute_total_amount", store=True)
    pending_amount = fields.Float(string="Pending Amount", compute="_compute_pending_amount", store=True)
    sale_order_line_ids = fields.One2many('sale.order.line', 'order_id', string="Sale Order Line")
    sale_order_count = fields.Integer(string="Sale Orders", compute="_compute_sale_order_count")
    invoice_count = fields.Integer(string="Invoices", compute="_compute_invoice_count")
    payment_count = fields.Integer(string="Payments",compute="_compute_payment_count")
    invoice_ids = fields.One2many('account.move', 'appointment_id', string="Invoices")

    @api.depends('patient')
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

    @api.depends('sale_order_line_ids.order_id')
    def _compute_sale_order_count(self):
        for appointment in self:
            appointment.sale_order_count = len(appointment.sale_order_line_ids.mapped('order_id'))



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
        self.ensure_one() # Tek bir kayıt için çalıştığından emin olun.
        action = {
            'type': 'ir.actions.act_window',
            'name': 'Sale Orders',
            'res_model': 'sale.order',
            'view_mode': 'tree,form',
            'domain': [('appointment_id', '=', self.id)],
            'context': {'default_appointment_id': self.id},
        }
        return action

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

    def action_payment(self):
        for appointment in self:
            # Hasta (patient) veya müşteri (customer) kaydı oluşturun (örnek olarak)

            patient_name = appointment.patient.full_name if appointment.patient else ''
            customer_values = {
                'name': f"{patient_name}",
                # Diğer gerekli müşteri bilgilerini burada ekleyin
            }
            customer = self.env['res.partner'].create(customer_values)

            # Ödeme (payment) kaydı oluşturun
            payment_values = {
                'partner_id': customer.id,  # Oluşturulan müşteri kaydının ID'sini kullanın
                'payment_date': fields.Date.today(),
                # Diğer gerekli ödeme (payment) bilgilerini burada ekleyin
            }
            payment = self.env['account.payment'].create(payment_values)

            # Ödeme (payment) kaydı formunu açın
            self.env.context = dict(self.env.context, default_payment_id=payment.id)
            return {
                'name': 'Payment',
                'type': 'ir.actions.act_window',
                'res_model': 'account.payment',
                'res_id': payment.id,
                'view_mode': 'form',
                'target': 'current',
            }

    @api.depends('sale_order_line_ids')
    def _compute_total_amount(self):
        for rec in self:
            total_amount = sum(rec.sale_order_line_ids.mapped('price_total'))
            rec.total_amount = total_amount

    @api.depends('sale_order_line_ids', 'sale_order_line_ids.invoice_status')
    def _compute_pending_amount(self):
        for rec in self:
            pending_amount = sum(
                rec.sale_order_line_ids.filtered(lambda line: line.invoice_status != 'invoiced').mapped(
                    'price_total'))
            rec.pending_amount = pending_amount

    @api.depends('sale_order_line_ids.order_id')
    def _compute_sale_order_count(self):
        for rec in self:
            rec.sale_order_count = len(rec.sale_order_line_ids.mapped('order_id'))


    # @api.depends('sale_order_line_ids.order_id')
    # def _compute_payment_count(self):
    #     for appointment in self:
    #         payment_count = len(appointment.sale_order_line_ids.mapped('order_id').mapped('payment_ids'))
    #         appointment.payment_count = payment_count



    @api.depends('invoice_ids')
    def _compute_invoice_count(self):
        for appointment in self:
            appointment.invoice_count = len(appointment.invoice_ids)





