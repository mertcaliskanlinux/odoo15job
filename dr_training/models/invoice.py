from odoo import models, fields, api

<<<<<<< HEAD

class Invoice(models.Model):
    _inherit = 'account.move'

    appointment_id = fields.Many2one('dr_patients.appointment', string='Appointment', ondelete='set null')
    appointment_ids = fields.One2many('dr_patients.appointment', 'account_move_id')
    appointment_count = fields.Integer(string='Appointment', compute='_compute_appointment_count')

    @api.depends('appointment_id')
    def _compute_appointment_count(self):
        for rec in self:
            rec.appointment_count = len(rec.appointment_ids) if rec.appointment_id else 0

=======
# Fatura modelini genişletiyor.
# Extends the Invoice model.
class Invoice(models.Model):
    
    _inherit = 'account.move'

    # Randevu alanı ekleniyor.
    # Adds the appointment field.
    appointment_id = fields.Many2one('dr_patients.appointment', string='Appointment')

    # Randevu kayıtlarını listelemek için bir alan ekleniyor.
    # Adds a field to list the appointment records.
    appointment_ids = fields.One2many('dr_patients.appointment', 'account_move_id' , compute='_compute_appointment_count')

    # Randevu sayısını hesaplamak için bir alan ekleniyor.
    # Adds a field to compute the appointment count.
    appointment_count = fields.Integer(string='Appointment', compute='_compute_appointment_count')

    # Randevu sayısını hesaplar.
    # Computes the appointment count.
    @api.depends('appointment_id')
    def _compute_appointment_count(self):
        for rec in self:
            # rec.appointment_count = rec.env['dr_patients.appointment'].search_count([('id', '=', rec.appointment_id.id)])
            rec.appointment_ids = rec.env['dr_patients.appointment'].search([('id', '=', rec.appointment_id.id)])
            rec.appointment_count = len(rec.appointment_ids) if rec.appointment_ids else 0

    # Randevuları görüntülemek için bir aksiyon döndürür.
    # Returns an action to view the appointments.
>>>>>>> mert1
    def action_view_appointment(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Appointment',
            'view_mode': 'tree,form',
            'res_model': 'dr_patients.appointment',
            'domain': [('id', 'in', self.appointment_ids.ids)],
            # 'context': {'create': False, 'edit': False},
            'target': 'current',
        }

<<<<<<< HEAD
    @api.model
    def create(self, vals):
        if 'invoice_origin' in vals and vals['invoice_origin']:
            sale_order = self.env['sale.order'].search([('name', '=', vals['invoice_origin'])])
            vals['appointment_id'] = sale_order.appointment_id.id
        rec = super(Invoice, self).create(vals)
        return rec
=======

    @api.model
    def create(self, vals):
        print("create account.move")
        print(vals)
        if 'invoice_origin' in vals and vals['invoice_origin']:
            sale_order = self.env['sale.order'].search([('name', '=', vals['invoice_origin'])])
            print(sale_order)
            vals['appointment_id'] = sale_order.appointment_id.id
        rec = super(Invoice, self).create(vals)
        return rec
>>>>>>> mert1
