# -*- coding: utf-8 -*-

# Gerekli kütüphaneleri ve modülleri Odoo çerçevesinden içe aktar
# Import necessary libraries and modules from the Odoo framework
from odoo import models, fields, api, exceptions

# 'dr_patients.appointment' adında Odoo'da yeni bir model tanımla. Bu model, bir hasta randevu sistemini temsil eder.
# Define a new model in Odoo named 'dr_patients.appointment' which represents an appointment in a patient system.
class Appointment(models.Model):

    # Model adı.
    # Model name.
    _name = "dr_patients.appointment"

    # Model açıklaması.
    # Model description.
    _description = "Appointment"

    # Randevu tarihi ve saati.
    # Appointment date and time.
    appointment_date_time = fields.Datetime(string="Appointment Date & Time", required=True)

    # Randevu kodu.
    # Appointment code.
    code = fields.Char(string="Code",index=True)
    # Doktor referansı (Many2Many ilişki).
    # Doctor reference (Many2Many relationship).
    doctor_id = fields.Many2many(comodel_name="dr_patients.doctor", string="Doctor")

    # Hasta referansı.
    # Patient reference.
    patient = fields.Many2one(comodel_name="dr_patients.patient", string="Patient", required=True)

    # Randevu aşaması (draft, in_progress, done, cancel).
    # Appointment stage (draft, in_progress, done, cancel).
    stage = fields.Selection(string="Stage", selection=[('draft', 'Draft'), ('in_progress', 'In Progress'), ('done', 'Done'),('cancel', 'Cancel')], default='draft', required=True)

    # Tedaviler (One2Many ilişki).
    # Treatments (One2Many relationship).
    treatment = fields.One2many('dr_patients.treatment', 'appointment', string='Treatments')

    # Hasta tam adı (hesaplanan alan).
    # Patient full name (computed field).
    patient_full_name = fields.Char(string="Patient Name", compute="_compute_patient_full_name", store=True)

    # Doktor tam adı (hesaplanan alan).
    # Doctor full name (computed field).
    doctor_full_name = fields.Char(string="Doctor Name", compute="_compute_doctor_full_name", store=True)

    # Salt okunur mu? (hesaplanan alan).
    # Is it read-only? (computed field).
    is_readonly = fields.Boolean(string="Is Readonly", compute="_compute_is_readonly")

    # Toplam miktar (hesaplanan alan).
    # Total amount (computed field).
    total_amount = fields.Float(string="Total Amount", compute="_compute_total_amount", store=True)

    # Satış siparişi satırları (One2Many ilişki).
    # Sale order lines (One2Many relationship).
    sale_order_line_ids = fields.One2many('sale.order.line', 'appointment_id', string="Sale Order Line")

    # Satış sipariş sayısı (hesaplanan alan).
    # Sales order count (computed field).
    sale_order_count = fields.Integer(string='Sale Orders', compute='_compute_sale_order_count')

    # Satış siparişleri (One2Many ilişki).
    # Sales orders (One2Many relationship).
    sale_order_ids = fields.One2many('sale.order', 'appointment_id', string="Sales Order")

    # Satış siparişi referansı.
    # Sales order reference.
    sale_order_id = fields.Many2one('sale.order')

    # Fatura referansı.
    # Invoice reference.
    account_move_id = fields.Many2one('account.move', string="Invoice")

    # Faturalar (One2Many ilişki).
    # Invoices (One2Many relationship).
    invoice_ids = fields.One2many('account.move', 'appointment_id', string="Invoices")

    # Fatura sayısı (hesaplanan alan).
    # Invoice count (computed field).
    invoice_count = fields.Integer(string='Invoices', compute='_compute_invoice_count')

    # Hasta ortağı referansı.
    # Patient partner reference.
    partner_id = fields.Many2one('res.partner', "Patient Partner")
    payment_ids = fields.One2many('account.payment', 'appointment_id', string="Payments")
    payment_count = fields.Integer(string='Payments', compute='_compute_payment_count')
    account_payment_id = fields.Many2one('account.payment')


    _sql_constraints = [
            ('unique_code', 'unique(code)', 'Code must be unique.'),
        ]
    

    
    @api.depends('patient')
    def _compute_patient_full_name(self):
        for appointment in self:
            appointment.patient_full_name = appointment.patient.full_name if appointment.patient else ""

    @api.depends('doctor_id')
    def _compute_doctor_full_name(self):
        for appointment in self:
            appointment.doctor_full_name = ', '.join(
                appointment.doctor_id.mapped('full_name')) if appointment.doctor_id else ""



        # 'invoice_ids' alanına bağlı olarak faturaların hesaplanmasını sağlar.
    # Computes the invoices based on the 'invoice_ids' field.
    @api.depends('invoice_ids')
    def _compute_invoice_ids(self):
        for appointment in self:
            appointment.invoice_ids = self.env['account.move'].search([('appointment_id', '=', appointment.id)])

    # Randevuya bağlı fatura sayısını hesaplar.
    # Computes the count of invoices linked to the appointment.
    def _compute_invoice_count(self):
        for rec in self:
            invoice_count = self.env['account.move'].search_count([
                ('appointment_id', '=', rec.id), ('state', '=', 'posted'),
                ('payment_state', 'in', ('in_payment', 'paid'))
                
                # Add your search criteria here.
            ])
            rec.invoice_count = invoice_count


    

    # Belirli bir randevu için faturaları görüntülemek üzere bir aksiyon döndürür.
    # Returns an action to view the invoices for a specific appointment.
    def action_view_invoice(self):
        self.ensure_one()  # Tek bir kayıt
                          # a single record.
        return {
            'type': 'ir.actions.act_window',
            'name': 'Invoices',
            'res_model': 'account.move',
            'view_mode': 'tree,form',
            'domain': [('appointment_id', '=', self.id), ('state', '=', 'posted'),
                       ('payment_state', 'in', ('in_payment', 'paid'))],  # Randevuya göre filtrele.
            
                                                           # Filter by appointment.
            'context': {'default_appointment_id': self.id},  # Varsayılan randevuyu ayarla.
                                                             # Set the default appointment.
            'stage': 'posted',
        }

    # Hastanın tam adını hesaplar.
    # Computes the full name of the patient.
    @api.depends('patient')
    def _compute_patient_full_name(self):
        for appointment in self:
            appointment.patient_full_name = appointment.patient.full_name if appointment.patient else ""

    # Doktorun tam adını hesaplar.
    # Computes the full name of the doctor.
    @api.depends('doctor_id')
    def _compute_doctor_full_name(self):
        for appointment in self:
            appointment.doctor_full_name = ', '.join(
                appointment.doctor_id.mapped('full_name')) if appointment.doctor_id else ""

    # Randevuya bağlı satış siparişi sayısını hesaplar.
    # Computes the count of sale orders linked to the appointment.
    @api.depends('sale_order_line_ids')
    def _compute_sale_order_count(self):
        for rec in self:
            sale_order_count = self.env['sale.order'].search_count([('appointment_id', '=', self.id)])
            rec.sale_order_count = sale_order_count

    # Randevunun durumunu 'devam ediyor' olarak ayarlar.
    # Sets the status of the appointment to 'in progress'.
    def action_in_progress(self):
        self.write({'stage': 'in_progress'})

    # Randevunun durumunu 'tamamlandı' olarak ayarlar.
    # Sets the status of the appointment to 'done'.
    def action_done(self):
        self.write({'stage': 'done'})

    # Randevunun durumunu 'taslak' olarak ayarlar.
    # Sets the status of the appointment to 'draft'.
    def action_draft(self):
        self.write({'stage': 'draft'})

    # Randevunun durumunu 'iptal edildi' olarak ayarlar.
    # Sets the status of the appointment to 'cancel'.
    def action_cancel(self):
        self.write({'stage': 'cancel'})

    # Tamamlanmış bir randevuyu silme işlemi yaparken bir hata oluşturur.
    # Raises an error when trying to delete a completed appointment.
    def unlink(self):
        if self.filtered(lambda appointment: appointment.stage == 'done'):
            raise exceptions.ValidationError("You cannot delete a done appointment")
        return super(Appointment, self).unlink()

    # Yeni bir randevu oluşturulduğunda kodun otomatik olarak atanmasını sağlar.
    # Ensures the code is automatically assigned when a new appointment is created.
    @api.model
    def create(self, vals):
        print("Appointment create vals ", vals)
        vals['code'] = self.env['ir.sequence'].next_by_code("dr_patients.appointment")
        return super(Appointment, self).create(vals)

    # Randevu kodunun benzersiz olup olmadığını kontrol eder.
    # Checks if the appointment code is unique.
    @api.constrains('code')
    def _check_code_unique(self):
        for record in self:
            if self.env['dr_patients.appointment'].search_count([('code', '=', record.code)]) > 1:
                raise exceptions.ValidationError('The Code must be unique.')
            

    # Belirli bir randevu için satış siparişini görüntülemek üzere bir aksiyon döndürür.
    # Returns an action to view the sale order for a specific appointment.
    def action_sale_order(self):
        self.ensure_one()  
        action = {
            'type': 'ir.actions.act_window',
            'name': 'Sale Orders',
            'res_model': 'sale.order',
            'view_mode': 'tree,form',
            'domain': [('appointment_id', '=', self.id)],  # Randevuya göre filtrele. / Filter by appointment.
            'context': {
                'default_appointment_id': self.id,  # Randevuyu referans olarak ayarla.
                                                     # Set the appointment for reference.
            },
        }
        return action
    #burası satış siparişi oluştururken kullanılıyor
    # This is used when creating a sale order.
    @api.depends('payment_ids')
    def _compute_payment_ids(self):
        for rec in self:
            rec.payment_ids = self.env['account.payment'].search([('appointment_id', '=', rec.id)])

    # Belirli bir randevu için ödemeleri görüntülemek üzere bir aksiyon döndürür.
    # Returns an action to view the payments for a specific appointment.
    def _compute_payment_count(self):
        for rec in self:
            payment_count = self.env['account.payment'].search_count([
                ('appointment_id', '=', rec.id)
            ])
            rec.payment_count = payment_count

    #burası ödeme oluştururken kullanılıyor
    # This is used when creating a payment.
    def action_view_payment(self):
        self.ensure_one()  
        return {
            'type': 'ir.actions.act_window',
            'name': 'Payments',
            'res_model': 'account.payment',
            'view_mode': 'tree,form',
            'domain': [('appointment_id', '=', self.id)], 
            'context': {'default_appointment_id': self.id},  
            'stage': 'posted',
        }


    # Yeni bir satış siparişi oluşturur.
    # Creates a new sale order.
    def create_sale_order(self):
        self.ensure_one()
        if not self.patient:
            # Eğer hastası yoksa bir hata mesajı döndürülüyor.
            # Returns an error message if there's no patient.
            raise exceptions.ValidationError("No patient found for this appointment.")
        
        self.partner_id = self.env['res.partner'].create({
            'name': self.patient.first_name + " " + self.patient.last_name,
            'phone': self.patient.phone,
            'email': self.patient.email,
        })

        sale_order = self.env['sale.order'].create({
            'appointment_id': self.id,
            'partner_id': self.partner_id.id,
        })

        product = self.env['product.product'].search([('name', '=', 'Injections')], limit=1)
        if not product:
            # Eğer ürün bulunamazsa bir hata mesajı döndürülüyor.
            # Returns an error message if the product is not found.
            raise exceptions.ValidationError("Product 'Injections' not found.")
        
        sale_order_line = self.env['sale.order.line'].create({
            'order_id': sale_order.id,
            'product_id': product.id,
        })

        return {
            'type': 'ir.actions.act_window',
            'name': 'Sale Order',
            'res_model': 'sale.order',
            'res_id': sale_order.id,
            'view_mode': 'form',
            'target': 'current',
        }

    
        
