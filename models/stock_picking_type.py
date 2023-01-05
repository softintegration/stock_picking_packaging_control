# -*- coding: utf-8 -*- 

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class PickingType(models.Model):
    _inherit = "stock.picking.type"

    control_product_packaging = fields.Boolean(string='Control the packaging', default=False,
        help="If this case is checked,the system will control the packaging in this type of transfers")
