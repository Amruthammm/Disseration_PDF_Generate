import os
import requests
from fpdf import FPDF

# Set your ServiceNow instance, username, and password
instance = "dev203623"
username = "admin"
password = "TmCESy74k!b%"

url = f"https://{instance}.service-now.com/api/now/table/incident"
auth = (username, password)

response = requests.get(url, auth=auth)
data = response.json()

# Check if the request was successful
if response.status_code != 200:
    print("Error:", response.status_code, response.text)
    exit()

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Incident Report', 0, 1, 'C')

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def create_pdf(incident, directory):
    pdf = PDF()
    pdf.add_page()
    
    # Title Page
    pdf.set_font("Arial", size=16)
    pdf.cell(0, 10, txt=f"Incident Report: {incident['number']}", ln=True, align='C')
    
    # Introduction
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt="This document provides a detailed report of the incident including the problem description and the resolution provided.")
    
    # Incident Details Section
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, txt="Incident Details", ln=True, align='L')
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, txt=f"Incident Number: {incident['number']}", ln=True, align='L')
    # pdf.cell(200, 10, txt=f"Reported By: {incident['reported_by']['display_value']}", ln=True, align='L')
    pdf.cell(0, 10, txt=f"Date: {incident['opened_at']}", ln=True, align='L')        
    pdf.cell(0, 10, txt=f"Description: {incident['description'].encode('latin-1', 'replace').decode('latin-1')}", ln=True, align='L')
    pdf.cell(0, 10, txt=f"Short_Description: {incident['short_description'].encode('latin-1', 'replace').decode('latin-1')}", ln=True, align='L')       
    pdf.cell(0, 10, txt=f"Category: {incident['category'].encode('latin-1', 'replace').decode('latin-1')}", ln=True, align='L')    
    pdf.cell(0, 10, txt=f"Resolution: {incident['close_notes'].encode('latin-1', 'replace').decode('latin-1')}", ln=True, align='L')
    pdf.cell(0, 10, txt=f"Status: {incident['close_code'].encode('latin-1', 'replace').decode('latin-1')}", ln=True, align='L')


 
    # # Problem Description
    # pdf.set_font("Arial", 'B', 12)
    # pdf.cell(0, 10, txt="Problem Description", ln=True, align='L')
    # pdf.set_font("Arial", size=12)
   
    
    # # Resolution
    # pdf.set_font("Arial", 'B', 12)
    # pdf.cell(0, 10, txt="Resolution", ln=True, align='L')
    # pdf.set_font("Arial", size=12)
    
    
    # # Conclusion
    # pdf.set_font("Arial", 'B', 12)
    # pdf.cell(0, 10, txt="Conclusion", ln=True, align='L')
    # pdf.set_font("Arial", size=12)
    # pdf.cell(0, 10, txt="Incident resolved successfully.", ln=True, align='L')

    pdf_file_path = os.path.join(directory, f"{incident['number']}.pdf")
    pdf.output(pdf_file_path)

# Define the directory to save PDFs
pdf_directory = 'incident_pdfs'

# Create directory if it doesn't exist
if not os.path.exists(pdf_directory):
    os.makedirs(pdf_directory)

# Generate PDFs for each incident
for incident in data["result"]:
    create_pdf(incident, pdf_directory)

print("PDFs created successfully")
