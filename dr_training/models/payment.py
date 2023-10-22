
from odoo import models, fields,api,_



class Payment(models.Model):

    _inherit = 'account.payment'

    # İlgili randevuyu temsil eden alan
    # Field representing the related appointment
    # Çoktan bir ilişki kuruyoruz
    # We are establishing a relationship from many to one
    appointment_id = fields.Many2one('dr_patients.appointment', string='Appointment') 

    # Bu ödeme ile ilişkilendirilmiş tüm randevuları temsil eden alan
    # Field representing all appointments associated with this payment
    appointment_ids = fields.One2many('dr_patients.appointment', 'account_payment_id', string='Appointments') 

    # İlgili randevu sayısını gösteren alan
    # Field showing the number of related appointments
    appointment_count = fields.Integer(string='Appointment Count', compute='_compute_appointment_count') 

    # Randevu sayısını hesaplamak için kullanılan fonksiyon
    # Function used to compute the number of appointments
    @api.depends('appointment_id')
    def _compute_appointment_count(self):
        for rec in self:
            # İlgili randevuları bul
            # Find the related appointments
            rec.appointment_ids = rec.env['dr_patients.appointment'].search([('id', '=', rec.appointment_id.id)])
            # Randevuların sayısını hesapla ve atama
            # Calculate and assign the number of appointments
            rec.appointment_count = len(rec.appointment_ids) if rec.appointment_ids else 0



    
    # Randevuları görüntülemek için kullanılan eylem
    # Action used to view the appointments
    def action_view_appointment(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Appointment',
            'view_mode': 'tree,form',
            'res_model': 'dr_patients.appointment',
            'domain': [('id', 'in', self.appointment_ids.ids)],
            'target': 'current',
        }

    # Ödeme kaydı oluşturulurken yapılacak işlemler
    # Operations when creating a payment record
    @api.model
    def create(self, vals):
        if 'ref' in vals and vals['ref']:
            # Hesap hareketi üzerinden ilgili randevuyu bulup ödemeye ekliyoruz
            # We find the related appointment from the account move and add it to the payment
            account_move = self.env['account.move'].search([('name', '=', vals['ref'])])
            vals['appointment_id'] = account_move.appointment_id.id
        rec = super(Payment, self).create(vals)
        return rec
    

    # Ödemeleri görüntülemek için kullanılan eylem
    # Action used to view the payments
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

    

