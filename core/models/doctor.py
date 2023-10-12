# -*- coding: utf-8 -*-
from odoo import models, fields

class Doctor(models.Model):

    _name='core.doctor'
    _description='Doctor'

    name = fields.Char(string='Name', required=True)
    date = fields.Date(string='Date', required=True)

