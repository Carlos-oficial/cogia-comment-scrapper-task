from openpyxl import load_workbook
import json

wb = load_workbook('../task/link_list.xlsx')
print(wb)
sheets = wb.sheetnames
print(sheets)
link_dict = {}
for sheet in sheets:
    link_dict[sheet] = []

    for row in wb[sheet].rows:
        link_dict[sheet].append((row[0].value))
    del(link_dict[sheet][0])
with open('output.json', "w") as file:
    file.write(json.dumps((link_dict), sort_keys=True, indent=2))
