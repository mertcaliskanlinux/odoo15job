from odoo import models, fields, api


class Invoice(models.Model):
    _inherit = 'account.move'

    appointment_id = fields.Many2one('dr_patients.appointment', string='Appointment', ondelete='set null')
    appointment_ids = fields.One2many('dr_patients.appointment', 'account_move_id')
    appointment_count = fields.Integer(string='Appointment', compute='_compute_appointment_count')

    @api.depends('appointment_id')
    def _compute_appointment_count(self):
        for rec in self:
            rec.appointment_count = len(rec.appointment_ids) if rec.appointment_id else 0

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
        if 'invoice_origin' in vals and vals['invoice_origin']:
            sale_order = self.env['sale.order'].search([('name', '=', vals['invoice_origin'])])
            vals['appointment_id'] = sale_order.appointment_id.id
        rec = super(Invoice, self).create(vals)
        return rec