# -*- coding: utf-8 -*-
# from odoo import http


# class RealEstate1(http.Controller):
#     @http.route('/real_estate_1/real_estate_1', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/real_estate_1/real_estate_1/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('real_estate_1.listing', {
#             'root': '/real_estate_1/real_estate_1',
#             'objects': http.request.env['real_estate_1.real_estate_1'].search([]),
#         })

#     @http.route('/real_estate_1/real_estate_1/objects/<model("real_estate_1.real_estate_1"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('real_estate_1.object', {
#             'object': obj
#         })
