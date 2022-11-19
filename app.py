
from settings.settings import *
import sys
import pathlib
import pandas as pd
import numpy as  np
from InquirerPy import inquirer
from datetime import datetime
from parsers.parser import B2BB2CParser
from helper_funcs.helper_funcs import get_gsheet, open_gsheet, empty_folder
from rich import print as rprint

# import logging
# logger = logging.getLogger(__name__)

sys.path.insert(0, str(pathlib.Path(__file__).parent))


if __name__=='__main__':
    try:
        # select a gsheet
        sheet_title = inquirer.select(message = "Select a google sheet to parse:",
                                    choices = [sheet['title'] for sheet in GSHEET_DETAILS_LIST],
                                    ).execute()
        
        sheet                       = get_gsheet(sheet_title,GSHEET_DETAILS_LIST)
        sheet_title, sheet_modules  = open_gsheet(sheet['sheet_id'],sheet['sheet_name'])
        
        # date_format = inquirer.select(message = "Select the date formate of the gsheet:",
        #                             choices = DATE_FORMATS_LIST,
        #                             ).execute()
        # date_format = DATE_FORMAT_MAPER[DATE_FORMATS_LIST.index(date_format)]
        
        # creating parser class obj 
        obj             = B2BB2CParser(sheet_title, sheet_modules)
        df              = obj.parse()
        months_list     = obj.get_unique_month(df)
        # sorting dates
        months_list.sort(key=lambda date: datetime.strptime(date, '%B-%Y'))
        
        # select (Monthly or Quarterly)
        action = inquirer.select(message="Select an action:", choices=["Monthly","Quarterly"],).execute()
        
        # select months ([Aug,Sep,Oct,...])
        if action == "Quarterly":
            result   = inquirer.select(message ="Select dates:",  choices =months_list
                                       , multiselect =True,).execute()
        else:
            result   = inquirer.select(message ="Select a date:", choices =months_list
                                       ).execute()
            
        # converting single values to list
        if action == "Monthly":
            result = [result]
            
        # get df with user requested months
        df                 = obj.group_df_month(df,months=result)
        # separating  df into two dfs
        b2b_df,b2c_df      = obj.separate_df(df)
        # making b2b df
        b2b_result_df      = obj.make_b2b_df(b2b_df)
        # making sac df
        sac_result_df      = obj.make_sac_df(df)
        
        # empting the folder
        empty_folder(SAVE_FOLDER_PATH)

        if not b2c_df.empty:
            b2c_result_df      = obj.make_b2c_df(b2c_df)
            
            b2c_result_df.to_csv("data/B2C {}-({}).csv".format(sheet_title,','.join(result)),index=False)
            rprint("The data is saved in file:: [bold magenta]B2C {}-({}).csv[/bold magenta]".format(sheet_title,','.join(result)))
            
        # saving the df into csv files   
        b2b_result_df.to_csv("data/B2B {}-({}).csv".format(sheet_title,','.join(result)),index=False)
        sac_result_df.to_csv("data/SAC {}-({}).csv".format(sheet_title,','.join(result)),index=False)

        rprint("The data is saved in file:: [bold magenta]B2B {}-({}).csv[/bold magenta]".format(sheet_title,','.join(result)))
        rprint("The data is saved in file:: [bold magenta]SAC {}-({}).csv[/bold magenta]".format(sheet_title,','.join(result)))
    
    except Exception as e:
        rprint("[red]ERROR:: "+str(e))
 
