from dash import dash_table
import pandas as pd
from dash import html

def displayDesiredBalance(rows, derived_virtual_selected_rows, dataframe, currency):
        ### the selectino for the checkboxes in datatable
    if derived_virtual_selected_rows is None:
        derived_virtual_selected_rows = []

    if rows is None:
        dff = dataframe.copy()
    else:
        dff = pd.DataFrame(rows)

    allReturn = []
    #allReturn = ''.join(str(x) for x in allReturn)
    ### Compute statistics from selected range of data
    if not dff.empty:
        if len(derived_virtual_selected_rows):
            totalBalance = dff['Balance in main currency'].iloc[derived_virtual_selected_rows].sum()            
            uniqueCurrencies = dff['Currency'].iloc[derived_virtual_selected_rows].unique()
            for cur in uniqueCurrencies:
                testBalance = dff.iloc[derived_virtual_selected_rows]
                testBalance = testBalance[testBalance['Currency'] == cur].sum()
                #tmpBalance = tmpBalance['Actual Balance']
                #tmpBalance = dff[dff['Currency'] == cur].iloc[derived_virtual_selected_rows].sum()
                #print(tmpBalance['Actual Balance'])
                tmpBalance = testBalance['Balance']
                #print(cur, ' ', tmpBalance)
                newReturn = html.Div([('Selected ' + cur + ' balance: ' + '{:,.2f}'.format(tmpBalance) + ' ' + cur), html.Br()])
                allReturn.append(('Selected ' + cur + ' balance: ' + '{:,.2f}'.format(tmpBalance) + ' ' + cur))
                #allReturn = ''.join(str(x) for x in allReturn)
        else:            
            totalBalance = round(dff['Balance in main currency'].sum(),2)                
    else:
        totalBalance = 0.00
        
    
    allReturn.append(('Total selected ' + currency + ' balance in main currency: ' + '{:,.2f}'.format(totalBalance) + ' ' + currency))
    allReturn = pd.DataFrame(allReturn, columns = ['Divs'])
    toReturn = html.Div([html.Strong(col) if 'Total' in col else html.P(col) for col in allReturn.Divs])
    return toReturn

def createCategoryDatatable(tableID, dataframe):
    return html.Div([
        dash_table.DataTable(
        id=tableID,
        columns=[
        {
            'id': 'Category',
            'name': 'Category',
            'type': 'text'
        }, {
            'id': 'Amount',
            'name': 'Amount [CZK]',
            'type': 'numeric',
            'format': {'specifier': ',.2f','precision':2,},            
        }, 
        ],
        data=dataframe.to_dict('records'),
        
        editable=False,        
        filter_action='custom',
        filter_query='',
        sort_action='custom',
        sort_mode='multi',
        sort_by=[],
        page_action='none',
        
        row_selectable = False,       
        row_deletable = False,        
        
        style_data_conditional=[
            {'if': {'column_id': 'Category'},
                 'width': '55%', 'textAlign': 'left', 'fontWeight': 'normal'},
            {'if': {'column_id': 'Amount'},
                 'width': '45%'},           
        ],                 
        ),
    ])

def createAccountDatatable(tableID, dataframe):
   
    return html.Div([
        dash_table.DataTable(
        id=tableID,
                
        columns=[
        {
            'id': 'Account',
            'name': 'Account',
            'type': 'text'
        }, {
            'id': 'Currency',
            'name': 'Currency',
            'type': 'text',
        }, {
            'id': 'Active',
            'name': 'Active',
            'type': 'text',
        }, {
            'id': 'Transfers',
            'name': 'Transfers',
            'type': 'numeric',
            'format': {'specifier': ',.2f','precision':2,},            
        }, {
            'id': 'Incomes',
            'name': 'Incomes',
            'type': 'numeric',
            'format': {'specifier': ',.2f','precision':2,},
        }, {
            'id': 'Expenses',
            'name': 'Expenses',
            'type': 'numeric',
            'format': {'specifier': ',.2f','precision':2,},
        }, {
            'id': 'Balance',
            'name': 'Balance',
            'type': 'numeric',
            'format': {'specifier': ',.2f','precision':2,},
        }, {
            'id': 'Balance in main currency',
            'name': 'Balance in main currency',
            'type': 'numeric',
            'format': {'specifier': ',.2f','precision':2,},
        },
        ],
                  
        data=dataframe.to_dict('records'),
      
        editable=False,
        
        filter_action='custom',
        filter_query='',
        sort_action='custom',
        sort_mode='multi',
        sort_by=[],
        page_action='none',
        
        row_selectable = 'multi',
        selected_rows=[],
        
        row_deletable=False,
             
        style_data_conditional=[

            {'if': {'column_id': 'Account'},
                 'width': '26%', 'textAlign': 'left', 'fontWeight': 'bold'},
            {'if': {'column_id': 'Active'},
                 'width': '7%', 'textAlign': 'left'},
            {'if': {'column_id': 'Currency'},
                 'width': '7%', 'textAlign': 'left'},
             ] + [ 
            {'if': {'column_id': c}, 'width': '12%'} 
                for c in ['Transfers', 'Incomes', 'Expenses', 'Balance', 'Balance in main currency']           
        ], 
                         
        ),
    ])

def createIncExpDataTable(tableID, dataframe):
    return html.Div([
        dash_table.DataTable(
        id=tableID,
        
        columns=[
        {
            'id': 'Account',
            'name': 'Account',
            'type': 'text',
        }, {
            'id': 'Category',
            'name': 'Category',
            'type': 'text',           
        }, {
            'id': 'Comment',
            'name': 'Comment',
            'type': 'text',
        }, {
            'id': 'Date',
            'name': 'Date',
            'type': 'date',
        }, {
            'id': 'Transaction',
            'name': 'Transaction',
            'type': 'numeric',
            'format': {'specifier': ',.2f','precision':2,},
        }, {
            'id': 'Rate',
            'name': 'Rate',
            'type': 'numeric',
            'format': {'specifier': '.2f','precision':2,},
        }, {
            'id': 'Amount CZK',
            'name': 'Amount CZK',
            'type': 'numeric',
            'format': {'specifier': ',.2f','precision':2,},
        },
        ],
           
        data=dataframe.to_dict('records'),
      
        editable=False,
        
        filter_action='custom',
        filter_query='',
        sort_action='custom',
        sort_mode='multi',
        sort_by=[],
        page_action='native',
        page_current= 0,
        page_size= 30,
        
        row_selectable = 'multi',
        selected_rows=[],
        
        row_deletable=False,

        fixed_rows=2,
        
        style_data_conditional=[
                
            {'if': {'column_id': c}, 'width': '16%', 'textAlign': 'left'} 
                for c in ['Date', 'Category', 'Comment', 'Account']           
                ] + [ 
            {'if': {'column_id': c}, 'width': '12%'} 
                for c in ['Rate', 'Transaction', 'Amount CZK']           
                ],      
                 
        ),
    ])    
    