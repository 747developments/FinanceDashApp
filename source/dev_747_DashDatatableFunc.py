from datetime import datetime as dt
import pandas as pd

operators = [['ge ', '>='],
             ['le ', '<='],
             ['lt ', '<'],
             ['gt ', '>'],
             ['ne ', '!='],
             ['eq ', '='],
             ['contains '],
             ['datestartswith ']]

def split_filter_part(filter_part):
    for operator_type in operators:
        for operator in operator_type:
            if operator in filter_part:
                name_part, value_part = filter_part.split(operator, 1)
                name = name_part[name_part.find('{') + 1: name_part.rfind('}')]

                value_part = value_part.strip()
                v0 = value_part[0]
                if (v0 == value_part[-1] and v0 in ("'", '"', '`')):
                    value = value_part[1: -1].replace('\\' + v0, v0)
                else:
                    try:
                        value = float(value_part)
                    except ValueError:
                        value = value_part

                # word operators need spaces after them in the filter string,
                # but we don't want these later
                return name, operator_type[0].strip(), value

    return [None] * 3

def tableFilter(dataframe, filter):       
    filtering_expressions = filter.split(' && ')
    dff = dataframe
    for filter_part in filtering_expressions:
        col_name, operator, filter_value = split_filter_part(filter_part)

        if operator in ('eq', 'ne', 'lt', 'le', 'gt', 'ge'):
            # these operators match pandas series operator method names
            dff = dff.loc[getattr(dff[col_name], operator)(filter_value)]
        elif operator == 'contains':
            dff = dff.loc[dff[col_name].str.lower().str.contains(filter_value.lower())]
        elif operator == 'datestartswith':
            # this is a simplification of the front-end filtering logic,
            # only works with complete fields in standard format
            dff = dff.loc[dff[col_name].str.startswith(filter_value)]

    return dff

def tableSortData(dataframe, sort_by, page_current, page_size):
    if len(sort_by):
        dff = dataframe.sort_values(
            sort_by[0]['column_id'],
            ascending=sort_by[0]['direction'] == 'asc',
            inplace=False
        )
    else:
        # No sort is applied
        dff = dataframe
    if (page_current and page_size):    
        return dff.iloc[
            page_current*page_size:(page_current+ 1)*page_size
            ]
    else:
        return dff

def tableDateFilter(dataframe, dateSelector, columnName, dateComparison):
       
    if dateSelector is not None:
        dateSelector = dt.strptime(dateSelector[:10], '%Y-%m-%d')
        if(dateComparison == '<='):
            dataframe = dataframe.loc[dataframe[columnName] <= pd.to_datetime(dateSelector)]  
        elif(dateComparison == '>='):
            dataframe = dataframe.loc[dataframe[columnName] >= pd.to_datetime(dateSelector)]  
    
    return dataframe