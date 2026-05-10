#!/usr/bin/env python3
import xmlrpc.client

url = "http://localhost:8069"
db = "odoo"
username = "admin"
password = "admin"

common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
uid = common.authenticate(db, username, password, {})
models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")

partner_id = 14  # Azure Interior

print("Creating customer invoice...")
invoice_id = models.execute_kw(db, uid, password, 'account.move', 'create', [{
    'move_type': 'out_invoice',
    'partner_id': partner_id,
    'journal_id': 1,
    'invoice_date': '2026-05-10',
    'invoice_line_ids': [[0, 0, {
        'name': 'Test Product',
        'quantity': 1,
        'price_unit': 500.00,
        'product_id': 4,
    }]]
}])

print(f"Created invoice ID: {invoice_id}")
models.execute_kw(db, uid, password, 'account.move', 'action_post', [invoice_id])
print("Customer invoice posted!")

print("\nCreating vendor bill...")
vendor_bill_id = models.execute_kw(db, uid, password, 'account.move', 'create', [{
    'move_type': 'in_invoice',
    'partner_id': partner_id,
    'journal_id': 2,
    'invoice_date': '2026-05-10',
    'invoice_line_ids': [[0, 0, {
        'name': 'Test Vendor Product',
        'quantity': 1,
        'price_unit': 200.00,
        'product_id': 5,
    }]]
}])

print(f"Created vendor bill ID: {vendor_bill_id}")
models.execute_kw(db, uid, password, 'account.move', 'action_post', [vendor_bill_id])
print("Vendor bill posted!")

print("\n=== TEST COMPLETE ===")
print(f"Go to Contact 'Azure Interior' (ID: {partner_id}) to see:")
print(f"  - Solde Client: -500.00 (green, Créance Client)")
print(f"  - Solde Fournisseur: 200.00 (red, Dette Fournisseur)")
print(f"  - Total Balance: -300.00")