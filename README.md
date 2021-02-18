# Demand-Planner

Get order proposals for multi-level sub-products.

## Testdata

### Export Templates

**product.product**

```
Name
Product Type
Cost
Manufacturing Lead Time
Customer Lead Time
Routes
```

**mrp.bom**

```
Product
Quantity
BoM Type
BoM Lines/Component
BoM Lines/Quantity
```

**product.supplierinfo**

```
Vendor
Product Template
Quantity
Price
Delivery Lead Time
```

**res.partner**

```
Name
Is a Company
```

## Import Sequence

1. Import `res.partner.csv`
2. Import `product.template.csv`
3. Import `product.suppliefinfo.csv`
4. Import `mrp.bom.csv`