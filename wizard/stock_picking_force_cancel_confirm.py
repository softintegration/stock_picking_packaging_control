# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class StockPickingForceCancelConfirm(models.TransientModel):
    _name = 'stock.picking.force.cancel.confirm'
    _description = 'Force cancel confirm'


    def confirm(self):
        pickings_to_cancel = self.env.context.get('pickings_to_cancel')
        return self.env['stock.picking'].browse(pickings_to_cancel)._action_force_cancel()
