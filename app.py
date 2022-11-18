
from settings.settings import *
import sys
import pathlib
import pandas as pd
import numpy as  np
from InquirerPy import inquirer

from parsers.parser import B2BB2CParser
from helper_funcs.helper_funcs import get_gsheet, open_gsheet, empty_folder

import logging
logger = logging.getLogger(__name__)

sys.path.insert(0, str(pathlib.Path(__file__).parent))


if __name__=='__main__':
    # try:
        # select a gsheet
        sheet_title = inquirer.select(message = "Select a google sheet to parse:",
                                    choices = [sheet['title'] for sheet in GSHEET_DETAILS_LIST],
                                    ).execute()
        
        sheet                       = get_gsheet(sheet_title,GSHEET_DETAILS_LIST)
        sheet_title, sheet_modules  = open_gsheet(sheet['sheet_id'],sheet['sheet_name'])
        
        # creating parser class obj 
        obj             = B2BB2CParser(sheet_title, sheet_modules)
        df              = obj.parse()
        months_list     = obj.get_df_month(df)
        
        # select (Monthly or Quarterly)
        action = inquirer.select(message="Select an action:", choices=["Monthly","Quarterly"],).execute()
        
        # select months ([Aug,Sep,Oct,...])
        if action == "Quarterly":
            result   = inquirer.select(message ="Select dates:",  choices =months_list, multiselect =True,).execute()
        else:
            result   = inquirer.select(message ="Select a date:", choices =months_list).execute()
            
        # converting single values to list
        if action == "Monthly":
            result = [result]
            
        df                 = obj.group_df_month(df,months=result)
        b2b_df,b2c_df      = obj.sort_df(df)
        
        b2b_result_df      = obj.make_b2b_df(b2b_df)
        
        #empting the folder
        empty_folder(SAVE_FOLDER_PATH)
        
        if not b2c_df.empty:
            b2c_result_df      = obj.make_b2c_df(b2c_df)
            
            b2c_result_df.to_csv("data/B2C {}-({}).csv".format(sheet_title,','.join(result)),index=False)
            logger.info("The data is saved in file:: B2C {}-({}).csv".format(sheet_title,','.join(result)))
            
            
        b2b_result_df.to_csv("data/B2B {}-({}).csv".format(sheet_title,','.join(result)),index=False)
            
        logger.info("The data is saved in file:: B2B {}-({}).csv".format(sheet_title,','.join(result)))
    
    # except Exception as e:
    #     logger.error(e)
 
