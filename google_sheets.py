import gspread 
from gspread.models import Cell

def push_to_sheets(data,sheet_name):
    # print(data)
    gc = gspread.service_account("./config/sheets_config.json")
    wks = gc.open("Emotions").worksheet(sheet_name)
    cols = wks.col_values(1)
    # rows = wks.row_values(1)
    c = len(cols)
    # row_number = "A{}".format(c+1)
    row_no =c+1
    no_cols = len(data[0])
    no_rows = len(data)
    
    cells = []
    # for i, val in enumerate(cell_values):  #gives us a tuple of an index and value
    # cell_list[i].value = val
    cell_list = wks.range("A{}:K{}".format(row_no,row_no))
  
    for i in range(no_rows):
        cell_list[i].values = data[i]
        # wks.update_cells(data[i])
    # print(rows)
    # wks.update(row_number, data)
    # wks.update_cell(2, 1, '2020-12-12')
    wks.update_cells(cell_list)

def push_to_sheets2(spreadsheet_name,csv_file):
    # from oauth2client.service_account import ServiceAccountCredentials

    # scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
    #         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

    # credentials = ServiceAccountCredentials.from_json_keyfile_name('./config/sheets_config.json', scope)
    # client = gspread.authorize(credentials)
    gc = gspread.service_account("./config/sheets_config.json")
    # wks = gc.open("Emotions").worksheet("Emotion_Data_Backend")
    spreadsheet = gc.open(spreadsheet_name)

    with open(csv_file, 'r') as file_obj:
        content = file_obj.read()
        gc.import_csv(spreadsheet.id, data=content)
