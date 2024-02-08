from dash import dcc, html, Dash
from dash.dependencies import Input, Output, State
from os import listdir, remove, path
import base64
from voice_taker import create_subtitles_with_ai, rename_file
from keyword_finder import keywords_extractor, get_similarite

app = Dash(__name__)

app.layout = html.Div([
    # Première colonne
    html.Div([
        html.H3('Upload de vidéo / fichier audio'),
        dcc.Upload(
            id='upload-video-audio-1',
            children=html.Div([
                'Glissez et déposez ou ',
                html.A('Sélectionnez un fichier vidéo/audio 1')
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
        ),
        dcc.Upload(
            id='upload-video-audio-2',
            children=html.Div([
                'Glissez et déposez ou ',
                html.A('Sélectionnez un fichier vidéo/audio 2')
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
        ),
        html.Div(id='output-upload-1'),
        html.Div(id='output-upload-2'),
    ], className='three columns'),

    # Deuxième colonne
    html.Div([
        html.H3('Traitement des vidéos'),
        html.Button('Télécharger les sous-titres de la vidéo 1', id='download-subtitles-1', n_clicks=0),
        html.Button('Télécharger les sous-titres de la vidéo 2', id='download-subtitles-2', n_clicks=0),
        html.Button('Récupérer les mots-clés de la vidéo 1', id='get-keywords-1', n_clicks=0),
        html.Button('Récupérer les mots-clés de la vidéo 2', id='get-keywords-2', n_clicks=0),
        dcc.Download(id='output-download-subtitles-1'),
        dcc.Download(id='output-get-keywords-1'),
        dcc.Download(id='output-get-keywords-2'),
        dcc.Download(id='output-download-subtitles-2'),
    ], className='three columns'),

    # Troisième colonne
    html.Div([
        html.H3('Matching'),
        html.Button('Afficher le pourcentage de ressemblance entre les 2 fichers de sous titres des vidéos/fichiers audio', id='match-percentage-subtitles', n_clicks=0),
        html.Div(id='output-match-percentage-subtitles'),
        html.Button('Afficher le pourcentage de ressemblance entre les 2 fichers de mots clés des vidéos/fichiers audio', id='match-percentage-keywords', n_clicks=0),
        html.Div(id='output-match-percentage-keywords'),
    ], className='three columns'),
])

##########################################################################################################
# Fonctions pour le traitement de vidéo 2

# Fonction pour gérer l'upload des vidéos/audio
@app.callback(
    Output('output-upload-1', 'children'),
    Input('upload-video-audio-1', 'contents'),
    State('upload-video-audio-1', 'filename'))
def upload_file_1(contents, filename):
    video_exist = [path.join('uploads', file) for file in listdir('uploads') if 'video_1' in file]
    if video_exist: [remove(video) for video in video_exist]
    if contents is not None:
        # TODO: Ajoutez votre logique pour sauvegarder le fichier dans le dossier 'uploads'
        file_path = f'uploads/{filename.split(".")[0]}_video_1.{filename.split(".")[1]}'
        with open(file_path, 'wb') as file:
            file.write(base64.b64decode(contents.split(',')[1]))
            rename_file(file_path)
        return f'Fichier {filename} a été uploadé avec succès.'

# Fonction pour télécharger les sous-titres de la vidéo 1
@app.callback(
    Output('output-download-subtitles-1', 'data'),
    Input('download-subtitles-1', 'n_clicks'))
def download_subtitles_1(n_clicks):
    if n_clicks > 0:
        video_1 = [path.join('uploads', file) for file in listdir('uploads') if 'video_1' in file][0]  
        subtitles = create_subtitles_with_ai(video_1)
        with open(f'{video_1.split(".")[0]}_subtitles.txt', 'w') as file: 
            file.write('\n'.join([f'{key}: {value}\n' for key, value in subtitles.items()]))
        
        return dcc.send_file(f'{video_1.split(".")[0]}_subtitles.txt', filename=f'{video_1.split(".")[0]}_subtitles.txt')

# Fonction pour récupérer les mots-clé de la vidéo 1
@app.callback(
    Output('output-get-keywords-1', 'data'),
    Input('get-keywords-1', 'n_clicks'))
def get_keywords_1(n_clicks):
    if n_clicks > 0:
        # TODO: Ajoutez votre logique pour récupérer les mots-clé
        video_1 = [path.join('uploads', file) for file in listdir('uploads') if 'video_1_subtitles' in file][0]
        keywords_extractor(video_1)
        return dcc.send_file(video_1.replace('_subtitles.txt', '_keywords.txt'), filename=video_1.replace('_subtitles.txt', '_keywords.txt'))


##########################################################################################################
# Fonctions pour le traitement de vidéo 2

# Fonction pour gérer l'upload des vidéos/audio
@app.callback(
    Output('output-upload-2', 'children'),
    Input('upload-video-audio-2', 'contents'),
    State('upload-video-audio-2', 'filename'))
def upload_file_2(contents, filename):
    video_exist = [path.join('uploads', file) for file in listdir('uploads') if 'video_2' in file]
    if video_exist: [remove(video) for video in video_exist]
    if contents is not None:
        # TODO: Ajoutez votre logique pour sauvegarder le fichier dans le dossier 'uploads'
        file_path = f'uploads/{filename.split(".")[0]}_video_2.{filename.split(".")[1]}'
        with open(file_path, 'wb') as file:
            file.write(base64.b64decode(contents.split(',')[1]))
            rename_file(file_path)
        return f'Fichier {filename} a été uploadé avec succès.'


# Fonction pour télécharger les sous-titres de la vidéo 2
@app.callback(
    Output('output-download-subtitles-2', 'data'),
    Input('download-subtitles-2', 'n_clicks'))
def download_subtitles_2(n_clicks):
    if n_clicks > 0:
        video_2 = [path.join('uploads', file) for file in listdir('uploads') if 'video_2' in file][0]  
        subtitles = create_subtitles_with_ai(video_2)
        with open(f'{video_2.split(".")[0]}_subtitles.txt', 'w') as file: 
            file.write('\n'.join([f'{key}: {value}\n' for key, value in subtitles.items()]))
        
        return dcc.send_file(f'{video_2.split(".")[0]}_subtitles.txt', filename=f'{video_2.split(".")[0]}_subtitles.txt')

# Fonction pour récupérer les mots-clé de la vidéo 2
@app.callback(
    Output('output-get-keywords-2', 'data'),
    Input('get-keywords-2', 'n_clicks'))
def get_keywords_2(n_clicks):
    if n_clicks > 0:
        # TODO: Ajoutez votre logique pour récupérer les mots-clé
        video_2 = [path.join('uploads', file) for file in listdir('uploads') if 'video_2_subtitles' in file][0]
        keywords_extractor(f'{video_2}')
        return dcc.send_file(video_2.replace('_subtitles.txt', '_keywords.txt'), filename=video_2.replace('_subtitles.txt', '_keywords.txt'))

# Fonction pour afficher le pourcentage de ressemblance entre les 2 vidéos/fichiers audio
@app.callback(
    Output('output-match-percentage-subtitles', 'children'),
    Input('match-percentage-subtitles', 'n_clicks'))
def match_percentage_subtitles(n_clicks):
    if n_clicks > 0:
        subtitles = [path.join('uploads', file) for file in listdir('uploads') if 'subtitles' in file]
        with open(subtitles[0], 'r') as file1, open(subtitles[1], 'r') as file2:
            text1 = file1.read()
            text2 = file2.read()
            print(get_similarite(text1, text2, subtitles))
            return html.Div(get_similarite(text1, text2, 'subtitles'))

# Fonction pour afficher le pourcentage de ressemblance entre les 2 vidéos/fichiers audio
@app.callback(
    Output('output-match-percentage-keywords', 'children'),
    Input('match-percentage-keywords', 'n_clicks'))
def match_percentage_keywords(n_clicks):
    if n_clicks > 0:
        keywords = [path.join('uploads', file) for file in listdir('uploads') if 'keywords' in file]
        with open(keywords[0], 'r') as file1, open(keywords[1], 'r') as file2:
            text1 = file1.read()
            text2 = file2.read()
            print(get_similarite(text1, text2, keywords))
            return html.Div(get_similarite(text1, text2, 'keywords'))
        
    
if __name__ == '__main__':
    app.run_server(debug=True)
    app.run()