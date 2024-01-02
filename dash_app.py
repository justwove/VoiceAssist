import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import base64

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("File Upload and Download"),
    html.H3("Upload a Video/Audio File"),
    dcc.Upload(
        id='upload-video',
        children=html.Button('Select Video/Audio File')
    ),
    html.H3("Upload a Text Document"),
    dcc.Upload(
        id='upload-text',
        children=html.Button('Select Text Document')
    ),
    html.H3("Download a File"),
    html.Button('Download', id='download-button'),
    dcc.Download(id='download')
])

@app.callback(
    Output('download', 'data'),
    Input('download-button', 'n_clicks')
)
def download_file(n_clicks):
    if n_clicks is not None:
        # Replace 'file_path' with the actual file path
        with open('file_path', 'rb') as file:
            file_content = file.read()
        return dcc.send_data_frame(file_content, filename='file.txt')

@app.callback(
    Output('upload-video', 'children'),
    Output('upload-text', 'children'),
    Input('upload-video', 'contents'),
    Input('upload-text', 'contents'),
    State('upload-video', 'filename'),
    State('upload-text', 'filename')
)
def upload_files(video_content, text_content, video_filename, text_filename):
    if video_content is not None:
        # Replace 'video_path' with the actual path to save the video file
        with open('video_path', 'wb') as file:
            file.write(base64.b64decode(video_content.split(',')[1]))
        return html.Button(f'Selected: {video_filename}')
    elif text_content is not None:
        # Replace 'text_path' with the actual path to save the text file
        with open('text_path', 'w') as file:
            file.write(text_content)
        return html.Button(f'Selected: {text_filename}')
    else:
        return html.Button('Select Video/Audio File'), html.Button('Select Text Document')

if __name__ == '__main__':
    app.run_server(debug=True)
