
import streamlit as st
import pandas as pd
from io import BytesIO
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.table import Table, TableStyleInfo

st.title("GSTR-2B vs GSTR-2A Merger Tool")

gstr2b_file = st.file_uploader("Upload GSTR-2B Excel File", type="xlsx")
gstr2a_file = st.file_uploader("Upload GSTR-2A Excel File", type="xlsx")

def load_excel(file, columns, skiprows=6):
    df = pd.read_excel(file, sheet_name="B2B", header=None, skiprows=skiprows)
    df.columns = columns
    return df

def prepare_output_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Merged Data")
        wb = writer.book
        ws = writer.sheets["Merged Data"]
        last_col = get_column_letter(df.shape[1])
        table = Table(displayName="MergedTable", ref=f"A1:{last_col}{df.shape[0]+1}")
        style = TableStyleInfo(name="TableStyleMedium9", showRowStripes=True, showColumnStripes=True)
        table.tableStyleInfo = style
        ws.add_table(table)
        for col in ws.columns:
            max_len = max(len(str(cell.value)) if cell.value else 0 for cell in col)
            ws.column_dimensions[col[0].column_letter].width = max_len + 2
    output.seek(0)
    return output

if gstr2b_file and gstr2a_file:
    with st.spinner("Processing..."):

        gstr2b_columns = [
            "GSTIN of supplier", "Trade/Legal name", "Invoice number", "Invoice type",
            "Invoice Date", "Invoice Value(₹)", "Place of supply", "Supply Attract Reverse Charge",
            "Rate(%)", "Taxable Value (₹)", "Integrated Tax(₹)", "Central Tax(₹)",
            "State/UT Tax(₹)", "Cess(₹)", "GSTR-1/5 Period", "GSTR-1/5 Filing Date",
            "ITC Availability", "Reason", "Applicable % of Tax Rate", "Source", "IRN",
            "IRN Date", "Period"
        ]

        gstr2a_columns = [
            "GSTIN of supplier", "Trade/Legal name of the Supplier", "Invoice number", "Invoice type",
            "Invoice Date", "Invoice Value (₹)", "Place of supply", "Supply Attract Reverse Charge",
            "Rate (%)", "Taxable Value (₹)", "Integrated Tax  (₹)", "Central Tax (₹)",
            "State/UT tax (₹)", "Cess  (₹)", "GSTR-1/5 Filing Status", "GSTR-1/5 Filing Date",
            "GSTR-1/5 Filing Period", "GSTR-3B Filing Status", "Amendment made, if any",
            "Tax Period in which Amended", "Effective date of cancellation", "Period"
        ]

        df2b = load_excel(gstr2b_file, gstr2b_columns)
        df2a = load_excel(gstr2a_file, gstr2a_columns)

        df2a.rename(columns={
            "Trade/Legal name of the Supplier": "Trade/Legal name",
            "Rate (%)": "Rate(%)",
            "Taxable Value (₹)": "Taxable Value (₹)",
            "Integrated Tax  (₹)": "Integrated Tax(₹)",
            "Central Tax (₹)": "Central Tax(₹)",
            "State/UT tax (₹)": "State/UT Tax(₹)",
            "Cess  (₹)": "Cess(₹)"
        }, inplace=True)

        merged = pd.merge(
            df2b,
            df2a[["Invoice number", "GSTIN of supplier", "Rate(%)", "Taxable Value (₹)",
                  "Integrated Tax(₹)", "Central Tax(₹)", "State/UT Tax(₹)", "Cess(₹)"]],
            on=["Invoice number", "GSTIN of supplier"],
            how="left"
        )

        to_drop = [col for col in merged.columns if col.endswith("_x")]
        merged.drop(columns=to_drop, inplace=True)

        insert_cols = [col for col in merged.columns if col.endswith("_y")]
        pos = merged.columns.get_loc("Supply Attract Reverse Charge") + 1
        cols = merged.columns.tolist()
        for col in reversed(insert_cols):
            cols.remove(col)
            cols.insert(pos, col)
        merged = merged[cols]

        excel_bytes = prepare_output_excel(merged)

        st.success("Merge completed successfully!")
        st.download_button("Download Merged Excel", data=excel_bytes,
                           file_name="merged_gstr_data.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
