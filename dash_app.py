import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import base64
from voice_taker import create_subtitles_with_ai
from keyword_finder import keywords_extractor

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Voice Assist"),
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
    html.Button('Download Subtitles', id='download-button-subtitles'),  # button for downloading subtitles
    html.Button('Extract and Download Keywords', id='download-button-keywords', n_clicks=0),  # button for keyword extraction and download
    dcc.Download(id='download-subtitles'),  # download component for subtitles
    dcc.Download(id='download-keywords'),  # download component for keywords
    html.Div(id='subtitle-output'),  # Div to display subtitles
    html.Div(id='keyword-output')  # Div to display keywords
])

@app.callback(
    Output('download-subtitles', 'data'),
    Input('download-button-subtitles', 'n_clicks')
)
def download_subtitles(n_clicks):
    if n_clicks is not None:  # Only run if the button has been clicked
        return dcc.send_file('subtitles.txt', filename='subtitles.txt')

@app.callback(
    Output('download-keywords', 'data'),
    Output('keyword-output', 'children'),  # New output to display keywords
    Input('download-button-keywords', 'n_clicks'),
    State('upload-video', 'contents'),
)
def extract_and_download_keywords(n_clicks, video_content):
    if n_clicks > 0 and video_content is not None:
        keywords = keywords_extractor('./subtitles.txt')
        return dcc.send_file('keywords.txt', filename='keywords.txt'), html.Div(keywords)
    else:
        return dash.no_update, html.Div()  # Return no update for 'download-keywords' and empty div for 'keyword-output'

@app.callback(
    Output('upload-video', 'children'),
    Output('upload-text', 'children'),
    Output('subtitle-output', 'children'),  # New output to display subtitles
    Input('upload-video', 'contents'),
    Input('upload-text', 'contents'),
    State('upload-video', 'filename'),
    State('upload-text', 'filename')
)
def upload_files(video_content, text_content, video_filename, text_filename):
    if video_content is not None:
        # Replace 'video_path' with the actual path to save the video file
        with open(f'./uploads/{video_filename}', 'wb') as file:
            file.write(base64.b64decode(video_content.split(',')[1]))
        subtitles = create_subtitles_with_ai(f'./uploads/{video_filename}')
        with open('subtitles.txt', 'w') as file: file.write('\n\n'.join([f'{key}: {value}\n' for key, value in subtitles.items()]))
        return html.Button(f'Selected: {video_filename}'), html.Button('Select Text Document'), html.Div('\n\n'.join([f'{key}: {value}\n' for key, value in subtitles.items()]))
    elif text_content is not None:
        # Replace 'text_path' with the actual path to save the text file
        with open(f'./uploads/{text_filename}', 'w') as file:
            file.write(text_content) 
        return html.Button(f'Selected: {text_filename}')
    else:
        return html.Button('Select Video/Audio File'), html.Button('Select Text Document'), html.Div('')

if __name__ == '__main__':
    app.run_server(debug=True)
