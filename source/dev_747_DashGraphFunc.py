from dash import dcc
import dev_747_styles

def graphStyle(graphTitle, graphHeight, colorMode, barmode = ''):

    style={ 
        } 

    if(colorMode):
        style={
            'title': graphTitle,
            'height': graphHeight,
            'font': {'color': dev_747_styles.HEX_COLORS_BOOTSTRAP['text']},
            'xaxis': {'color': dev_747_styles.HEX_COLORS_BOOTSTRAP['text']},
            'yaxis': {'color': dev_747_styles.HEX_COLORS_BOOTSTRAP['text']},
            'barmode': barmode,
            'plot_bgcolor': dev_747_styles.HEX_COLORS_BOOTSTRAP['gray-secondary'],
            'paper_bgcolor': dev_747_styles.HEX_COLORS_BOOTSTRAP['gray-secondary'],
            }
        #style.update( {'plot_bgcolor': dev_747_styles.HEX_COLORS_BOOTSTRAP['gray-secondary']} )
        #style.update( {'paper_bgcolor': dev_747_styles.HEX_COLORS_BOOTSTRAP['gray-secondary']} )  
               
    return style

def plotBarChartHorizontal(graphID, dataframe, yLabel, xLabel, graphTitle, graphHeight, barColors=""):
    
    graphToReturn = dcc.Graph(
                id=graphID,
                figure={
                    "data": [
                        {
                            "y": dataframe[xLabel] if len(dataframe) else [],
                            "x": dataframe[yLabel] if yLabel in dataframe else [],
                            "type": "bar",
                            "orientation":"h",
                            "marker": dict(color=barColors),
                        }
                    ],
                    "layout": 
                        graphStyle(graphTitle, graphHeight), 
                },
            )    
    return (graphToReturn) 