# Demand-Planner

Get order proposals for multi-level sub-products.

## Test Data

The test data set contains a manufacturing setup for a mountain bike. The product is assembled from manufactured and purchased parts.

![](static/description/Mountain%20Bike.png)

## Import Sequence

Import csv files from demo folder.

1. Import `res.partner.csv`
2. Import `product.template.csv`
3. Import `product.supplierinfo.csv`
4. Import `mrp.bom.csv`

### Export Templates

When exporting models use these fields and save as csv file.

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
