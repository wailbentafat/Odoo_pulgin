from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    solde_fournisseur = fields.Monetary(
        compute='_compute_balances',
        string="Solde Fournisseur",
        currency_field='currency_id'
    )
    solde_client = fields.Monetary(
        compute='_compute_balances',
        string="Solde Client",
        currency_field='currency_id'
    )
    total_balance = fields.Monetary(
        compute='_compute_balances',
        string="Balance",
        currency_field='currency_id'
    )
    label_solde_fournisseur = fields.Char(
        compute='_compute_balances',
        string="Statut Fournisseur"
    )
    label_solde_client = fields.Char(
        compute='_compute_balances',
        string="Statut Client"
    )

    def _compute_balances(self):
        for partner in self:
            lines = self.env['account.move.line'].search([
                ('partner_id', '=', partner.id),
                ('move_id.state', '=', 'posted'),
            ])

            solde_fournisseur = 0.0
            solde_client = 0.0

            for line in lines:
                account_type = line.account_id.account_type
                if account_type == 'liability_payable':
                    solde_fournisseur += line.debit - line.credit
                elif account_type == 'asset_receivable':
                    solde_client += line.debit - line.credit

            partner.solde_fournisseur = solde_fournisseur
            partner.solde_client = solde_client
            partner.total_balance = solde_fournisseur + solde_client

            if solde_fournisseur > 0:
                partner.label_solde_fournisseur = "Dette Fournisseur"
            else:
                partner.label_solde_fournisseur = "Avance Fournisseur"

            if solde_client < 0:
                partner.label_solde_client = "Créance Client"
            else:
                partner.label_solde_client = "Avance Client"