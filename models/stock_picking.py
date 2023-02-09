# -*- coding: utf-8 -*- 

from odoo import models,fields,api,_
from odoo.exceptions import UserError


class StockPicking(models.Model):
    _inherit = "stock.picking"

    control_product_packaging = fields.Boolean(related='picking_type_id.control_product_packaging')
    control_in_details = fields.Boolean(compute='_compute_control_in_details')

    @api.depends('picking_type_id.show_operations')
    def _compute_control_in_details(self):
        for each in self:
            each.control_in_details = each.picking_type_id.show_operations