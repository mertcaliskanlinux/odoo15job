from odoo import api, fields, models


class Payment(models.Model):
    _inherit = "account.payment"

    appointment_id = fields.Many2one('dr_patients.appointment', string='Appointment')  # One2many another
    appointment_ids = fields.One2many('dr_patients.appointment', 'account_payment_id', compute='_compute_appointment_count')
    appointment_count = fields.Integer(string='Appointment', compute='_compute_appointment_count')

    @api.depends('appointment_id')
    def _compute_appointment_count(self):
        for rec in self:
            rec.appointment_ids = self.env['dr_patients.appointment'].search([('account_payment_id', '=', rec.id)])
            rec.appointment_count = len(rec.appointment_ids) if rec.appointment_ids else 0

    def action_view_appointment(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Appointment',
            'view_mode': 'tree,form',
            'res_model': 'dr_patients.appointment',
            'context': {'create': False, 'edit': False},
            'domain': [('id', '=', self.appointment_id.id)],
            'target': 'current',
        }

    @api.model
    def create(self, vals):
        if 'ref' in vals and vals['ref']:
            account_move = self.env['account.move'].search([('name', '=', vals['ref'])])
            vals['appointment_id'] = account_move.appointment_id.id
        rec = super(Payment, self).create(vals)
        return rec
