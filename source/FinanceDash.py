__author__ = "Radek Reznicek - 747 Developments"
__copyright__ = "Copyright 2020"
__version__ = "1.1"
__email__ = "747developments@gmail.com"

################################################################################
## Import libraries
################################################################################ 
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
from dash.dependencies import Input, Output
import time
from datetime import datetime as dt, timedelta
import webbrowser #for opening web page automatically
import dev_747_styles, dev_747_DashDatatableFunc, dev_747_DashGraphFunc
import FinanceDashFunctions, FinanceDashConfig
import shutil

################################################################################
## INIT DATA
################################################################################ 
DATA_SOURCE = FinanceDashConfig.DATA_SOURCE
INITIAL_DATE = FinanceDashConfig.INITIAL_DATE
YOUR_NAME = FinanceDashConfig.YOUR_NAME
THEME_DARK = FinanceDashConfig.THEME_DARK
EXCHANGE_RATES = FinanceDashConfig.EXCHANGE_RATES

###############################################################################    
#################### Data processing and preparation part #####################
###############################################################################     
DATE_FORMAT = '%Y-%m-%d'
try:
    if(THEME_DARK):
        shutil.copyfile('StyleSheets/StyleSheetDark.css', 'assets/StyleSheet.css')
    else:
        shutil.copyfile('StyleSheets/StyleSheetLight.css', 'assets/StyleSheet.css')

except Exception as ex:
    print('Unable to copy stylesheet file: %s' % (ex))
### Actual UTC offset in hours
UTC_OFFSET_HOURS = int(time.localtime().tm_gmtoff/3600) 
### Use currency where exchange Rate is 1.0 as my main currency
MainCurrency = list(EXCHANGE_RATES.keys())[list(EXCHANGE_RATES.values()).index(1.0)]
InitialDateList = str.split(INITIAL_DATE,'-')
InitialDateList = [int(i) for i in InitialDateList]
actualYear = dt.today().year

try:
    
    if('XLS' in DATA_SOURCE):
        InitialAccounts = pd.read_excel('FinanceData/_AllFinanceData.xlsx', sheet_name='Initial')
        ExpensesDf = pd.read_excel('FinanceData/_AllFinanceData.xlsx', sheet_name='Expenses')
        IncomesDf = pd.read_excel('FinanceData/_AllFinanceData.xlsx', sheet_name='Incomes')
        TransfersDf = pd.read_excel('FinanceData/_AllFinanceData.xlsx', sheet_name='Transfers')
    
    else:
        InitialAccounts = pd.read_csv("FinanceData/_Initial.csv", sep=',')
        ExpensesDf = pd.read_csv("FinanceData/_Expenses.csv", sep=',')
        IncomesDf = pd.read_csv("FinanceData/_Incomes.csv", sep=',')
        TransfersDf = pd.read_csv("FinanceData/_Transfers.csv", sep=',')           
    
except Exception as ex:
    print ("Exception happened during data reading: " % (ex))

initialTotalBalance = 0
for index, row in InitialAccounts.iterrows():
    if(row['Currency'] in EXCHANGE_RATES):
        initialTotalBalance += row['Initial Balance']*EXCHANGE_RATES[row['Currency']]
    else:
        initialTotalBalance += row['Initial Balance']
    
# add Initial balance to beginning date where statistics starts
initialLine = pd.DataFrame({'Transaction': initialTotalBalance, 'Account': '', 'Category': 'Initial Balance', 'Date': INITIAL_DATE, 'Rate': '1', 'Comment': 'Initial balance'}, index=[0])

# merge together incomes , expenses and initial balance 
mergeExpInc = [initialLine, IncomesDf, ExpensesDf]
# concatenate these tables 
ExpIncProgressDf = pd.concat(mergeExpInc, ignore_index=True, sort=False)
# fill n/a values in Rate column with 1
values = {'Rate': 1}
ExpIncProgressDf.fillna(value=values, inplace=True)
# read date and sort table based on date
ExpIncProgressDf['Date'] = pd.to_datetime(ExpIncProgressDf['Date'], format=DATE_FORMAT)
ExpIncProgressDf = ExpIncProgressDf.sort_values('Date')
ExpIncProgressDf.reset_index(inplace=True)

# do cumulative sum which will add balance progress
ExpIncProgressDf['Balance'] = (ExpIncProgressDf['Transaction'].astype(float) * ExpIncProgressDf['Rate'].astype(float)).cumsum()

# sort expenses, incomes and transfers tables by date
ExpensesDf.fillna(value=values, inplace=True)
ExpensesDf[['Transaction', 'Rate']] = ExpensesDf[['Transaction', 'Rate']].astype(float)
ExpensesDf['Transact'+MainCurrency] = ExpensesDf['Transaction'] * ExpensesDf['Rate']
ExpensesDf['Date'] = pd.to_datetime(ExpensesDf['Date'], format=DATE_FORMAT)
ExpensesDf = ExpensesDf.sort_values('Date')
ExpensesDf = ExpensesDf.fillna('-')

IncomesDf['Date'] = pd.to_datetime(IncomesDf['Date'], format=DATE_FORMAT)
IncomesDf.fillna(value=values, inplace=True)
IncomesDf[['Transaction', 'Rate']] = IncomesDf[['Transaction', 'Rate']].astype(float)
IncomesDf['Transact'+MainCurrency] = IncomesDf['Transaction'] * IncomesDf['Rate']
IncomesDf = IncomesDf.sort_values('Date')
IncomesDf = IncomesDf.fillna('-')

TransfersDf['Date'] = pd.to_datetime(TransfersDf['Date'], format=DATE_FORMAT)
TransfersDf.fillna(value=values, inplace=True)
TransfersDf[['Amount', 'Rate']] = TransfersDf[['Amount', 'Rate']].astype(float)
TransfersDf['CurrencyTo'] = TransfersDf['Amount'] / TransfersDf['Rate']
TransfersDf = TransfersDf.sort_values('Date')

### Export to csv - uncomment if necessary
#ExpensesDf.to_csv("_Expenses.csv", sep=',', encoding='utf-8', index=False, columns = ['Transaction','Account','Category','Date','Rate','Comment'])
#IncomesDf.to_csv("_Incomes.csv", sep=',', encoding='utf-8', index=False, columns = ['Transaction','Account','Category','Date','Rate','Comment'])
#TransfersDf.to_csv("_Transfers.csv", sep=',', encoding='utf-8', index=False, columns = ['Transfer from','Transfer to','Amount','Date','Note','Rate'])

# get list of Accounts
uniqueAccountDf = InitialAccounts['Account'].unique()
uniqueCurrency = InitialAccounts['Currency'].unique()

allAccountsList = []
# in this for cycle calculate actual balance for every accout
for acc in range(0, len(InitialAccounts['Account'])):
        
    tmpTransfer = TransfersDf[TransfersDf["Transfer to"] == InitialAccounts['Account'][acc]].sum().fillna(0)["CurrencyTo"] - TransfersDf[TransfersDf["Transfer from"] == uniqueAccountDf[acc]].sum().fillna(0)["Amount"]
    tmpIncome = IncomesDf[IncomesDf["Account"] == InitialAccounts['Account'][acc]].sum().fillna(0)["Transaction"]
    tmpExpense = ExpensesDf[ExpensesDf["Account"] == InitialAccounts['Account'][acc]].sum().fillna(0)["Transaction"]
    tmpInitial = InitialAccounts[InitialAccounts["Account"] == InitialAccounts['Account'][acc]].sum().fillna(0)["Initial Balance"]
    tmpActive = InitialAccounts[InitialAccounts["Account"] == InitialAccounts['Account'][acc]]["Active"].values[0]
    tmpActual = tmpInitial + tmpExpense + tmpIncome + tmpTransfer
    tmpTransfer = round(tmpTransfer, 2)
    tmpIncome = round(tmpIncome, 2)
    tmpExpense = round(tmpExpense, 2)
    tmpInitial = round(tmpInitial, 2)
    tmpActual = round(tmpActual, 2)
    tmpInCurrency = round(tmpActual*EXCHANGE_RATES.get(InitialAccounts['Currency'][acc]), 2)
    allAccountsList.append([InitialAccounts['Account'][acc],InitialAccounts['Currency'][acc],tmpActive,tmpTransfer,tmpIncome,tmpExpense, tmpActual, tmpInCurrency])
        
# format created tables to dataframes
columnsForAccounts=['Account','Currency','Active','Transfers','Incomes','Expenses','Balance','Balance in main currency']
allDfAccounts = pd.DataFrame(allAccountsList, columns = columnsForAccounts)

# Calucualte sum of balances for each currency (or each set category of holdings)
totalBalance = allDfAccounts['Balance'].sum()

### placeholder for callback
categoryDfEmpty = pd.DataFrame(columns=['Category', 'Amount'])

###############################################################################    
####################        Dash APP                      #####################
###############################################################################   
# get actual date and time
now = dt.now()

# create Dash app
app = dash.Dash()

# run local server
app.scripts.config.serve_locally = True
app.css.config.serve_locally = True

# app layout
app.layout = html.Div(children=[
        
    html.H1(children='Personal Finance analysis'),
    html.H3(children=YOUR_NAME),
         

    # date range pickers
    html.Div([
      html.Table([

              html.Tr([html.Th(['Date from:']), html.Th(['Date to:'])]),

              html.Tr([html.Td([dcc.Input(id='datePickerFrom',
                      className = 'btn btn-secondary',
                      type='date',
                      value=dt.strftime(dt(InitialDateList[0], InitialDateList[1], InitialDateList[2]) + timedelta(hours=1), '%Y-%m-%d'),
                      )]),    
                      html.Td([dcc.Input(id='datePickerTo',
                      className = 'btn btn-secondary',
                      type='date',
                      value=dt.strftime(dt(now.year, now.month, now.day) + timedelta(hours=UTC_OFFSET_HOURS), '%Y-%m-%d'),
                      )])    
                      ]),
        
                      ],className='simpleTable',
      )],className='divCenter'),          

    html.H3(),
    
    ### Tabs section
    dcc.Tabs(id="tabs", parent_className='custom-tabs', className='custom-tabs-container', value='tab-2', children=[
            
            dcc.Tab(label='Accounts', className='custom-tab', selected_className='custom-tab--selected', value='tab-1',
                children=[
                    html.Div(id='containerAllTab1'),                           
                    html.H3('All accounts'),
                    html.Div(id='container1Tab1'),
                    html.Div(html.Br()),
                    html.Div(FinanceDashFunctions.createAccountDatatable('dataTable1Tab1', allDfAccounts)),
               ]),
            dcc.Tab(label='Dashboard', className='custom-tab', selected_className='custom-tab--selected', value='tab-2', 
                children=[
                    html.Div(id='container1Tab2'),
                    html.Div(id='container2Tab2'),
                    html.H3('Incomes'),
                    html.Div(FinanceDashFunctions.createCategoryDatatable('dataTable1Tab2', categoryDfEmpty),className='divCenter50'),
                    html.H3('Expenses'),
                    html.Div(FinanceDashFunctions.createCategoryDatatable('dataTable2Tab2', categoryDfEmpty),className='divCenter50'),
            ]),
            dcc.Tab(label='Monthly', className='custom-tab', selected_className='custom-tab--selected', value='tab-3',   
                children=[
                    html.Div(id='container1Tab3'),    
                    html.Div(id='container2Tab3'),
            ]),
            dcc.Tab(label='Tables', className='custom-tab', selected_className='custom-tab--selected', value='tab-4',  
                children=[
                    html.H3('Expenses'),
                    html.Div(id='container1Tab4'), 
                    html.Div(html.Br()),
                    html.Div(FinanceDashFunctions.createIncExpDataTable('dataTable1Tab4', ExpensesDf)),
                    html.Div(html.Br()),
                    html.Div(html.Br()),
                    html.H3('Incomes'),
                    html.Div(id='container2Tab4'),
                    html.Div(html.Br()),
                    html.Div(FinanceDashFunctions.createIncExpDataTable('dataTable2Tab4', IncomesDf)),
            ]),
    ]),
                      
    html.Footer(['Copyright 2020 © - 747 Developments']),
    
])
                      

###############################################################################
##################### TAB 1 callbacks           ###############################
###############################################################################
@app.callback(
    
     Output('dataTable1Tab1', 'data'),
    
    [
     Input('dataTable1Tab1', 'filter_query'),
     Input('dataTable1Tab1', 'sort_by'),
     Input('dataTable1Tab1', 'page_current'),
     Input('dataTable1Tab1', 'page_size'),
    ]
)
def updateTable1Tab1(filter_query, sort_by, page_current, page_size):
    
    dff = allDfAccounts.copy() 
    ### table filter data
    if not dff.empty:
        dff = dev_747_DashDatatableFunc.tableFilter(dff, filter_query)
    ### table filter data
    if not dff.empty:
        dff = dev_747_DashDatatableFunc.tableSortData(dff, sort_by, page_current, page_size)
           
    return dff.to_dict('records')      

### Callback for container with graphs and summary
@app.callback(
    Output('container1Tab1', "children"),    
    [
     Input('dataTable1Tab1', "derived_virtual_data"),
     Input('dataTable1Tab1', "derived_virtual_selected_rows"),
    ]
)
def updateContainer1Tab1(rows, derived_virtual_selected_rows):
     
    return FinanceDashFunctions.displayDesiredBalance(rows, derived_virtual_selected_rows, allDfAccounts, MainCurrency)

###############################################################################
##################### TAB 2 callbacks           ###############################
############################################################################### 
@app.callback(  
    [ 
     Output('container1Tab2', 'children'),
     Output('dataTable1Tab2', 'data'),
     Output('dataTable2Tab2', 'data'),
     Output('container2Tab2', 'children'),
    ],
    [
     Input('datePickerFrom', 'value'),
     Input('datePickerTo', 'value'),
    ]
)
def updateTab2(dateFrom, dateTo):

    tmpExpIncProgressDf = ExpIncProgressDf.copy()
    tmpExpensesDf = ExpensesDf.copy()
    tmpIncomesDf = IncomesDf.copy()
    
    tmpExpIncProgressDf = dev_747_DashDatatableFunc.tableDateFilter(tmpExpIncProgressDf, dateFrom, 'Date', '>=')   
    tmpExpIncProgressDf = dev_747_DashDatatableFunc.tableDateFilter(tmpExpIncProgressDf, dateTo, 'Date', '<=') 
    
    tmpExpensesDf = dev_747_DashDatatableFunc.tableDateFilter(tmpExpensesDf, dateFrom, 'Date', '>=')   
    tmpExpensesDf = dev_747_DashDatatableFunc.tableDateFilter(tmpExpensesDf, dateTo, 'Date', '<=') 
    
    tmpIncomesDf = dev_747_DashDatatableFunc.tableDateFilter(tmpIncomesDf, dateFrom, 'Date', '>=')   
    tmpIncomesDf = dev_747_DashDatatableFunc.tableDateFilter(tmpIncomesDf, dateTo, 'Date', '<=')     
     
    categoryExpenseDf = tmpExpensesDf.copy()
    categoryExpenseDf.rename(columns={'Transact'+MainCurrency: 'Amount'}, inplace=True)
    categoryExpenseDf = round(categoryExpenseDf.groupby('Category', as_index=False, sort=False)['Amount'].sum().fillna(0),2)
    categoryExpenseDf['Amount'] = -categoryExpenseDf['Amount']
    categoryExpenseDf = categoryExpenseDf.sort_values('Amount', ascending=False) 
    categoryExpenseDf.reset_index(inplace=True, drop=True)
    
    categoryIncomesDf = tmpIncomesDf.copy()
    categoryIncomesDf.rename(columns={'Transact'+MainCurrency: 'Amount'}, inplace=True)
    categoryIncomesDf = round(categoryIncomesDf.groupby('Category', as_index=False, sort=False)['Amount'].sum().fillna(0),2)
    categoryIncomesDf = categoryIncomesDf.sort_values('Amount', ascending=False)        
    categoryIncomesDf.reset_index(inplace=True, drop=True)   
    
    # calculate total incomes and expenses
    totalExpenseValue = tmpExpensesDf['Transact'+MainCurrency].fillna(0)
    totalExpenseValue = totalExpenseValue.sum() * (-1)
    totalIncomeValue = tmpIncomesDf['Transact'+MainCurrency].fillna(0)
    totalIncomeValue = totalIncomeValue.sum()

    ## create Div with statistics and graphs to return with callback
    divToReturn1 = html.Div([            
        ### create graphs based on selected data
        html.Div([  
            dcc.Graph(
                id='graphBalanceProgress',
                figure={
                    "data": [
                        {
                            "y": tmpExpIncProgressDf['Balance'],
                            "x": tmpExpIncProgressDf['Date'],
                            "type": "area",
                            "fill":'tonexty',
                        }
                    ],
                    "layout": 
                        dev_747_DashGraphFunc.graphStyle('Balance Progress', 500, THEME_DARK),                        
                },
            )
        ]),  
        html.Div([            
            dcc.Graph(
                id='graphTotalIncExpBar',
                figure={
                    "data": [
                        {
                            "y": [totalIncomeValue, totalExpenseValue],
                            "x": ['Incomes','Expenses'],
                            "type": "bar",
                            "marker":dict(
                                color=[dev_747_styles.selectRGBAcolor('color_green1'),
                                       dev_747_styles.selectRGBAcolor('color_red1')]
                            ),
                        }
                    ],
                    "layout":
                        dev_747_DashGraphFunc.graphStyle('Incomes and Expenses', 400, THEME_DARK),
                },
            ),
        ]),
    ])
            
    ## create Div with statistics and graphs to return with callback
    divToReturn2 = html.Div([            
        ### create graphs based on selected data
        html.Div([  
            dcc.Graph(
                id='graphIncExpByCatBar',
                figure={
                    "data": [
                        {
                            "y": categoryIncomesDf['Amount'],
                            "x": categoryIncomesDf['Category'],
                            "type": "bar",
                            "name": 'Incomes',
                            "text": categoryIncomesDf['Category'],
                            "marker":dict(
                                color=dev_747_styles.selectRGBAcolor('color_green1')
                            ),
                        },
                        {
                            "y": categoryExpenseDf['Amount'],
                            "x": categoryExpenseDf['Category'],
                            "type": "bar",
                            "name": 'Expenses',
                            "text": categoryExpenseDf['Category'],
                            "marker":dict(
                                color=dev_747_styles.selectRGBAcolor('color_red1')
                            ),
                        }
                    ],
                    "layout":
                        dev_747_DashGraphFunc.graphStyle('Incomes and Expenses by category', 400, THEME_DARK),
                },
            )
        ]),            
            
        html.Div([  
            dcc.Graph(
                id='graphCatIncExpPie',
                figure={
                    "data": [
                        {
                            "values": categoryIncomesDf['Amount'],
                            "labels": categoryIncomesDf['Category'],
                            "type": "pie",
                            "name": 'Incomes',
                            "domain": {"x": [0, .48]},
                            "textinfo":'none',
                            "hoverinfo":"label+percent+name+value",
                        },
                        {
                            "values": categoryExpenseDf['Amount'],
                            "labels": categoryExpenseDf['Category'],
                            "type": "pie",
                            "name": 'Expenses',
                            "domain": {"x": [.52, 1]},
                            "textinfo":'none',
                            "hoverinfo":"label+percent+name+value",
                        }
                    ],
                    "layout":
                        dev_747_DashGraphFunc.graphStyle('', 500, THEME_DARK),
                },
            ),
        ]),  
    ])            

    return divToReturn1, categoryIncomesDf.to_dict('records'), categoryExpenseDf.to_dict('records'), divToReturn2

###############################################################################
##################### TAB 3 callbacks           ###############################
############################################################################### 
@app.callback(  
     Output('container1Tab3', 'children'),
    [
     Input('datePickerFrom', 'value'),
     Input('datePickerTo', 'value'),
    ]
)
def updateTab3(dateFrom, dateTo):

    monthExpenseDf = ExpensesDf.copy()
    monthIncomesDf = IncomesDf.copy()
       
    monthExpenseDf = dev_747_DashDatatableFunc.tableDateFilter(monthExpenseDf, dateFrom, 'Date', '>=')   
    monthExpenseDf = dev_747_DashDatatableFunc.tableDateFilter(monthExpenseDf, dateTo, 'Date', '<=')      

    monthIncomesDf = dev_747_DashDatatableFunc.tableDateFilter(monthIncomesDf, dateFrom, 'Date', '>=')   
    monthIncomesDf = dev_747_DashDatatableFunc.tableDateFilter(monthIncomesDf, dateTo, 'Date', '<=')         
    
    monthExpenseDf.rename(columns={'Transact'+MainCurrency: 'Amount'}, inplace=True)
    monthExpenseDf['Date'] = monthExpenseDf['Date'].dt.strftime('%B %Y')
    monthExpenseDf = monthExpenseDf.groupby(['Category','Date'], as_index=False, sort=False)['Amount'].sum().fillna(0)
    monthExpenseDf['Amount'] = -monthExpenseDf['Amount'] 
    monthExpenseDf.reset_index(inplace=True, drop=True)
    
    monthExpenseTotalDf = monthExpenseDf.copy()
    monthExpenseTotalDf = monthExpenseTotalDf.groupby(['Date'], as_index=False, sort=False)['Amount'].sum()
    
    # get unique categories of incomes        
    monthIncomesDf.rename(columns={'Transact'+MainCurrency: 'Amount'}, inplace=True)
    monthIncomesDf['Date'] = monthIncomesDf['Date'].dt.strftime('%B %Y')
    monthIncomesDf = monthIncomesDf.groupby(['Category','Date'], as_index=False, sort=False)['Amount'].sum().fillna(0)  
    monthIncomesDf.reset_index(inplace=True, drop=True)
    
    # format df to print table
    monthIncomesTotalDf = monthIncomesDf.copy()
    monthIncomesTotalDf = monthIncomesTotalDf.groupby(['Date'], as_index=False, sort=False)['Amount'].sum() 

    # Generate monthly bar chart of expenses by category
    uniqueCategoryExp = monthExpenseDf['Category'].unique()
    dataExpenseToPlot = []
    for categ in uniqueCategoryExp:
        if categ == 'Food and drink':        
            dataExpenseToPlot.append(go.Bar(x=monthExpenseDf[monthExpenseDf['Category'] == categ]['Date'],y=monthExpenseDf[monthExpenseDf['Category'] == categ]['Amount'],name=categ, visible=True),)
        else:
            dataExpenseToPlot.append(go.Bar(x=monthExpenseDf[monthExpenseDf['Category'] == categ]['Date'],y=monthExpenseDf[monthExpenseDf['Category'] == categ]['Amount'],name=categ, visible="legendonly"),)
 
    uniqueCategoryInc = monthIncomesDf['Category'].unique()
    dataIncomesToPlot = []
    for categ in uniqueCategoryInc:
        if categ == 'Salary':        
            dataIncomesToPlot.append(go.Bar(x=monthIncomesDf[monthIncomesDf['Category'] == categ]['Date'],y=monthIncomesDf[monthIncomesDf['Category'] == categ]['Amount'],name=categ, visible=True),)
        else:
            dataIncomesToPlot.append(go.Bar(x=monthIncomesDf[monthIncomesDf['Category'] == categ]['Date'],y=monthIncomesDf[monthIncomesDf['Category'] == categ]['Amount'],name=categ, visible="legendonly"),)
         
    ## create Div with statistics and graphs to return with callback
    divToReturn1 = html.Div([            
        ### create graphs based on selected data
        html.Div([  
            dcc.Graph(
                id='graphMonthBarIncExp',
                figure={
                    "data": [
                        {
                            "y": monthIncomesTotalDf['Amount'],
                            "x": monthIncomesTotalDf['Date'],
                            "type": "bar",
                            "name": 'Incomes',
                            "labels": 'Incomes',
                            "marker":dict(
                                color=dev_747_styles.selectRGBAcolor('color_green1')
                            ),                            
                        },
                        {
                            "y": monthExpenseTotalDf['Amount'],
                            "x": monthExpenseTotalDf['Date'],
                            "type": "bar",
                            "name": 'Expenses',
                            "labels": 'Expenses',
                            "marker":dict(
                                color=dev_747_styles.selectRGBAcolor('color_red1')
                            ),                            
                        }
                    ],
                    "layout":
                        dev_747_DashGraphFunc.graphStyle('Total monthly incomes and expenses', 400, THEME_DARK),
                },
            )
        ]),            
            
        html.Div([  
            dcc.Graph(
                id='graphMonthBarExpCat',
                figure={
                      'data':dataExpenseToPlot,
                      'layout': dev_747_DashGraphFunc.graphStyle('Monthly expenses by category', 500, THEME_DARK, 'stack'),
                      },
            ),
        ]),  
        html.Div([  
            dcc.Graph(
                id='graphMonthBarIncCat',
                figure={
                      'data':dataIncomesToPlot,
                      'layout': dev_747_DashGraphFunc.graphStyle('Monthly incomes by category', 500, THEME_DARK, 'stack'),
                      },
            ),
        ]),                      
    ])            

    return divToReturn1

###############################################################################
##################### TAB 4 callbacks           ###############################
############################################################################### 
@app.callback(  
    [
     Output('container1Tab4', 'children'),
     Output('dataTable1Tab4', 'data'),
    ],
    [
     Input('datePickerFrom', 'value'),
     Input('datePickerTo', 'value'),
     Input('dataTable1Tab4', 'filter_query'),
     Input('dataTable1Tab4', 'sort_by'),
     Input('dataTable1Tab1', 'page_current'),
     Input('dataTable1Tab1', 'page_size'),
    ]
)
def updateExpensesTab4(dateFrom, dateTo, filter_query, sort_by, page_current, page_size):

    dff = ExpensesDf.copy()
   
    dff.rename(columns={'Transact'+MainCurrency: 'Amount '+MainCurrency}, inplace=True)
    dff['Amount '+MainCurrency] = -dff['Amount '+MainCurrency] 
    
    dff = dff.sort_values('Date', ascending=False)

    dff.reset_index(inplace=True, drop=True)

    ### table filter data
    if not dff.empty:
        dff = dev_747_DashDatatableFunc.tableFilter(dff, filter_query)
    ### table filter data
    if not dff.empty:
        dff = dev_747_DashDatatableFunc.tableSortData(dff, sort_by, page_current, page_size)
    if not dff.empty:
        dff = dev_747_DashDatatableFunc.tableDateFilter(dff, dateFrom, 'Date', '>=')   
        dff = dev_747_DashDatatableFunc.tableDateFilter(dff, dateTo, 'Date', '<=') 
    
    expenseTotalSum = dff['Amount '+MainCurrency].sum()
    
    divToReturn = ('Total selected expenses: ' + '{:,.2f}'.format(expenseTotalSum) + ' ' + MainCurrency)

    return divToReturn, dff.to_dict('records')

@app.callback(  
    [
     Output('container2Tab4', 'children'),
     Output('dataTable2Tab4', 'data'),
    ],
    [
     Input('datePickerFrom', 'value'),
     Input('datePickerTo', 'value'),
     Input('dataTable2Tab4', 'filter_query'),
     Input('dataTable2Tab4', 'sort_by'),
     Input('dataTable1Tab1', 'page_current'),
     Input('dataTable1Tab1', 'page_size'),
    ]
)
def updateIncomesTab4(dateFrom, dateTo, filter_query, sort_by, page_current, page_size):

    dff = IncomesDf.copy()
    
    dff.rename(columns={'Transact'+MainCurrency: 'Amount '+MainCurrency}, inplace=True)
        
    dff = dff.sort_values('Date', ascending=False)

    dff.reset_index(inplace=True, drop=True)

    ### table filter data
    if not dff.empty:
        dff = dev_747_DashDatatableFunc.tableFilter(dff, filter_query)
    ### table filter data
    if not dff.empty:
        dff = dev_747_DashDatatableFunc.tableSortData(dff, sort_by, page_current, page_size)
    
    if not dff.empty:
        dff = dev_747_DashDatatableFunc.tableDateFilter(dff, dateFrom, 'Date', '>=')   
        dff = dev_747_DashDatatableFunc.tableDateFilter(dff, dateTo, 'Date', '<=') 
    
    incomesTotalSum = dff['Amount '+MainCurrency].sum()
    
    divToReturn = ('Total selected incomes: ' + '{:,.2f}'.format(incomesTotalSum) + ' ' + MainCurrency)

    return divToReturn, dff.to_dict('records')  

###############################################################################
#######################  Run Dash App               ###########################
###############################################################################    
# open web browser automatically
webbrowser.open('http://127.0.0.1:8050', new=1, autoraise=True)
# remove unnecessary folder with cash if created
shutil.rmtree('./__pycache__',ignore_errors=True)
    
# run the local server
if __name__ == '__main__':    
    app.run_server(debug=False)