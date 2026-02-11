# FY2025 owed-candidate report (conservative)
This report lists *invoice* evidence documents whose **CAD totals** do not match 1:1 with any single ingested statement transaction (exact match by absolute CAD amount).

- This is a review aid only; it is **not** proof that an invoice is unpaid.
- Follow the repo gating rules before creating any `owed.csv` entries (confirm statement coverage).
## Summary
- Invoices scanned: 279
- CAD invoices with no exact 1:1 statement amount match: 33
- Non-CAD invoices (not evaluated for 1:1): 69

## CAD invoice candidates (no exact 1:1 match)
### doc-20250102-amazon-canada-40.57CAD-6bba4ccceb
- document_date: `2025-01-02`
- vendor: `Amazon Canada`
- amount: `40.57 CAD`
- source_file: `FY2025/transactions/5_expenses/Amazon_Canada_2025-01-02_CA5MPJAACCUI.md`
- linked_transactions: 0
- nearest_statement_amounts (by abs amount delta):
  - delta 0.06 | tx-2025-cc-20250707-640afc4b55 | 2025-07-07 | cad_amount -40.51 | corporate/TD Business VISA | OPENPHONE OPENPHONE.CO FOREIGN CURRENCY 29.00 USD @ EXCHANGE RATE
  - delta 0.17 | tx-2025-cc-20250811-caf3b24e87 | 2025-08-11 | cad_amount -40.40 | corporate/TD Business VISA | PAYPAL *GODADDY.COM 4029357733
  - delta 0.18 | tx-2025-cc-20250425-a9167514d9 | 2025-04-25 | cad_amount -40.39 | personal/TD Personal VISA | SAFEWAY #4905 NORTH VANCOU

### doc-20250120-amazon-canada-109.75CAD-2cfdff036d
- document_date: `2025-01-20`
- vendor: `Amazon Canada`
- amount: `109.75 CAD`
- source_file: `FY2025/transactions/5_expenses/Amazon_Canada_2025-01-20_CA511IFEJB4I.md`
- linked_transactions: 0
- nearest_statement_amounts (by abs amount delta):
  - delta 0.01 | tx-2025-cc-20251021-25b15aff30 | 2025-10-21 | cad_amount 109.76 | personal/TD Personal VISA | LaMaisonSimons West Vancouv
  - delta 0.47 | tx-2025-cc-20250515-5f25fe4f83 | 2025-05-15 | cad_amount -109.28 | personal/TD Personal VISA | SHELL EASYPAY C01285 NORTH
  - delta 1.13 | tx-2025-cc-20251014-8d351c370b | 2025-10-14 | cad_amount -110.88 | personal/TD Personal VISA | LaMaisonSimons West Vancouv

### doc-20250131-jinwei-heller-xu-3150.00CAD-d2e703144a
- document_date: `2025-01-31`
- vendor: `Jinwei (Heller) Xu`
- amount: `3150.00 CAD`
- source_file: `FY2025/transactions/5_expenses/Jinwei_(Heller)_Xu_2025-01-31.md`
- linked_transactions: 0
- nearest_statement_amounts (by abs amount delta):
  - delta 110.76 | tx-2025-cc-20251015-e7b288b96b | 2025-10-15 | cad_amount -3039.24 | personal/TD Personal VISA | WHOLE FOODS MARKET VANCOUVER
  - delta 250.00 | tx-2025-bank-20250730-051d08f2ca | 2025-07-30 | cad_amount -2900.00 | corporate/TD Business Chequing | HJ544 TFR-TO 6084079
  - delta 250.00 | tx-2025-bank-20251031-2edbdb9506 | 2025-10-31 | cad_amount -2900.00 | corporate/TD Business Chequing | JW375 TFR-TO 6084079

### doc-20250304-amazon-canada-21.99CAD-3289977e78
- document_date: `2025-03-04`
- vendor: `Amazon Canada`
- amount: `21.99 CAD`
- source_file: `FY2025/transactions/5_expenses/Amazon_Canada_2025-03-04_CA514YQDM9CEI.md`
- linked_transactions: 0
- nearest_statement_amounts (by abs amount delta):
  - delta 0.09 | tx-2025-cc-20250515-24c41b5611 | 2025-05-15 | cad_amount -21.90 | corporate/TD Business VISA | NAMESPRO SOLUTIONS INC. RICHMOND
  - delta 0.13 | tx-2025-cc-20250730-13e3eb071f | 2025-07-30 | cad_amount -21.86 | personal/TD Personal VISA | Amazon.ca*DG9U141I3 AMAZON.CA
  - delta 0.13 | tx-2025-cc-20251029-9e6b6d3cda | 2025-10-29 | cad_amount -21.86 | personal/TD Personal VISA | Amazon.ca*N46Q17Y50 866-216-1072

### doc-20250403-amazon-canada-41.43CAD-a87e49feb5
- document_date: `2025-04-03`
- vendor: `Amazon Canada`
- amount: `41.43 CAD`
- source_file: `FY2025/transactions/5_expenses/Amazon_Canada_2025-04-03_CA5E0VS7E1CI.md`
- linked_transactions: 0
- nearest_statement_amounts (by abs amount delta):
  - delta 0.08 | tx-2025-cc-20250411-b0e0ca5d85 | 2025-04-11 | cad_amount -41.35 | personal/TD Personal VISA | Amazon.ca*XK5XS6JV3 AMAZON.CA
  - delta 0.10 | tx-2025-cc-20251006-8e79225196 | 2025-10-06 | cad_amount -41.53 | corporate/TD Business VISA | OPENPHONE QUO.COM FOREIGN CURRENCY 29.00
  - delta 0.16 | tx-2025-cc-20250805-e1f00eafbb | 2025-08-05 | cad_amount -41.27 | corporate/TD Business VISA | OPENPHONE OPENPHONE.CO FOREIGN CURRENCY

### doc-20250513-namespro-59.28CAD-d059ec2782
- document_date: `2025-05-13`
- vendor: `Namespro`
- amount: `59.28 CAD`
- source_file: `FY2025/transactions/5_expenses/Namespro_2025-05-13.md`
- linked_transactions: 0
- nearest_statement_amounts (by abs amount delta):
  - delta 0.36 | tx-2025-cc-20251001-284cbd7a5e | 2025-10-01 | cad_amount -58.92 | corporate/TD Business VISA | TST-Social Corner - Co Vancouver
  - delta 0.63 | tx-2025-cc-20250807-d021fa7d62 | 2025-08-07 | cad_amount -58.65 | corporate/TD Business VISA | UBER *TRIP HELP.UBER.CO
  - delta 0.64 | tx-2025-cc-20250731-88f3bf8972 | 2025-07-31 | cad_amount -59.92 | corporate/TD Business VISA | NAMESPRO SOLUTIONS INC. RICHMOND

### doc-20250620-vancouver-headshots-236.25CAD-1057babc2a
- document_date: `2025-06-20`
- vendor: `Vancouver Headshots`
- amount: `236.25 CAD`
- source_file: `FY2025/transactions/5_expenses/Vancouver_Headshots_2025-06-20_Invoice_#006052_-_Square.md`
- linked_transactions: 0
- nearest_statement_amounts (by abs amount delta):
  - delta 0.33 | tx-2025-cc-20250711-c0788fafb8 | 2025-07-11 | cad_amount -236.58 | personal/TD Personal VISA | EXPEDIA 73169634538824 EXPEDIA.CA
  - delta 1.05 | tx-2025-cc-20250721-0a7e9d3291 | 2025-07-21 | cad_amount -235.20 | personal/TD Personal VISA | JLR CANADA ULC MISSISSAUGA
  - delta 6.25 | tx-2025-cc-20251021-b5925d9b68 | 2025-10-21 | cad_amount -230.00 | corporate/TD Business VISA | HAWKSWORTH RESTAURANT

### doc-20250620-vancouver-headshots-236.25CAD-2499db082a
- document_date: `2025-06-20`
- vendor: `Vancouver Headshots`
- amount: `236.25 CAD`
- source_file: `FY2025/transactions/5_expenses/Vancouver_Headshots_2025-06-20_Invoice_#006052_[Obsolete].md`
- doc_notes: amount inferred (no explicit Total/Amount Due marker nearby)
- linked_transactions: 0
- nearest_statement_amounts (by abs amount delta):
  - delta 0.33 | tx-2025-cc-20250711-c0788fafb8 | 2025-07-11 | cad_amount -236.58 | personal/TD Personal VISA | EXPEDIA 73169634538824 EXPEDIA.CA
  - delta 1.05 | tx-2025-cc-20250721-0a7e9d3291 | 2025-07-21 | cad_amount -235.20 | personal/TD Personal VISA | JLR CANADA ULC MISSISSAUGA
  - delta 6.25 | tx-2025-cc-20251021-b5925d9b68 | 2025-10-21 | cad_amount -230.00 | corporate/TD Business VISA | HAWKSWORTH RESTAURANT

### doc-20250622-amazon-canada-98.20CAD-49645b08d4
- document_date: `2025-06-22`
- vendor: `Amazon Canada`
- amount: `98.20 CAD`
- source_file: `FY2025/transactions/5_expenses/Amazon_Canada_2025-06-22_CA51PIXWDACCUI.md`
- linked_transactions: 0
- nearest_statement_amounts (by abs amount delta):
  - delta 0.02 | tx-2025-cc-20250805-09744ce85e | 2025-08-05 | cad_amount -98.18 | corporate/TD Business VISA | TST*NOVO RESTAURANT &LO San Luis
  - delta 0.42 | tx-2025-cc-20250729-f6221d502c | 2025-07-29 | cad_amount -98.62 | personal/TD Personal VISA | NICDEPT PARKS WEBSI EGOV.COM FOREIGN
  - delta 0.74 | tx-2025-cc-20250908-e4693539a4 | 2025-09-08 | cad_amount -98.94 | corporate/TD Business VISA | LIFT BAR GRILL VIEW VANCOUVER

### doc-20250625-namespro-15.68CAD-2897884123
- document_date: `2025-06-25`
- vendor: `Namespro`
- amount: `15.68 CAD`
- source_file: `FY2025/transactions/5_expenses/Namespro_2025-06-25.md`
- linked_transactions: 0
- nearest_statement_amounts (by abs amount delta):
  - delta 0.01 | tx-2025-cc-20250428-e4efb9f3cf | 2025-04-28 | cad_amount -15.67 | corporate/TD Business VISA | AMZN Mktp CA*NB0O02F62
  - delta 0.01 | tx-2025-cc-20250730-ee25eaa046 | 2025-07-30 | cad_amount -15.69 | personal/TD Personal VISA | Amazon.ca*X682Z27L3 AMAZON.CA
  - delta 0.03 | tx-2025-cc-20250306-10b571890e | 2025-03-06 | cad_amount -15.65 | personal/TD Personal VISA | Amazon.ca*TX1IB2ZK3 AMAZON.CA

### doc-20250630-digitalocean-0.62CAD-3b2281c217
- document_date: `2025-06-30`
- vendor: `DigitalOcean`
- amount: `0.62 CAD`
- source_file: `FY2025/transactions/5_expenses/DigitalOcean_2025-06-30.md`
- doc_notes: amount inferred (no explicit Total/Amount Due marker nearby)
- linked_transactions: 0
- nearest_statement_amounts (by abs amount delta):
  - delta 0.03 | tx-2025-cc-20250724-89eefc9365 | 2025-07-24 | cad_amount -0.65 | personal/TD Personal VISA | CITY OF VAN PAYBYPHONE VANCOUVER
  - delta 0.04 | tx-2025-cc-20251006-89fa5264db | 2025-10-06 | cad_amount -0.58 | corporate/TD Business VISA | CASH INTEREST
  - delta 0.08 | tx-2025-cc-20250724-0108483131 | 2025-07-24 | cad_amount -0.54 | personal/TD Personal VISA | CITY OF VAN PAYBYPHONE VANCOUVER

### doc-20250709-uber-5.70CAD-a023c2672d
- document_date: `2025-07-09`
- vendor: `Uber`
- amount: `5.70 CAD`
- source_file: `FY2025/transactions/5_expenses/Uber_2025-07-09_receipt_665d08ea-d9b5-4487-9523-80fc03b02be9.md`
- linked_transactions: 0
- nearest_statement_amounts (by abs amount delta):
  - delta 0.02 | tx-2025-cc-20250305-7c5a1fa628 | 2025-03-05 | cad_amount -5.68 | personal/TD Personal VISA | Amazon.ca*3Q2HL3X13 AMAZON.CA
  - delta 0.02 | tx-2025-cc-20250407-6fb0f04dae | 2025-04-07 | cad_amount -5.68 | personal/TD Personal VISA | Amazon.ca*MY0Z87N63 AMAZON.CA
  - delta 0.02 | tx-2025-cc-20250430-6c59a703ac | 2025-04-30 | cad_amount -5.68 | personal/TD Personal VISA | Amazon.ca*WH5I040B3 AMAZON.CA

### doc-20250731-digitalocean-14.79CAD-f2ce4a406a
- document_date: `2025-07-31`
- vendor: `DigitalOcean`
- amount: `14.79 CAD`
- source_file: `FY2025/transactions/5_expenses/DigitalOcean_2025-07-31.md`
- doc_notes: amount inferred (no explicit Total/Amount Due marker nearby)
- linked_transactions: 0
- nearest_statement_amounts (by abs amount delta):
  - delta 0.03 | tx-2025-cc-20250805-555d007e65 | 2025-08-05 | cad_amount -14.82 | personal/TD Personal VISA | WHOLEFDS SCA #10633 SANTA CLARA
  - delta 0.09 | tx-2025-cc-20250505-ab0e568de9 | 2025-05-05 | cad_amount -14.70 | personal/TD Personal VISA | ZIPBY MISSISSAUGA
  - delta 0.09 | tx-2025-cc-20250715-2060d7c5d8 | 2025-07-15 | cad_amount -14.70 | corporate/TD Business VISA | UBER CANADA/UBERTRIP

### doc-20250804-uber-42.93CAD-f505cd2264
- document_date: `2025-08-04`
- vendor: `Uber`
- amount: `42.93 CAD`
- source_file: `FY2025/transactions/5_expenses/Uber_2025-08-04_receipt_5430386c-c82d-4839-8e9b-ec02233f7b2c.md`
- linked_transactions: 0
- nearest_statement_amounts (by abs amount delta):
  - delta 0.02 | tx-2025-cc-20250527-df1be986e3 | 2025-05-27 | cad_amount -42.95 | personal/TD Personal VISA | WHOLE FOODS MARKET VANCOUVER
  - delta 0.09 | tx-2025-cc-20250324-4772f23458 | 2025-03-24 | cad_amount -42.84 | personal/TD Personal VISA | HOMER ST CAFE AND BAR VANCOUVER
  - delta 0.12 | tx-2025-cc-20250422-b35afce53e | 2025-04-22 | cad_amount -43.05 | personal/TD Personal VISA | PAYPAL *UBER 4029357733

### doc-20250805-uber-41.46CAD-5c3fb50cbd
- document_date: `2025-08-05`
- vendor: `Uber`
- amount: `41.46 CAD`
- source_file: `FY2025/transactions/5_expenses/Uber_2025-08-05_receipt_6f6ec47d-c3b3-46ca-8bb1-817e920da00a.md`
- linked_transactions: 0
- nearest_statement_amounts (by abs amount delta):
  - delta 0.07 | tx-2025-cc-20251006-8e79225196 | 2025-10-06 | cad_amount -41.53 | corporate/TD Business VISA | OPENPHONE QUO.COM FOREIGN CURRENCY 29.00
  - delta 0.11 | tx-2025-cc-20250411-b0e0ca5d85 | 2025-04-11 | cad_amount -41.35 | personal/TD Personal VISA | Amazon.ca*XK5XS6JV3 AMAZON.CA
  - delta 0.16 | tx-2025-cc-20250407-27e7fa556c | 2025-04-07 | cad_amount -41.62 | personal/TD Personal VISA | Amazon.ca*7M3K41US3 AMAZON.CA

### doc-20250831-digitalocean-12.12CAD-f63924c699
- document_date: `2025-08-31`
- vendor: `DigitalOcean`
- amount: `12.12 CAD`
- source_file: `FY2025/transactions/5_expenses/DigitalOcean_2025-08-31.md`
- doc_notes: amount inferred (no explicit Total/Amount Due marker nearby)
- linked_transactions: 0
- nearest_statement_amounts (by abs amount delta):
  - delta 0.02 | tx-2025-cc-20250306-0a70b38c4f | 2025-03-06 | cad_amount -12.10 | personal/TD Personal VISA | Amazon.ca*MF04O8513 AMAZON.CA
  - delta 0.06 | tx-2025-cc-20250310-7e5a800169 | 2025-03-10 | cad_amount -12.18 | personal/TD Personal VISA | WHOLE FOODS MARKET WEST VANCOUV
  - delta 0.07 | tx-2025-cc-20250107-9d8e7935ac | 2025-01-07 | cad_amount -12.05 | corporate/TD Business VISA | PAYPAL *GITHUB INC 4029357733

### doc-20250831-jinwei-heller-xu-4830.00CAD-fb82e1fdf5
- document_date: `2025-08-31`
- vendor: `Jinwei (Heller) Xu`
- amount: `4830.00 CAD`
- source_file: `FY2025/transactions/5_expenses/Jinwei_(Heller)_Xu_2025-08-31.md`
- linked_transactions: 0
- nearest_statement_amounts (by abs amount delta):
  - delta 170.00 | tx-2025-bank-20250115-e634606b63 | 2025-01-15 | cad_amount -5000.00 | corporate/TD Business Chequing | HW293 TFR-TO 6084079
  - delta 530.00 | tx-2025-bank-20250515-1d6609749b | 2025-05-15 | cad_amount -4300.00 | corporate/TD Business Chequing | IJ391 TFR-TO 6084079
  - delta 557.31 | tx-2025-bank-20250929-322eb13e55 | 2025-09-29 | cad_amount 5387.31 | corporate/TD Business Chequing | E-TRANSFER ***PyD

### doc-20250914-uber-7.59CAD-ec3dd5432d
- document_date: `2025-09-14`
- vendor: `Uber`
- amount: `7.59 CAD`
- source_file: `FY2025/transactions/5_expenses/Uber_2025-09-14_receipt_614ba2a3-380e-467c-a7dc-7e9f41580a3a.md`
- linked_transactions: 0
- nearest_statement_amounts (by abs amount delta):
  - delta 0.01 | tx-2025-cc-20250605-17f76eec9a | 2025-06-05 | cad_amount -7.58 | personal/TD Personal VISA | Amazon.ca*N65CG1BK1 AMAZON.CA
  - delta 0.01 | tx-2025-cc-20251029-6c6347fa33 | 2025-10-29 | cad_amount -7.58 | personal/TD Personal VISA | Amazon.ca*NK5FM7CF0 866-216-1072
  - delta 0.04 | tx-2025-cc-20250602-492abbe45f | 2025-06-02 | cad_amount -7.63 | corporate/TD Business VISA | UBER* TRIP UBER.COM/CA/

### doc-20250930-digitalocean-5.94CAD-d7fcc6c381
- document_date: `2025-09-30`
- vendor: `DigitalOcean`
- amount: `5.94 CAD`
- source_file: `FY2025/transactions/5_expenses/DigitalOcean_2025-09-30.md`
- linked_transactions: 0
- nearest_statement_amounts (by abs amount delta):
  - delta 0.06 | tx-2025-cc-20250630-5fdfbba44b | 2025-06-30 | cad_amount -6.00 | personal/TD Personal VISA | FALSE CREEK FERRIES VANCOUVER
  - delta 0.10 | tx-2025-cc-20251028-140c46d7de | 2025-10-28 | cad_amount -6.04 | personal/TD Personal VISA | BC PLACE VANCOUVER
  - delta 0.12 | tx-2025-cc-20250704-d3dde697c7 | 2025-07-04 | cad_amount -6.06 | personal/TD Personal VISA | Amazon.ca*N34ES0WO2 AMAZON.CA

### doc-20250930-jinwei-heller-xu-4410.00CAD-00b09928bd
- document_date: `2025-09-30`
- vendor: `Jinwei (Heller) Xu`
- amount: `4410.00 CAD`
- source_file: `FY2025/transactions/5_expenses/Jinwei_(Heller)_Xu_2025-09-30.md`
- linked_transactions: 0
- nearest_statement_amounts (by abs amount delta):
  - delta 110.00 | tx-2025-bank-20250515-1d6609749b | 2025-05-15 | cad_amount -4300.00 | corporate/TD Business Chequing | IJ391 TFR-TO 6084079
  - delta 210.00 | tx-2025-bank-20250113-0d3ba02571 | 2025-01-13 | cad_amount 4200.00 | corporate/TD Business Chequing | E-TRANSFER ***T3z
  - delta 210.00 | tx-2025-bank-20250117-0180d16fa3 | 2025-01-17 | cad_amount 4200.00 | corporate/TD Business Chequing | E-TRANSFER ***6CW

### doc-20251001-screenconnect-216.75CAD-ff83c06877
- document_date: `2025-10-01`
- vendor: `ScreenConnect`
- amount: `216.75 CAD`
- source_file: `FY2025/transactions/5_expenses/ScreenConnect_2025-10-01_Quantity_and_Payment.md`
- linked_transactions: 0
- nearest_statement_amounts (by abs amount delta):
  - delta 0.44 | tx-2025-cc-20250714-7c95ef8c53 | 2025-07-14 | cad_amount -217.19 | corporate/TD Business VISA | ANDONIS VANCOUVER VANCOUVER
  - delta 0.45 | tx-2025-cc-20250520-761f5cdbcd | 2025-05-20 | cad_amount -216.30 | personal/TD Personal VISA | SP SWAGGER AJAX
  - delta 1.58 | tx-2025-cc-20250505-aa9f92d4dd | 2025-05-05 | cad_amount -215.17 | corporate/TD Business VISA | TST-Brix and Mortar Vancouver

### doc-20251001-screenconnect-64.65CAD-9ba4e1bbd8
- document_date: `2025-10-01`
- vendor: `ScreenConnect`
- amount: `64.65 CAD`
- source_file: `FY2025/transactions/5_expenses/ScreenConnect_2025-10-01_Standard_Subscription_Billed_Every_Month_Started.md`
- doc_notes: amount inferred (no explicit Total/Amount Due marker nearby)
- linked_transactions: 0
- nearest_statement_amounts (by abs amount delta):
  - delta 0.07 | tx-2025-cc-20251229-96916ab45c | 2025-12-29 | cad_amount -64.58 | personal/TD Personal VISA | CINEPLEX REC ROOM 1002 VANCOUVER
  - delta 0.27 | tx-2025-cc-20250407-9c6cd23d2e | 2025-04-07 | cad_amount -64.38 | personal/TD Personal VISA | DAN DAN NOODLE VANCOUVER
  - delta 0.28 | tx-2025-cc-20251208-1d3232b638 | 2025-12-08 | cad_amount -64.37 | corporate/TD Business VISA | AMZN Mktp CA*BI9S32WF1 866-216-1072

### doc-20251031-digitalocean-5.94CAD-1d569b10f4
- document_date: `2025-10-31`
- vendor: `DigitalOcean`
- amount: `5.94 CAD`
- source_file: `FY2025/transactions/5_expenses/DigitalOcean_2025-10-31.md`
- linked_transactions: 0
- nearest_statement_amounts (by abs amount delta):
  - delta 0.06 | tx-2025-cc-20250630-5fdfbba44b | 2025-06-30 | cad_amount -6.00 | personal/TD Personal VISA | FALSE CREEK FERRIES VANCOUVER
  - delta 0.10 | tx-2025-cc-20251028-140c46d7de | 2025-10-28 | cad_amount -6.04 | personal/TD Personal VISA | BC PLACE VANCOUVER
  - delta 0.12 | tx-2025-cc-20250704-d3dde697c7 | 2025-07-04 | cad_amount -6.06 | personal/TD Personal VISA | Amazon.ca*N34ES0WO2 AMAZON.CA

### doc-20251031-jinwei-heller-xu-3780.00CAD-087dba246f
- document_date: `2025-10-31`
- vendor: `Jinwei (Heller) Xu`
- amount: `3780.00 CAD`
- source_file: `FY2025/transactions/5_expenses/Jinwei_(Heller)_Xu_2025-10-31.md`
- linked_transactions: 0
- nearest_statement_amounts (by abs amount delta):
  - delta 30.00 | tx-2025-bank-20251114-a9fa67fec1 | 2025-11-14 | cad_amount 3750.00 | corporate/TD Business Chequing | E-TRANSFER ***XEz
  - delta 180.00 | tx-2025-bank-20250131-67e22a8356 | 2025-01-31 | cad_amount -3600.00 | corporate/TD Business Chequing | JJ074 TFR-TO 6084079
  - delta 220.00 | tx-2025-bank-20250514-e761c50695 | 2025-05-14 | cad_amount 4000.00 | corporate/TD Business Chequing | E-TRANSFER ***559

### doc-20251116-amazon-canada-55.94CAD-193f5fe959
- document_date: `2025-11-16`
- vendor: `Amazon Canada`
- amount: `55.94 CAD`
- source_file: `FY2025/transactions/5_expenses/Amazon_Canada_2025-11-16_CA5MNKEYCL4I.md`
- linked_transactions: 0
- nearest_statement_amounts (by abs amount delta):
  - delta 0.01 | tx-2025-cc-20251201-476312b5c7 | 2025-12-01 | cad_amount -55.95 | corporate/TD Business VISA | PAYPAL *PP* FS TECHSMIT 4029357733
  - delta 0.05 | tx-2025-cc-20250407-5daca7d8da | 2025-04-07 | cad_amount -55.99 | personal/TD Personal VISA | AMAZON.COM.CA www.amazon.c
  - delta 0.06 | tx-2025-cc-20250112-83e39c7838 | 2025-01-12 | cad_amount -56.00 | personal/TD Personal VISA | PREVIOUS STATEMENT BALANCE $594.62

### doc-20251128-staples-79.13CAD-57e67c636c
- document_date: `2025-11-28`
- vendor: `Staples`
- amount: `79.13 CAD`
- source_file: `FY2025/transactions/5_expenses/Staples_2025-11-28_Invoice_for_Order_#45413109.md`
- linked_transactions: 0
- nearest_statement_amounts (by abs amount delta):
  - delta 0.39 | tx-2025-cc-20250630-41aa1e8e34 | 2025-06-30 | cad_amount 79.52 | personal/TD Personal VISA | PAYPAL *WGWSB JEANS 4029357733
  - delta 0.51 | tx-2025-cc-20250624-522eb2f5a3 | 2025-06-24 | cad_amount -79.64 | corporate/TD Business VISA | NAMESPRO SOLUTIONS INC. RICHMOND
  - delta 0.71 | tx-2025-cc-20250317-c208a8d4da | 2025-03-17 | cad_amount -78.42 | personal/TD Personal VISA | Amazon.ca*J71021A73 AMAZON.CA

### doc-20251129-techsmith-53.29CAD-26e6f0b4fc
- document_date: `2025-11-29`
- vendor: `TechSmith`
- amount: `53.29 CAD`
- source_file: `FY2025/transactions/5_expenses/TechSmith_2025-11-29.md`
- linked_transactions: 0
- nearest_statement_amounts (by abs amount delta):
  - delta 0.05 | tx-2025-cc-20250730-7b775241c9 | 2025-07-30 | cad_amount -53.34 | personal/TD Personal VISA | SAFEWAY #4905 NORTH VANCOU
  - delta 0.14 | tx-2025-cc-20250326-ff6876f4b5 | 2025-03-26 | cad_amount -53.15 | personal/TD Personal VISA | CHV43001 BURRARD CHEVR VANCOUVER
  - delta 0.26 | tx-2025-cc-20250704-353b2056fa | 2025-07-04 | cad_amount -53.03 | personal/TD Personal VISA | Amazon.ca*N354W8WZ2 AMAZON.CA

### doc-20251130-digitalocean-5.94CAD-8833a892c5
- document_date: `2025-11-30`
- vendor: `DigitalOcean`
- amount: `5.94 CAD`
- source_file: `FY2025/transactions/5_expenses/DigitalOcean_2025-11-30.md`
- linked_transactions: 0
- nearest_statement_amounts (by abs amount delta):
  - delta 0.06 | tx-2025-cc-20250630-5fdfbba44b | 2025-06-30 | cad_amount -6.00 | personal/TD Personal VISA | FALSE CREEK FERRIES VANCOUVER
  - delta 0.10 | tx-2025-cc-20251028-140c46d7de | 2025-10-28 | cad_amount -6.04 | personal/TD Personal VISA | BC PLACE VANCOUVER
  - delta 0.12 | tx-2025-cc-20250704-d3dde697c7 | 2025-07-04 | cad_amount -6.06 | personal/TD Personal VISA | Amazon.ca*N34ES0WO2 AMAZON.CA

### doc-20251130-jinwei-heller-xu-3150.00CAD-1a8522aa4b
- document_date: `2025-11-30`
- vendor: `Jinwei (Heller) Xu`
- amount: `3150.00 CAD`
- source_file: `FY2025/transactions/5_expenses/Jinwei_(Heller)_Xu_2025-11-30.md`
- doc_notes: amount inferred (no explicit Total/Amount Due marker nearby)
- linked_transactions: 0
- nearest_statement_amounts (by abs amount delta):
  - delta 110.76 | tx-2025-cc-20251015-e7b288b96b | 2025-10-15 | cad_amount -3039.24 | personal/TD Personal VISA | WHOLE FOODS MARKET VANCOUVER
  - delta 250.00 | tx-2025-bank-20250730-051d08f2ca | 2025-07-30 | cad_amount -2900.00 | corporate/TD Business Chequing | HJ544 TFR-TO 6084079
  - delta 250.00 | tx-2025-bank-20251031-2edbdb9506 | 2025-10-31 | cad_amount -2900.00 | corporate/TD Business Chequing | JW375 TFR-TO 6084079

### doc-20251206-amazon-canada-46.46CAD-394dd53df8
- document_date: `2025-12-06`
- vendor: `Amazon Canada`
- amount: `46.46 CAD`
- source_file: `FY2025/transactions/5_expenses/Amazon_Canada_2025-12-06_CA5488HJHZ6I.md`
- linked_transactions: 0
- nearest_statement_amounts (by abs amount delta):
  - delta 0.04 | tx-2025-cc-20250324-a96c22c7e3 | 2025-03-24 | cad_amount -46.50 | personal/TD Personal VISA | VANCOUVER INTERNATIONAL A LANGLEY
  - delta 0.96 | tx-2025-cc-20250514-6882b4f0c0 | 2025-05-14 | cad_amount -45.50 | personal/TD Personal VISA | VAGARO* BEAUTY VAULT V
  - delta 1.00 | tx-2025-cc-20250414-bdcfa930e9 | 2025-04-14 | cad_amount -47.46 | personal/TD Personal VISA | BLACK TOP & CHECKER CABS

### doc-20251209-amazon-canada-31.50CAD-dd8907308d
- document_date: `2025-12-09`
- vendor: `Amazon Canada`
- amount: `31.50 CAD`
- source_file: `FY2025/transactions/5_expenses/Amazon_Canada_2025-12-09_CA515LE4L7W30I.md`
- linked_transactions: 0
- nearest_statement_amounts (by abs amount delta):
  - delta 0.19 | tx-2025-cc-20250416-98956827be | 2025-04-16 | cad_amount -31.31 | personal/TD Personal VISA | PAYPAL *UBERPAYMENT 35314369001
  - delta 0.60 | tx-2025-cc-20250317-6c1f8a90fd | 2025-03-17 | cad_amount -30.90 | personal/TD Personal VISA | AIR CAN* 0144284504317 AIRCANADA.CO
  - delta 0.60 | tx-2025-cc-20250317-71e1e4f254 | 2025-03-17 | cad_amount -30.90 | personal/TD Personal VISA | AIR CAN* 0144284504316 AIRCANADA.CO

### doc-20251224-rogers-320.83CAD-b406ea952c
- document_date: `2025-12-24`
- vendor: `Rogers`
- amount: `320.83 CAD`
- source_file: `FY2025/transactions/5_expenses/Rogers_2025-12-24.md`
- linked_transactions: 0
- nearest_statement_amounts (by abs amount delta):
  - delta 3.28 | tx-2025-bank-20250225-c2700d8c8e | 2025-02-25 | cad_amount -317.55 | corporate/TD Business Chequing | GST-B 4245035    BUS
  - delta 7.23 | tx-2025-cc-20251229-7145c94884 | 2025-12-29 | cad_amount -313.60 | personal/TD Personal VISA | AMAZON.COM.CA www.amazon.c
  - delta 12.20 | tx-2025-cc-20250609-a0fa5b4868 | 2025-06-09 | cad_amount -308.63 | corporate/TD Business VISA | ROGERS ******1233 888-764-3771

### doc-20261231-digitalocean-4.88CAD-441f190776
- document_date: `2026-12-31`
- vendor: `DigitalOcean`
- amount: `4.88 CAD`
- source_file: `FY2025/transactions/5_expenses/DigitalOcean_2026-12-31.md`
- doc_notes: amount inferred (no explicit Total/Amount Due marker nearby)
- linked_transactions: 0
- nearest_statement_amounts (by abs amount delta):
  - delta 0.04 | tx-2025-cc-20250602-195460e116 | 2025-06-02 | cad_amount -4.84 | corporate/TD Business VISA | GOOGLE*GSUITE KEFELAN. CC GOOGLE.CO
  - delta 0.13 | tx-2025-cc-20250505-ca2b257034 | 2025-05-05 | cad_amount -4.75 | personal/TD Personal VISA | ZIPBY MISSISSAUGA
  - delta 0.13 | tx-2025-cc-20250605-0ebb220f4f | 2025-06-05 | cad_amount -4.75 | personal/TD Personal VISA | Amazon.ca*N69EY3P50 AMAZON.CA

## Non-CAD invoices (manual review)
- doc-20250101-slack-18.73USD-f7fe2e63fd | 2025-01-01 | Slack | 18.73 USD | FY2025/transactions/5_expenses/Slack_2025-01-01_(ksi).md
- doc-20250104-quo-openphone-27.00USD-f84682e9d6 | 2025-01-04 | Quo (OpenPhone) | 27.00 USD | FY2025/transactions/5_expenses/Quo_(OpenPhone)_2025-01-04.md
- doc-20250105-jetbrains-USD-33316f91db | 2025-01-05 | JetBrains |  USD | FY2025/transactions/5_expenses/JetBrains_2025-01-05.md
- doc-20250117-namespro-59.81USD-cf077e661b | 2025-01-17 | Namespro | 59.81 USD | FY2025/transactions/5_expenses/Namespro_2025-01-17.md
- doc-20250125-paddle-13.44USD-fe49bf601c | 2025-01-25 | Paddle | 13.44 USD | FY2025/transactions/5_expenses/Paddle_2025-01-25.md
- doc-20250201-slack-18.73USD-8eb78c682b | 2025-02-01 | Slack | 18.73 USD | FY2025/transactions/5_expenses/Slack_2025-02-01_(ksi).md
- doc-20250204-quo-openphone-27.00USD-cf1542792d | 2025-02-04 | Quo (OpenPhone) | 27.00 USD | FY2025/transactions/5_expenses/Quo_(OpenPhone)_2025-02-04.md
- doc-20250205-jetbrains-USD-cc5e9c679c | 2025-02-05 | JetBrains |  USD | FY2025/transactions/5_expenses/JetBrains_2025-02-05.md
- doc-20250215-namespro-38.78USD-440abdf75e | 2025-02-15 | Namespro | 38.78 USD | FY2025/transactions/5_expenses/Namespro_2025-02-15.md
- doc-20250225-paddle-13.44USD-8e3f6cae77 | 2025-02-25 | Paddle | 13.44 USD | FY2025/transactions/5_expenses/Paddle_2025-02-25.md
- doc-20250301-slack-18.73USD-f86345a6e3 | 2025-03-01 | Slack | 18.73 USD | FY2025/transactions/5_expenses/Slack_2025-03-01_(ksi).md
- doc-20250304-quo-openphone-27.00USD-4a36d979ae | 2025-03-04 | Quo (OpenPhone) | 27.00 USD | FY2025/transactions/5_expenses/Quo_(OpenPhone)_2025-03-04.md
- doc-20250305-jetbrains-USD-cf040fdd53 | 2025-03-05 | JetBrains |  USD | FY2025/transactions/5_expenses/JetBrains_2025-03-05.md
- doc-20250310-namespro-89.13USD-8e7dd604ea | 2025-03-10 | Namespro | 89.13 USD | FY2025/transactions/5_expenses/Namespro_2025-03-10.md
- doc-20250325-paddle-13.44USD-8e9198072f | 2025-03-25 | Paddle | 13.44 USD | FY2025/transactions/5_expenses/Paddle_2025-03-25.md
- doc-20250401-slack-18.73USD-e63cccf48c | 2025-04-01 | Slack | 18.73 USD | FY2025/transactions/5_expenses/Slack_2025-04-01_(ksi).md
- doc-20250404-quo-openphone-29.00USD-b4f9e8672c | 2025-04-04 | Quo (OpenPhone) | 29.00 USD | FY2025/transactions/5_expenses/Quo_(OpenPhone)_2025-04-04.md
- doc-20250406-jetbrains-USD-a60d92cc24 | 2025-04-06 | JetBrains |  USD | FY2025/transactions/5_expenses/JetBrains_2025-04-06.md
- doc-20250425-paddle-13.44USD-eec2627848 | 2025-04-25 | Paddle | 13.44 USD | FY2025/transactions/5_expenses/Paddle_2025-04-25.md
- doc-20250501-slack-18.73USD-7ae5e44ffd | 2025-05-01 | Slack | 18.73 USD | FY2025/transactions/5_expenses/Slack_2025-05-01_(ksi).md
- doc-20250504-quo-openphone-29.00USD-d743d5d51e | 2025-05-04 | Quo (OpenPhone) | 29.00 USD | FY2025/transactions/5_expenses/Quo_(OpenPhone)_2025-05-04.md
- doc-20250506-jetbrains-USD-d7a4326269 | 2025-05-06 | JetBrains |  USD | FY2025/transactions/5_expenses/JetBrains_2025-05-06.md
- doc-20250512-namespro-41.02USD-8eae1295a7 | 2025-05-12 | Namespro | 41.02 USD | FY2025/transactions/5_expenses/Namespro_2025-05-12.md
- doc-20250514-namespro-20.86USD-00a169aec7 | 2025-05-14 | Namespro | 20.86 USD | FY2025/transactions/5_expenses/Namespro_2025-05-14.md
- doc-20250522-slack-2.12USD-f6549a7857 | 2025-05-22 | Slack | 2.12 USD | FY2025/transactions/5_expenses/Slack_2025-05-22_(lexibl).md
- doc-20250525-paddle-13.44USD-c8125af224 | 2025-05-25 | Paddle | 13.44 USD | FY2025/transactions/5_expenses/Paddle_2025-05-25.md
- doc-20250526-lenovo-canada-789.00USD-df8e11181a | 2025-05-26 | Lenovo Canada | 789.00 USD | FY2025/transactions/5_expenses/Lenovo_Canada_2025-05-26_Order_4648752389_Invoice_6296701127.md
- doc-20250601-slack-18.73USD-b6b7d9ee29 | 2025-06-01 | Slack | 18.73 USD | FY2025/transactions/5_expenses/Slack_2025-06-01_(ksi).md
- doc-20250604-quo-openphone-29.00USD-f6f36c013f | 2025-06-04 | Quo (OpenPhone) | 29.00 USD | FY2025/transactions/5_expenses/Quo_(OpenPhone)_2025-06-04.md
- doc-20250606-jetbrains-USD-638d92ab6f | 2025-06-06 | JetBrains |  USD | FY2025/transactions/5_expenses/JetBrains_2025-06-06.md
- doc-20250617-namespro-20.48USD-1a63811e3d | 2025-06-17 | Namespro | 20.48 USD | FY2025/transactions/5_expenses/Namespro_2025-06-17.md
- doc-20250622-slack-9.36USD-b9df82c29e | 2025-06-22 | Slack | 9.36 USD | FY2025/transactions/5_expenses/Slack_2025-06-22_(lexibl).md
- doc-20250623-namespro-79.64USD-15849d53cc | 2025-06-23 | Namespro | 79.64 USD | FY2025/transactions/5_expenses/Namespro_2025-06-23.md
- doc-20250701-slack-18.73USD-7409fb8541 | 2025-07-01 | Slack | 18.73 USD | FY2025/transactions/5_expenses/Slack_2025-07-01_(ksi).md
- doc-20250704-quo-openphone-29.00USD-4c30a54648 | 2025-07-04 | Quo (OpenPhone) | 29.00 USD | FY2025/transactions/5_expenses/Quo_(OpenPhone)_2025-07-04.md
- doc-20250706-jetbrains-USD-548bedd768 | 2025-07-06 | JetBrains |  USD | FY2025/transactions/5_expenses/JetBrains_2025-07-06.md
- doc-20250722-slack-8.75USD-c505b19540 | 2025-07-22 | Slack | 8.75 USD | FY2025/transactions/5_expenses/Slack_2025-07-22_(lexibl).md
- doc-20250730-namespro-57.07USD-6b698a2737 | 2025-07-30 | Namespro | 57.07 USD | FY2025/transactions/5_expenses/Namespro_2025-07-30.md
- doc-20250801-slack-17.50USD-48153f4a6b | 2025-08-01 | Slack | 17.50 USD | FY2025/transactions/5_expenses/Slack_2025-08-01_(ksi).md
- doc-20250804-quo-openphone-29.00USD-3cddfa994c | 2025-08-04 | Quo (OpenPhone) | 29.00 USD | FY2025/transactions/5_expenses/Quo_(OpenPhone)_2025-08-04.md
- doc-20250806-jetbrains-USD-e1c73f38b0 | 2025-08-06 | JetBrains |  USD | FY2025/transactions/5_expenses/JetBrains_2025-08-06.md
- doc-20250808-openai-150.00USD-e681054165 | 2025-08-08 | OpenAI | 150.00 USD | FY2025/transactions/5_expenses/OpenAI_2025-08-08.md
- doc-20250822-slack-8.75USD-372e4a2fbc | 2025-08-22 | Slack | 8.75 USD | FY2025/transactions/5_expenses/Slack_2025-08-22_(lexibl).md
- doc-20250901-slack-17.50USD-8549e56a3b | 2025-09-01 | Slack | 17.50 USD | FY2025/transactions/5_expenses/Slack_2025-09-01_(ksi).md
- doc-20250903-namespro-20.69USD-c5bdf1307b | 2025-09-03 | Namespro | 20.69 USD | FY2025/transactions/5_expenses/Namespro_2025-09-03.md
- doc-20250904-quo-openphone-29.00USD-e0a3b33b97 | 2025-09-04 | Quo (OpenPhone) | 29.00 USD | FY2025/transactions/5_expenses/Quo_(OpenPhone)_2025-09-04.md
- doc-20250906-jetbrains-USD-c7fa9d5408 | 2025-09-06 | JetBrains |  USD | FY2025/transactions/5_expenses/JetBrains_2025-09-06.md
- doc-20250908-openai-67.20USD-dab7750878 | 2025-09-08 | OpenAI | 67.20 USD | FY2025/transactions/5_expenses/OpenAI_2025-09-08.md
- doc-20250917-jetbrains-USD-53470dbf2c | 2025-09-17 | JetBrains |  USD | FY2025/transactions/5_expenses/JetBrains_2025-09-17.md
- doc-20250922-slack-8.75USD-bd8b049737 | 2025-09-22 | Slack | 8.75 USD | FY2025/transactions/5_expenses/Slack_2025-09-22_(lexibl).md
- doc-20251001-slack-17.50USD-dff54e3b75 | 2025-10-01 | Slack | 17.50 USD | FY2025/transactions/5_expenses/Slack_2025-10-01_(ksi).md
- doc-20251004-quo-openphone-29.00USD-30e50abbfe | 2025-10-04 | Quo (OpenPhone) | 29.00 USD | FY2025/transactions/5_expenses/Quo_(OpenPhone)_2025-10-04.md
- doc-20251006-jetbrains-USD-c626f3b4d9 | 2025-10-06 | JetBrains |  USD | FY2025/transactions/5_expenses/JetBrains_2025-10-06.md
- doc-20251008-openai-60.00USD-37c7724a75 | 2025-10-08 | OpenAI | 60.00 USD | FY2025/transactions/5_expenses/OpenAI_2025-10-08.md
- doc-20251017-jetbrains-USD-62ad817511 | 2025-10-17 | JetBrains |  USD | FY2025/transactions/5_expenses/JetBrains_2025-10-17.md
- doc-20251022-slack-8.75USD-9d213b4642 | 2025-10-22 | Slack | 8.75 USD | FY2025/transactions/5_expenses/Slack_2025-10-22_(lexibl).md
- doc-20251025-quo-openphone-19.50USD-0af77dbb27 | 2025-10-25 | Quo (OpenPhone) | 19.50 USD | FY2025/transactions/5_expenses/Quo_(OpenPhone)_2025-10-25.md
- doc-20251101-slack-18.73USD-ac6e43fa7a | 2025-11-01 | Slack | 18.73 USD | FY2025/transactions/5_expenses/Slack_2025-11-01_(ksi).md
- doc-20251104-quo-openphone-30.89USD-93ead943db | 2025-11-04 | Quo (OpenPhone) | 30.89 USD | FY2025/transactions/5_expenses/Quo_(OpenPhone)_2025-11-04.md
- doc-20251105-jetbrains-USD-a49dcd97a8 | 2025-11-05 | JetBrains |  USD | FY2025/transactions/5_expenses/JetBrains_2025-11-05.md
- doc-20251108-openai-60.00USD-ed285cde91 | 2025-11-08 | OpenAI | 60.00 USD | FY2025/transactions/5_expenses/OpenAI_2025-11-08.md
- doc-20251116-jetbrains-USD-a70ebd9a66 | 2025-11-16 | JetBrains |  USD | FY2025/transactions/5_expenses/JetBrains_2025-11-16.md
- doc-20251122-slack-8.75USD-124baeda4f | 2025-11-22 | Slack | 8.75 USD | FY2025/transactions/5_expenses/Slack_2025-11-22_(lexibl).md
- doc-20251201-slack-18.73USD-e52b567d38 | 2025-12-01 | Slack | 18.73 USD | FY2025/transactions/5_expenses/Slack_2025-12-01_(ksi).md
- doc-20251204-quo-openphone-30.50USD-d96e7424cd | 2025-12-04 | Quo (OpenPhone) | 30.50 USD | FY2025/transactions/5_expenses/Quo_(OpenPhone)_2025-12-04.md
- doc-20251205-jetbrains-USD-440709fe72 | 2025-12-05 | JetBrains |  USD | FY2025/transactions/5_expenses/JetBrains_2025-12-05.md
- doc-20251208-openai-67.20USD-c840d405d2 | 2025-12-08 | OpenAI | 67.20 USD | FY2025/transactions/5_expenses/OpenAI_2025-12-08.md
- doc-20251216-jetbrains-USD-63cde5f535 | 2025-12-16 | JetBrains |  USD | FY2025/transactions/5_expenses/JetBrains_2025-12-16.md
- doc-20251222-slack-8.75USD-646d281f20 | 2025-12-22 | Slack | 8.75 USD | FY2025/transactions/5_expenses/Slack_2025-12-22_(lexibl).md
