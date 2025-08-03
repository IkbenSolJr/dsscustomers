# -*- coding: utf-8 -*-
from odoo import models, fields, api,  _
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError

class DsscustomersAccountPay(models.Model):
    _name = 'dsscustomers.ketoan'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'DSS Customers Accounting Pay'
    _rec_name = 'khachhangkt_ids'

    sottktoan = fields.Char(string='Stt', copy=False, readonly=True, default=lambda self: _('New'))
    khachhangkt_ids = fields.Many2one('dsscustomers.dsscustomers', string="Khách hàng",required=True)
    masokh = fields.Char(related = 'khachhangkt_ids.masokh',store=True)
    visa = fields.Selection(related = 'khachhangkt_ids.visa',store=True)
    phonekh = fields.Char(related = 'khachhangkt_ids.phonekh',store=True)
    phonekh = fields.Char(related = 'khachhangkt_ids.phonekh',store=True)
    emailkh = fields.Char(related = 'khachhangkt_ids.emailkh',store=True)
    giaidoantt = fields.Selection([
    ('thanhtoangdmot', 'Đợt 1'),
    ('thanhtoangdhai', 'Đợt 2'),
    ('thanhtoangdba', 'Đợt 3'),
    ('thanhtoangdbon', 'Đợt 4'),
    ('thanhtoangdnam', 'Đợt 5'),
    ('thanhtoangdsau', 'Đợt 6'),
    ('thanhtoangdbay', 'Đợt 7'),
    ('thanhtoangdtam', 'Đợt 8')],
    string="Giai đoạn", default=False)
    lanthanhtoan = fields.Selection([
    ('ttlanmot', 'Lần 1'),
    ('ttlanhai', 'Lần 2'),
    ('ttlanba', 'Lần 3'),
    ('ttlanbon', 'Lần 4')],
    string="Số lần", default=False)
    ngaydukien = fields.Date(string="Ngày dự kiến")
    sotiendukien = fields.Monetary(string="Số tiền dự kiến",currency_field='currency_id')
    ngaytt = fields.Date(string="Ngày thực thu")
    sotientt = fields.Monetary(string="Số tiền thực thu",currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', string="Đơn vị tiền", store=True, readonly=False)    
    phihopdong = fields.Monetary(related = 'khachhangkt_ids.phihopdong',currency_field='currency_ids')
    currency_ids = fields.Many2one('res.currency', related = 'khachhangkt_ids.currency_id',string="Đơn vị tiền")
    ngaychothd = fields.Date(related = 'khachhangkt_ids.ngaychothd')
    ktcheck = fields.Boolean('Kế toán kiểm tra', tracking=True)
    user_id = fields.Many2one(related = 'khachhangkt_ids.user_id',store=True)
    teamphutrach = fields.Many2one(related = 'khachhangkt_ids.teamphutrach',store=True)
    percentage = fields.Float("Tỷ lệ %", compute='_compute_percentage',
                              store=True)


    @api.model
    def create(self, vals):
        if vals.get('sottktoan', _('New')) == _('New'):
           vals['sottktoan'] = self.env['ir.sequence'].next_by_code('dsscustomers.ketoan') or _('New')
        res = super(DsscustomersAccountPay, self).create(vals)
        return res   

    @api.depends('sotientt','sotiendukien')
    def _compute_percentage(self):
        for record in self:
              if (record.sotientt == 0.0) or (record.sotiendukien == 0.0):
                record.percentage = 0
              else:  record.percentage = (record.sotientt/record.sotiendukien) * 100