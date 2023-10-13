from odoo import models, fields, api

class Invoice(models.Model):

    _name = 'account.move'
    _inherit = 'account.move'
    # bu burada çünkü appointment_id şu işe yarıyor ki appointment_id ile invoice_id birbirine bağlı olsun
    appointment_id = fields.Many2one('dr_patients.appointment', string='Appointment') #one2many
    #appointment id's ise şu işe yarıyor ki appointment_id ile invoice_id birbirine bağlı olsun
    appointment_ids = fields.One2many('dr_patients.appointment', 'invoice_id', string='Appointment', compute='_compute_appointment_ids')
    appointment_count = fields.Integer(string='Appointments', compute='_compute_appointment_count')
    invoice_count = fields.Integer(string='Invoice', compute='_compute_invoice_count')



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


