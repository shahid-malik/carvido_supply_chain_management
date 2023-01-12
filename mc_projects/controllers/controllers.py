# -*- coding: utf-8 -*-
# from odoo import http


# class McProjects(http.Controller):
#     @http.route('/mc_projects/mc_projects', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mc_projects/mc_projects/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('mc_projects.listing', {
#             'root': '/mc_projects/mc_projects',
#             'objects': http.request.env['mc_projects.mc_projects'].search([]),
#         })

#     @http.route('/mc_projects/mc_projects/objects/<model("mc_projects.mc_projects"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mc_projects.object', {
#             'object': obj
#         })
