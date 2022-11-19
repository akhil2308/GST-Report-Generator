import pandas as pd
import numpy as  np
import calendar
from settings.settings import *
from helper_funcs.helper_funcs import treat_date_v2
import re

class B2BB2CParser():
	
	def __init__(self,sheet_title, sheet_modules):
		self.sheet_title 	= sheet_title
		self.sheet_modules  = sheet_modules
		
		self.b2b_df_col_names =["GSTIN/UIN of Recipient","Receiver Name","Invoice Number","Invoice date",
								"Invoice Value","Place Of Supply","Reverse Charge","Applicable % of Tax Rate",
								"Invoice Type","E-Commerce GSTIN","Rate","Taxable Value","Cess Amount"]
		
		self.required_cols 	= [	'Invoice No.', 'Date', 'Name of the Buyer',
								'GSTIN OF BUYER', 'Place of the Buyer','SAC Code','Taxable Value',
								'IGST RATE', 'IGST TAX', 'CGST RATE', 'CGST TAX', 'SGST RATE', 'SGST TAX',
								'Invoice Value']
	
	def make_b2b_df(self,df):
		final_b2b_df = pd.DataFrame(columns =self.b2b_df_col_names)
		# creating a 
		for key, value in DATA_COLUMN_EXCEL_CSV_MAP.items():
				final_b2b_df[key] = df[value]
		
		for key, value in DEFAULT_DATA_CSV.items():
				final_b2b_df[key] = value
				
		return final_b2b_df


	def make_b2c_df(self,df):
		final_b2c_df 	= df[['GSTIN OF BUYER', 'Place of the Buyer', 'TOTAL RATE', 'TOTAL TAX', 'Taxable Value', 'Invoice Value']]
		grouped_df 		= final_b2c_df.groupby(['Place of the Buyer','TOTAL RATE'])
		result=[]
		for i,group in grouped_df:
				total  	= group[['TOTAL TAX','Taxable Value', 'Invoice Value']].sum(axis=0)
				total   = total.to_dict()
				result.append({ 'Place of the Buyer':i[0],'TOTAL RATE':i[1], 'TOTAL TAX':total['TOTAL TAX'],
								'TOTAL Taxable Value':total['Taxable Value'], 'TOTAL Invoice Value':total['Invoice Value']})

		return pd.DataFrame(result)


	def parse(self):
		try:
			df = pd.DataFrame(self.sheet_modules[4:], columns=self.sheet_modules[3])
			df = df.replace(r'^\s*$', np.nan, regex=True)
			df = df.replace({None :np.nan})
			
			# get index of the start and end column
			end_index   = df.columns.get_loc('Invoice Value')
			start_index = df.columns.get_loc('Sl.No')

			#slicing the df based on the start and end index
			df  		= df.iloc[:,range(start_index,end_index+1)]
			
			col = list(df.columns)
			col[col.index('Taxable Value'):col.index('Invoice Value')+1]   = [
										'Taxable Value','IGST RATE', 'IGST TAX', 'CGST RATE',
										'CGST TAX', 'SGST RATE', 'SGST TAX','Invoice Value']
			df.columns 	= col
   
			# using only required columns from df
			df			=	df[self.required_cols]

			# replacing NA with the coresponding values
			df.fillna({'Taxable Value':0.0, 'IGST RATE':'0%', 'IGST TAX':0.0, 'CGST RATE':'0%', 'CGST TAX':0.0,
						'SGST RATE':'0%', 'SGST TAX':0.0, 'Invoice Value' :0.0}, inplace=True)
			
			# treating date
			df['Date']       = df["Date"].map(lambda x: treat_date_v2(x))   
			df.dropna(subset =['Date'], axis=0, inplace=True)
			
			df['SAC Code']          = df['SAC Code'].map(lambda x: str(x)[:4])

			# converting string to float
			persentage_col      = ['IGST RATE','CGST RATE','SGST RATE']
			number_col          = ['Taxable Value', 'IGST TAX', 'CGST TAX', 'SGST TAX','Invoice Value']
			# string number to float
			df[number_col]      = df[number_col].apply(lambda x: x.str.replace(',', ''))
			df[number_col]      = df[number_col].apply(pd.to_numeric, errors='coerce')

			# string persentage to float
			df[persentage_col]  = df[persentage_col].apply(lambda x: x.str.rstrip('%'))
			df[persentage_col]  = df[persentage_col].astype('float', errors='ignore') 
			
			# adding multiple columns to form one column
			tax_col     		= ['IGST TAX', 'CGST TAX', 'SGST TAX']
			rate_clo    		= ['IGST RATE','CGST RATE','SGST RATE']
			df['TOTAL TAX']    	= df[tax_col].sum(axis=1)
			df['TOTAL RATE']   	= df[rate_clo].sum(axis=1)
			
			# creating month column from date 
			df['Months']  = df['Date'].apply(lambda x: treat_date_v2(x,format='month_year')) 
			
			return df
		except Exception as e:
			print(e)
			raise
			
	def make_sac_df(self,df):
		df 		= df [['SAC Code','TOTAL TAX','Taxable Value','Invoice Value']]
		sac_df 	= df.groupby(['SAC Code'])[['TOTAL TAX','Taxable Value','Invoice Value']].apply(sum)
		return sac_df

			
	def separate_df(self,df):
		# making two dataframes based on the condition
		b2c_df = df.loc[df['GSTIN OF BUYER']=='B2C']
		b2b_df = df.loc[df['GSTIN OF BUYER']!='B2C']

		return b2b_df,b2c_df

	def get_unique_month(self,df):
		return list(df['Months'].unique())

	def group_df_month(self,df,months):
		grouped_df  = df.groupby(['Months'])
		new_df 		= pd.concat([grouped_df.get_group(group) for group in df['Months'].unique() if group in months ])  

		return  new_df
