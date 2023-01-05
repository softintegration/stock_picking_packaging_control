# -*- coding: utf-8 -*- 

from odoo import models,fields,api,_
from odoo.exceptions import UserError


class StockPicking(models.Model):
    _inherit = "stock.picking"

    control_product_packaging = fields.Boolean(related='picking_type_id.control_product_packaging')