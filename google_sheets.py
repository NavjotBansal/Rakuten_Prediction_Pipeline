import gspread

def push_to_sheets(data,sheet_name):
    
    gc = gspread.service_account("./config/sheets_config.json")
    wks = gc.open("Emotions").worksheet(sheet_name)
    cols = wks.col_values(1)
    rows = wks.row_values(1)
    c = len(cols)
    k = "A{}".format(c+1)
    print(rows)
    #wks.update(k, data)