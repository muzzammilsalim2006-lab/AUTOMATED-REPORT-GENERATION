# ==============================
# 📌 AUTOMATED REPORT GENERATOR
# ==============================

# Import required libraries
import pandas as pd
import matplotlib.pyplot as plt
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

# ==============================
# 📌 STEP 1: LOAD DATA (CSV / EXCEL)
# ==============================

file_type = input("Enter file type (csv/excel): ").strip().lower()

if file_type == "csv":
    data = pd.read_csv("sales_data.csv")
elif file_type == "excel":
    data = pd.read_excel("sales_data.xlsx", engine="openpyxl")
else:
    print("Invalid file type!")
    exit()

# ==============================
# 📌 STEP 2: DATA ANALYSIS
# ==============================

# Total Revenue
total_revenue = data["Total Sales"].sum()

# Best Selling Product (by Units Sold)
best_product = data.groupby("Product")["Units Sold"].sum().idxmax()

# Top Region (by Total Sales)
top_region = data.groupby("Region")["Total Sales"].sum().idxmax()

# Average Sales
average_sales = data["Total Sales"].mean()

# ==============================
# 📌 STEP 3: CREATE CHART
# ==============================

# Sales by Product Chart
product_sales = data.groupby("Product")["Total Sales"].sum()

plt.figure()
product_sales.plot(kind='bar')
plt.title("Sales by Product")
plt.xlabel("Product")
plt.ylabel("Total Sales")

# Save chart as image
chart_path = "sales_chart.png"
plt.savefig(chart_path)
plt.close()

# ==============================
# 📌 STEP 4: GENERATE PDF REPORT
# ==============================

# Create PDF document
doc = SimpleDocTemplate("Sales_Report.pdf")
doc = SimpleDocTemplate("Sales_Report_v2.pdf")

# Styles for formatting
styles = getSampleStyleSheet()

# Content list
content = []

# ==============================
# 📌 HEADING
# ==============================

content.append(Paragraph("Sales Analysis Report", styles['Title']))
content.append(Spacer(1, 20))

# ==============================
# 📌 SUMMARY (BOLD TEXT)
# ==============================

content.append(Paragraph(f"<b>Total Revenue:</b> ₹{total_revenue}", styles['Normal']))
content.append(Spacer(1, 10))

content.append(Paragraph(f"<b>Best Selling Product:</b> {best_product}", styles['Normal']))
content.append(Spacer(1, 10))

content.append(Paragraph(f"<b>Top Region:</b> {top_region}", styles['Normal']))
content.append(Spacer(1, 10))

content.append(Paragraph(f"<b>Average Sales:</b> ₹{average_sales:.2f}", styles['Normal']))
content.append(Spacer(1, 20))

# ==============================
# 📌 TABLE (DATA)
# ==============================

# Convert dataframe to table format
table_data = [data.columns.tolist()] + data.values.tolist()

# Create table
table = Table(table_data)

# Add styling
table.setStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold')
])

content.append(Paragraph("<b>Sales Data Table</b>", styles['Heading2']))
content.append(Spacer(1, 10))
content.append(table)
content.append(Spacer(1, 20))

# ==============================
# 📌 ADD CHART TO PDF
# ==============================

content.append(Paragraph("<b>Sales Chart</b>", styles['Heading2']))
content.append(Spacer(1, 10))

# Add chart image
content.append(Image(chart_path, width=400, height=250))

# ==============================
# 📌 BUILD PDF
# ==============================

doc.build(content)

print("✅ PDF Report Generated Successfully!")