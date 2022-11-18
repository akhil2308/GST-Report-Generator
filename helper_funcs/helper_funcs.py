from dateutil import parser
import os
import glob
from settings.settings import GOOGLE_CREDENTIALS_PATH, GOOGLE_AUTHORIZED_USER_PATH, gc




def treat_date_v2(s_date, format='date'):
    try:
        if format == 'date': return parser.parse(s_date).strftime("%d-%b-%Y")
        if format == 'time': return parser.parse(s_date).strftime("%H:%M:%S")
        if format == 'datetime': return parser.parse(s_date).strftime('%Y-%m-%d %H:%M:%S%z')
        
    except:
        return None
    
def open_gsheet(sheet_id,sheet_name):
    try:
        sh             = gc.open_by_key(sheet_id)
        wks            = sh.worksheet(sheet_name)
        sheet_modules  = wks.get_all_values()
        print("Successfully accessed gsheet")
        return sh.title, sheet_modules
    except Exception as e:
        print(e)
        exit()
        
def get_gsheet(title,gsheets):
    for sheet in gsheets:
        if title == sheet['title']:
            return sheet
    
def empty_folder(folder_path):
    files = glob.glob(folder_path)
    for f in files:
        os.remove(f)
    print("Folder has been emptied")