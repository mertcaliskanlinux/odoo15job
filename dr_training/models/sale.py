from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    appointment_id = fields.Many2one('dr_patients.appointment', string='Appointment')
    appointment_count = fields.Integer(string='Appointment', compute='_compute_appointment_count', store=True)
    invoice_count = fields.Integer(string='Invoice', compute='_compute_invoice_count')
    invoice_ids = fields.One2many('account.move', 'appointment_id', string='Invoice', compute="_compute_invoice_ids",
                                  store="True")


    @api.depends('appointment_id')
    def _compute_appointment_count(self):
        for rec in self:
            rec.appointment_count = len(rec.appointment_id) if rec.appointment_id else 0

    @api.depends('invoice_ids')
    def _compute_invoice_ids(self):
        for rec in self:
            rec.invoice_ids = self.env['account.move'].search([('appointment_id', '=', rec.id)])

    @api.depends('invoice_ids', 'appointment_id')
    def _compute_invoice_count(self):
        for rec in self:
            rec.invoice_count = len(rec.invoice_ids)

    def action_open_appointments(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Appointment',
            'view_mode': 'form',
            'res_model': 'dr_patients.appointment',
            'res_id': self.appointment_id.id,
            'context': {'create': True, 'edit': False},
            'target': 'current',
        }

    def action_open_invoice(self):
        self.ensure_one()

        invoice_id = self.env['account.move'].create({
            'appointment_id': self.appointment_id.id,
            'ref': self.name,
        })



        return {
            'type': 'ir.actions.act_window',
            'name': 'Invoice',
            'res_model': 'account.move',
            'res_id': invoice_id.id,
            'context': {'create': False, 'edit': False},
            'view_mode': 'form',
            'target': 'current',
        }

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


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    appointment_id = fields.Many2one('dr_patients.appointment', string='Appointment')
