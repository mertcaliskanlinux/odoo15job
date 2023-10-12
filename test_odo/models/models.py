# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Person(models.Model):
    _name = 'test_odo.person'
    _description = 'test_odo.person'

    name = fields.Char()
    value = fields.Integer()
    value2 = fields.Float(compute="_value_pc", store=True)
    description = fields.Text()

    @api.depends('value')
    def _value_pc(self):
        for record in self:
            record.value2 = float(record.value) / 100
