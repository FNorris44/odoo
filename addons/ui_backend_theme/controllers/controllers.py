# -*- coding: utf-8 -*-
from openerp import http
from openerp import SUPERUSER_ID
from openerp.addons.web.http import request

class UiBackendTheme(http.Controller):
    
    @http.route('/get/color', auth='public', type="json", website=True)
    def get_color(self):
        ui_id = request.registry['ui.backend.theme'].search(request.cr, SUPERUSER_ID, [])
        ui_obj = request.env['ui.backend.theme'].browse(ui_id)
        if ui_obj:
            color_code = ui_obj[-1].color
            contrast_color = ui_obj[-1].contrast_color
            heading_font_size = ui_obj[-1].heading_font_size
            font_family = ui_obj[-1].font_family
            font_color = ui_obj[-1].font_color
            return {'color' : str(color_code), 'heading_font_size': heading_font_size, 'contrast_color': contrast_color, 'font_family': font_family, 'font_color' : font_color}
        return '#fa6500'