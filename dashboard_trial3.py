import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import base64
import io

class Dashboard:

    def application(self, *description):
        self.description = description

        app = dash.Dash(__name__)

        app.layout = html.Div([
            dcc.Upload(
                id='upload-data',
                children=html.Div([
                    'Drag and Drop or ',
                    html.A('Select Files')
                ]),
                style={
                    'width': '100%',
                    'height': '60px',
                    'lineHeight': '60px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    'margin': '10px'
                },
                # Allow multiple files to be uploaded
                multiple=False
            ),
            html.Div(id='output-data-upload')
        ])

        @app.callback(Output('output-data-upload', 'children'),
                      [Input('upload-data', 'contents')],
                      [dash.dependencies.State('upload-data', 'filename')])
        def update_output(contents, filename):
            if contents is not None:
                content_type, content_string = contents.split(',')
                decoded = base64.b64decode(content_string)
                try:
                    if 'csv' in filename:
                        # Assume that the user uploaded a CSV file
                        df = pd.read_csv(
                            io.StringIO(decoded.decode('utf-8')))
                    elif 'xls' in filename:
                        # Assume that the user uploaded an excel file
                        df = pd.read_excel(io.BytesIO(decoded))
                except Exception as e:
                    print(e)
                    return html.Div([
                        'There was an error processing this file.'
                    ])

                number_columns = len(df.columns)

                # make a dictionary with number of columns and their names
                list_count_columns = list(range(1, number_columns))
                res = {description[i]: list_count_columns[i] for i in range(len(description))}

                output =[]
                i = 0
                for j, k in res.items():
                    output.append(
                        dcc.Graph(
                            id='graph'+str(i),
                            figure={
                                'data': [go.Scatter(
                                    showlegend=True,
                                    marker_color='rgba(128, 128, 128, .9)',
                                    mode='lines', 
                                    x=list(df.iloc[:, 0]),  # Using the first column as x-axis
                                    y=list(df.iloc[:, k]), 
                                    name=str(j)
                                )],
                                'layout': go.Layout(
                                    xaxis={'title': df.columns[0]},  # Set x-axis title to the first column name
                                    yaxis={'title': 'Y-axis'},
                                    margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                                    hovermode='closest'
                                )
                            }
                        )
                    )
                    i += 1

                return html.Div(output)

        if __name__ == '__main__':
            app.run_server(debug=True)

apps = Dashboard()

def main():
    apps.application('CpuPercent','CpuFreq','MemoryTotal','MemoryAvailable','MemoryPercent','SwapPercent','DiskReadCount','DiskWriteCount','DiskReadBytes',
                     'DiskWriteBytes','DiskPercent','PacketsReceived','PacketsSent','SystemProcesses','BootTime')

if __name__ == '__main__':
    main()
