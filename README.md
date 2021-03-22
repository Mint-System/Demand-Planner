# Demand Planner

Get order proposals for multi-level sub-products.

## Test Data

The test data set contains a manufacturing setup for two products. These products are assembled from manufactured and purchased parts.

### Mountain Bike

This is fictional product for testing puproses only.

![](test_data/Mountain%20Bike/Mountain%20Bike.png)

**BoM**

This is the bill of material with lead times:

![](test_data/Mountain%20Bike/BoM.png)

### Meldeeinheit PMA14

This is a real product from the customer.

![](test_data/Meldeeinheit%20PMA14/BoM.png)

## Import Sequence

Import csv files from the `test_data` folder.

1. Navigate to *Contacts* and import `res.partner.csv`
2. Navigate to *Manufacturing > Products > Product Variants* and import `product.product.csv`
3. Navigate to *Purchase > Configuration > Vendor Pricelists* and import `product.supplierinfo.csv`
4. Navigate to *Manufacturing > Products > Bills of Materials* and import `mrp.bom.csv`

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
