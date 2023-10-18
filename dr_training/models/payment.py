from odoo import api, fields, models, _


class Payment(models.Model):
    _inherit = "account.payment"

    appointment_id = fields.Many2one('dr_patients.appointment', string='Appointment')  
    appointment_ids = fields.One2many('dr_patients.appointment', 'account_payment_id')  #
    appointment_count = fields.Integer(string='Appointment', compute='_compute_appointment_count')


    @api.depends('appointment_id')
    def _compute_appointment_count(self):
        for rec in self:
            rec.appointment_count = len(rec.appointment_id) if rec.appointment_id else 0

    def action_view_appointment(self):
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

    @api.model
    def create(self, vals):
        if 'ref' in vals and vals['ref']:
            account_move = self.env['account.move'].search([('name', '=', vals['ref'])])
            vals['appointment_id'] = account_move.appointment_id.id
        rec = super(Payment, self).create(vals)
        return rec
