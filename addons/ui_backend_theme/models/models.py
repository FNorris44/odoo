from openerp.osv import fields, osv

class base_config_settings(osv.osv_memory):
    _name = 'ui.backend.theme'
    _inherit = 'res.config.settings'

    _columns = {
        'color': fields.char('Change Header color' ),
        'font_color': fields.char('Change Font color' ),
        'contrast_color': fields.char('Change Header contrast color' ),
        'heading_font_size': fields.selection([(x, x) for x in range(10, 26)]),
        'font_family': fields.selection([('Times New Roman', 'Times New Roman'),('Georgia, serif','Georgia, serif'),('Arial','Arial'),('Lucida Sans Unicode, Lucida Grande, sans-serif','Lucida Sans Unicode, Lucida Grande, sans-serif'),('Courier New','Courier New')])
        # 'left_menu_font_size': fields.selection([(x, x) for x in range(5, 18)]),
        }
    _defaults = {
        'heading_font_size': 16
    }

    def get_default_color(self, cr, uid, fields, context=None):
        color= self.search(cr, uid, [])
        if not color:
            return {'color': color}
        color = self.browse(cr, uid, color, context)[-1].color
        return {'color': color}

    def get_default_contrast_color(self, cr, uid, fields, context=None):
        contrast_color= self.search(cr, uid, [])
        if not contrast_color:
            return {'contrast_color': contrast_color}
        contrast_color = self.browse(cr, uid, contrast_color, context)[-1].contrast_color
        return {'contrast_color': contrast_color}

    def get_default_heading_font_size(self, cr, uid, fields, context=None):
        heading_font_size= self.search(cr, uid, [])
        if not heading_font_size:
            return {'heading_font_size': 16}
        heading_font_size = self.browse(cr, uid, heading_font_size, context)[-1].heading_font_size
        return {'heading_font_size': heading_font_size}

    def get_default_font_family(self, cr, uid, fields, context=None):
        font_family= self.search(cr, uid, [])
        if not font_family:
            return {'font_family': 'Times New Roman'}
        font_family = self.browse(cr, uid, font_family, context)[-1].font_family
        return {'font_family': font_family}