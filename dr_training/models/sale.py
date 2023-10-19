from odoo import models, fields, api

# Satış Siparişi modelini genişletiyor.
# Extends the Sale Order model.
class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    appointment_id = fields.Many2one('dr_patients.appointment', string='Appointment') # Randevu /* Appointment */
    appointment_count = fields.Integer(string='Appointment', compute='_compute_appointment_count', store=True) # Randevu sayısı /* Appointment count */


    # Randevu sayısını hesaplar.
    # Computes the appointment count.
    @api.depends('appointment_id')
    def _compute_appointment_count(self):
        for rec in self:
            rec.appointment_count = len(rec.appointment_id) if rec.appointment_id else 0


    # Randevuları görüntülemek için bir aksiyon döndürür.
    # Returns an action to view the appointments.
    def action_open_appointments(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window', # Aksiyon tipi /* Action type */
            'name': 'Appointment', # Aksiyon adı /* Action name */
            'view_mode': 'form', # Görünüm modu /* View mode */ 
            'res_model': 'dr_patients.appointment', # Kaynak modeli /* Resource model */
            'res_id': self.appointment_id.id,   # Kaynak kimliği /* Resource id */
            'context': {'create': True, 'edit': False}, # Bağlam /* Context */
            'target': 'current', 
        }

    # Yeni bir fatura oluşturur.
    # Creates a new invoice.
    def action_open_invoice(self):
        self.ensure_one()

        invoice_id = self.env['account.move'].create({
            'appointment_id': self.appointment_id.id, 
            'ref': self.name, 
        }) # Fatura oluşturur. /* Creates an invoice. */

        return {
            'type': 'ir.actions.act_window',
            'name': 'Invoice',
            'res_model': 'account.move',
            'res_id': invoice_id.id,
            'context': {'create': False, 'edit': False},
            'view_mode': 'form',
            'target': 'current',
        } # Fatura formunu açar. /* Opens the invoice form. */

    # Faturaları görüntülemek için bir aksiyon döndürür.
    # Returns an action to view the invoices.
    def action_view_invoice(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Invoices',
            'res_model': 'account.move',
            'view_mode': 'tree,form',
            'domain': [('appointment_id', '=', self.appointment_id.id)], 
            'context': {'default_appointment_id': self.appointment_id.id},  
            'stage': 'posted',
        }
    
# Satış Siparişi Satırı modelini genişletiyor.
# Extends the Sale Order Line model.
class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    appointment_id = fields.Many2one('dr_patients.appointment', string='Appointment')
