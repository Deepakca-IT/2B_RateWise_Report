# GSTR-2B Rate Wise Report

A Streamlit app that adds rate-wise values from GSTR-2A to GSTR-2B invoices and produces an Excel report.

## What it does
- Reads the **B2B** sheet of one GSTR-2B file and one or more GSTR-2A files
- Matches rows on supplier GSTIN and invoice number
- Adds the rate, taxable value, IGST, CGST, SGST/UTGST and cess from GSTR-2A
- Shows the taxable value before and after matching

## How to use
1. Upload the GSTR-2B Excel file (`.xlsx`).
2. Upload the GSTR-2A Excel file(s) (`.xlsx`).
3. Click **Reconcile Now**.
4. Compare the two taxable value totals.
5. Download the merged Excel file.

The GSTIN in the first GSTR-2A file must be authorised for use.

## Run on your computer
```
pip install -r requirements.txt
streamlit run gst_merge_app.py
```

## Limits
- Covers the B2B section only; amendments, credit notes and imports are not covered.
- Expects the column layout coded in the app. A changed portal format may need an update.
- Matching is exact, so differently written invoice numbers will not match.
- Unmatched GSTR-2B invoices have blank rate-wise values.
- An invoice with several rates appears on several rows.

Review the output before using it for a return. Do not upload client data to this repository.
