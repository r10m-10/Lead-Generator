from openpyxl import Workbook

def convert_to_excel(leads):
    print("----------GENERATING EXCEL FILE----------")
    wb = Workbook()
    ws = wb.active

    ws.title = "Leads"
    ws.append(["Name", "Phone Number", "Website", "Rating & Reviews"])

    for i in leads:
        row = list(i.values())
        ws.append(row)
    
    wb.save("leads.xlsx")
    print('\n----------EXCEL FILE SAVED SUCESSFULLY AS "leads.xlsx"----------')