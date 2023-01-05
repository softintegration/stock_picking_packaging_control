# -*- coding: utf-8 -*- 

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare


class StockMove(models.Model):
    _inherit = "stock.move"

    use_packaging = fields.Boolean(string='Use packaging', compute='_compute_use_packaging')
    qty_by_packaging = fields.Float(string="Qty by packaging", related='product_packaging_id.qty', store=True)
    packaging_nbr = fields.Integer(string="Nbr of packaging", states={'done': [('readonly', True)]},copy=False)
    incomplete_qty = fields.Float(string='Incomplete Qty', store=True, compute='_get_incomplete_qty')

    @api.depends('product_id')
    def _compute_use_packaging(self):
        for each in self:
            each.use_packaging = each.picking_type_id.control_product_packaging and len(each.product_id.packaging_ids) > 0

    @api.depends('quantity_done', 'qty_by_packaging')
    def _get_incomplete_qty(self):
        for each in self:
            try:
                each.incomplete_qty = each.quantity_done % each.qty_by_packaging
            except ZeroDivisionError as ex:
                each.incomplete_qty = 0.0

    def _action_done(self, cancel_backorder=False):
        moves_todo = super(StockMove, self)._action_done(cancel_backorder=cancel_backorder)
        for move in moves_todo.filtered(lambda mv: mv.use_packaging):
            move._check_packaging_consistency()
        return moves_todo

    def _check_packaging_consistency(self):
        self.ensure_one()
        if self.use_packaging and not self.product_packaging_id:
            raise ValidationError(_("Packaging is required for product %s") % self.product_id.display_name)
        # we have to convert the qty_by_packaging to the move uom
        qty_by_packaging = self.product_packaging_id.product_uom_id._compute_quantity(self.qty_by_packaging, self.product_uom)
        # this is the number of packaging that we have to find
        try:
            ref_packaging_nbr = int(self.quantity_done / qty_by_packaging)
        except ZeroDivisionError as e:
            raise ValidationError(_("Contained Quantity must be positive in %s!") % self.product_packaging_id.name)
        # we have to get the remainder
        remaining_qty = self.quantity_done % qty_by_packaging
        # if there is remaining qty so we have to add package
        if float_compare(remaining_qty, 0.0, precision_rounding=self.product_uom.rounding) > 0:
            ref_packaging_nbr += 1
        # Now the final step is to compare the reference number of packaging (the number of packaging that we have to find)
        # with number of packaging entered by the user
        if ref_packaging_nbr != self.packaging_nbr:
            raise ValidationError(
                _("Nbr of packaging in move %s doesn't match the Quantity Done and Contained Quantity in %s ") %(self.name,self.product_packaging_id.name))
