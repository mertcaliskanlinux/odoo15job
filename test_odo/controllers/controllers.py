# -*- coding: utf-8 -*-
# from odoo import http


# class TestOdo(http.Controller):
#     @http.route('/test_odo/test_odo', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/test_odo/test_odo/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('test_odo.listing', {
#             'root': '/test_odo/test_odo',
#             'objects': http.request.env['test_odo.test_odo'].search([]),
#         })

#     @http.route('/test_odo/test_odo/objects/<model("test_odo.test_odo"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('test_odo.object', {
#             'object': obj
#         })
