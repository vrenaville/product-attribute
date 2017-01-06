# -*- coding: utf-8 -*-
# © 2015 ADHOC SA  (http://www.adhoc.com.ar)
# © 2015-2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from openerp import models, fields
from openerp import api


class Product(models.Model):
    _inherit = 'product.product'

    @api.onchange('length', 'height', 'width', 'dimensional_uom_id')
    def onchange_calculate_volume(self):
        if (not self.length or not self.height or not self.width or
                not self.dimensional_uom_id):
            return False

        length_m = self.convert_to_meters(self.length, self.dimensional_uom_id)
        height_m = self.convert_to_meters(self.height, self.dimensional_uom_id)
        width_m = self.convert_to_meters(self.width, self.dimensional_uom_id)
        self.volume = length_m * height_m * width_m

    def convert_to_meters(self, measure, dimensional_uom):
        uom_meters = self.env['product.uom'].search([('name', '=', 'm')])

        return self.env['product.uom']._compute_qty_obj(
            from_unit=dimensional_uom,
            qty=measure,
            to_unit=uom_meters)

    @api.model
    def _get_dimension_uom_domain(self):
        return [
            ('category_id', '=', self.env.ref('product.uom_categ_length').id)
        ]

    length = fields.Float()
    height = fields.Float()
    width = fields.Float()
    dimensional_uom_id = fields.Many2one(
        'product.uom',
        'Dimensional UoM',
        domain=_get_dimension_uom_domain,
        help='UoM for length, height, width')


class ProductTemplate(models.Model):

    _inherit = 'product.template'

    @api.onchange('length', 'height', 'width', 'dimensional_uom_id')
    def onchange_calculate_volume(self):
        if (not self.length or not self.height or not self.width or
                not self.dimensional_uom_id):
            return False

        length_m = self.convert_to_meters(self.length, self.dimensional_uom_id)
        height_m = self.convert_to_meters(self.height, self.dimensional_uom_id)
        width_m = self.convert_to_meters(self.width, self.dimensional_uom_id)
        self.volume = length_m * height_m * width_m

    def convert_to_meters(self, measure, dimensional_uom):
        uom_meters = self.env['product.uom'].search([('name', '=', 'm')])

        return self.env['product.uom']._compute_qty_obj(
            from_unit=dimensional_uom,
            qty=measure,
            to_unit=uom_meters)

    @api.model
    def create(self, vals):
        product_template_id = super(ProductTemplate, self).create(vals)
        # TODO: this is needed to set given values to first variant after creation
        # these fields should be moved to product as lead to confusion
        if vals.get('dimensional_uom_id'):
            related_vals = {}
            related_vals['dimensional_uom_id'] = vals['dimensional_uom_id']
            product_template_id.write(related_vals)
        return product_template_id

    length = fields.Float(related='product_variant_ids.length')
    height = fields.Float(related='product_variant_ids.height')
    width = fields.Float(related='product_variant_ids.width')
    dimensional_uom_id = fields.Many2one(
        'product.uom',
        'Dimensional UoM', related='product_variant_ids.dimensional_uom_id',
        help='UoM for length, height, width')
