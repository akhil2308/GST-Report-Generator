import gspread


GOOGLE_CREDENTIALS_PATH    ='./credentials/client_secret.json',
GOOGLE_AUTHORIZED_USER_PATH='./credentials/authorized_user.json'

gc = gspread.oauth(credentials_filename=GOOGLE_CREDENTIALS_PATH,authorized_user_filename=GOOGLE_AUTHORIZED_USER_PATH)
        
GSHEET_DETAILS_LIST=[
    {
    "title"       :"Money Stream Financial Services IMF Pvt Ltd 1",
    "sheet_id"    :'1v2iQQex_vQpqORToi2kLO44VMO7zv3KG2IqIapS0Agw',
    "sheet_name"  :"Sheet2"
    },{
    "title"       :"Money Stream Financial Services IMF Pvt Ltd 2",
    "sheet_id"    :'1dY25SsFDWsx83vEu9DiV4DFPOYk95guh12N04Jx6VvU',
    "sheet_name"  :"Sales FY2022-2023"
    },{
    "title"       :"BALAJI ELECTRONICS",
    "sheet_id"    :'1EIk0_Suz67VeGrpwRlFw_T-u05NDR10LDZe4zqUbeEk',
    "sheet_name"  :"Sales FY2021-2022"
    },
]

SAVE_FOLDER_PATH = './data/*'

# # logging
# LOGGING = {
# 	'version': 1,
# 	'disable_existing_loggers': False,
# 	'formatters': {
# 		'simple': {
# 			'format': '[%(asctime)s] %(levelname)s %(message)s',
# 		},
# 		'verbose': {
# 			'format': '[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s',
# 		},
# 	},
# 	'handlers': {
# 		'console': {
# 			'class': 'logging.StreamHandler',
# 			'level': 'INFO',
# 			'formatter': 'verbose'
# 		},
# 	},
# 	'loggers': {
# 		'': {
# 			'handlers': ['console'],
# 			'level': 'INFO',
# 			'propagate': True,
# 		},
# 	},
# }
# import logging
# import logging.config

# logging.config.dictConfig(LOGGING)

#DATE_FORMATS_LIST = ["%d-%b-%Y :: 3-Apr-2022", "%d/%m/%Y :: 4/7/2022", "%d-%m-%y :: 4-7-22", "%Y-%m-%d :: 2022-01-07"]

# DATE_FORMAT_MAPER = ['%d-%b-%Y','%d/%m/%Y',"%d-%m-%y","%Y-%m-%d"]

DATA_COLUMN_EXCEL_CSV_MAP={
    "GSTIN/UIN of Recipient": 'GSTIN OF BUYER',
    "Receiver Name"         : 'Name of the Buyer',
    "Invoice Number"        : 'Invoice No.',
    "Invoice date"          : 'Date',
    "Invoice Value"         : 'Invoice Value',
    "Place Of Supply"       : 'Place of the Buyer',
    "Rate"                  : 'TOTAL RATE',
    "Taxable Value"         : 'Taxable Value'
}

DEFAULT_DATA_CSV={
    "Reverse Charge"            : 'N',
    "Applicable % of Tax Rate"  : "",
    "Invoice Type"              : "Regular B2B",
    "E-Commerce GSTIN"          : "",
    "Cess Amount"               : 0
}