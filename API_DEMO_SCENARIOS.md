# API Demo Scenarios

## 1. Setup Phase
**Req**: `POST /api/auth/register/` (Seller)
```json
{
  "email": "seller@store.com", "password": "pass", "role": "SELLER", 
  "business_name": "Tech World"
}
```

**Req**: `POST /api/auth/register/` (Buyer)
```json
{
  "email": "buyer@me.com", "password": "pass", "role": "BUYER"
}
```

---

## 2. Inventory Phase (Seller)
**Req**: `POST /api/products/`
header: `Authorization: Token <seller_token>`
```json
{
  "name": "Gaming Laptop",
  "description": "Fastest laptop",
  "variants": [
    { "sku": "LP-001", "name": "16GB RAM", "price": "1200.00", "stock_quantity": 10 }
  ]
}
```
*Note: Product status defaults to DRAFT or ACTIVE depending on settings. Assuming ACTIVE for demo.*

---

## 3. Shopping Phase (Buyer)
**Req**: `POST /api/orders/buyer/checkout/`
header: `Authorization: Token <buyer_token>`
```json
{
  "items": [
    { "variant_id": 1, "quantity": 1 }
  ],
  "shipping_address": { "street": "123 Main St", "city": "NY" },
  "billing_address": { "street": "123 Main St", "city": "NY" }
}
```
**Res**:
```json
{
  "id": 1,
  "total_amount": "1200.00",
  "status": "PAID"
}
```

---

## 4. Fulfillment Phase (Seller)
**Req**: `GET /api/orders/seller/`
**Res**: List of orders. Seller sees *SubOrder* #5.

**Req**: `POST /api/orders/seller/5/ship/`
```json
{
  "tracking_number": "UPS-99999",
  "carrier_name": "UPS",
  "estimated_delivery": "2026-01-20"
}
```
**Res**: `{"status": "Order Shipped"}`

---

## 5. Dispute Phase (Buyer)
**Req**: `POST /api/disputes/`
```json
{
  "order": 5, 
  "reason": "DAMAGED",
  "description": "Screen cracked upon arrival."
}
```
**Res**: Dispute created (ID 1), Status: OPEN.

---

## 6. Resolution Phase (Admin)
*Admin logs into Django Admin Panel, views Dispute #1, issues refund, and marks status RESOLVED.*
