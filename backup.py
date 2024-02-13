from dash import html, Dash, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from os import path, makedirs, listdir
import plotly.express as px
import plotly.graph_objects as go

import itertools

from keyword_finder import keywords_extractor, get_similarite   # Importer les fonctions de keyword_finder.py
from voice_taker import create_subtitles_with_ai, rename_file

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div(
    children=[
        dbc.Row(
            [
                dbc.Col([
                    html.Div("Upload fichier"),
                    dcc.Upload(
                        id='upload-files-cv',
                        children=html.Button('Sélectionnez un CV'),
                        multiple=True
                    ),
                    dcc.Upload(
                        id='upload-files-fp',
                        children=html.Button('Sélectionnez une fiche de poste'),
                        multiple=True
                    )], width=4),
                dbc.Col([
                    html.Div("CV"),
                    dcc.Dropdown(
                        id='dropdown-cv',
                        options=[{'label': filename, 'value': filename} for filename in listdir('CVs')],
                        placeholder="Veuillez sélectionner un CV"
                    ),
                    html.Div("Fiche de poste"),
                    dcc.Dropdown(
                        id='dropdown-fp',
                        options=[{'label': filename, 'value': filename} for filename in listdir('FPs')],
                        placeholder="Veuillez sélectionner une fiche de poste"
                    ),
                    html.Button('Lancer le traitement', id='start-working'),
                ], width=4),
                dbc.Col([
                    html.Div("Résultat"),
                    html.Div(id='finised-working')

                ], width=4),
            ]
        ),
        html.Div(id="graphs")
    ]
)

@app.callback(
    Output('upload-files', 'contents'),
    Output('dropdown-cv', 'options'),
    Input('upload-files-cv', 'contents'),
    Input('upload-files-cv', 'filename')
)
def upload_files(contents: list[str], filenames: list[str]):
    destination_folder = 'CVs'  # Répertoire de destination des fichiers téléchargés
    if not path.exists(destination_folder):
        makedirs(destination_folder)
    if contents is not None:
        for content, filename in zip(contents, filenames):
            with open(path.join(destination_folder, filename), 'wb') as file:
                file.write(content.encode('utf-8'))
    options = [{'label': filename, 'value': filename} for filename in listdir('CVs')]
    return contents, options, options

@app.callback(
    Output('upload-files', 'contents'),
    Output('dropdown-fp', 'options'),
    Input('upload-files-fp', 'contents'),
    Input('upload-files-fp', 'filename')
)
def upload_files(contents: list[str], filenames: list[str]):
    destination_folder = 'FPs'  # Répertoire de destination des fichiers téléchargés
    if not path.exists(destination_folder):
        makedirs(destination_folder)
    if contents is not None:
        for content, filename in zip(contents, filenames):
            with open(path.join(destination_folder, filename), 'wb') as file:
                file.write(content.encode('utf-8'))
    options = [{'label': filename, 'value': filename} for filename in listdir('FPs')]
    return contents, options, options

    
@app.callback(
    Output('start-working', 'children'),
    Output('finised-working', 'children'),
    Output('graphs', 'children'),
    Input('start-working', 'n_clicks'),
    State('dropdown-cv', 'value'),
    State('dropdown-fp', 'value'),

)
def check_dropdown_values(n_clicks, cvs, fps):
    if n_clicks and cvs and fps:
        for CV, FP in itertools.product(cvs, fps):
            if (CV and FP) and (CV != FP):
                CV_path = path.join('CVs', CV)
                CV_subtitles, CV_keywords = logic_attribution(CV_path)
                FP_path = path.join('FPs', FP)
                FP_subtitles, FP_keywords = logic_attribution(FP_path)
                sub_cos_similarity, sub_jac_similarity, sub_lev_distance = get_similarite(CV_subtitles, FP_subtitles)
                key_cos_similarity, key_jac_similarity, key_lev_distance = get_similarite(CV_keywords, FP_keywords)

            # Graphique Similarité Cosinus
            fig_cos = px.bar(x=['Similarité Cosinus Sous-titres', 'Mots-clés'],
                            y=[sub_cos_similarity, key_cos_similarity],
                            labels={'x': 'Similarité Cosinus', 'y': 'Valeur'})

            # Graphique Distance de Jaccard 
            fig_jacc = px.bar(x=['Sous-titres', 'Mots-clés'],
                            y=[sub_jac_similarity, key_jac_similarity],
                            labels={'x': 'Similarité de Jaccard', 'y': 'Valeur'})

            # Graphique Distance de Levenshtein
            fig_lev = px.bar(x=['Sous-titres', 'Mots-clés'],
                            y=[sub_lev_distance, key_lev_distance],
                            labels={'x': 'Distance de Levenshtein', 'y': 'Valeur'})
            return "Traitement terminé", html.Div(
                [
                    html.Div(f"Similarité du cosinus des sous-titres: {sub_cos_similarity}"),
                    html.Div(f"Similarité de Jaccard des sous-titres: {sub_jac_similarity}"),
                    html.Div(f"Distance de Levenshtein des sous-titres:{sub_lev_distance}"),
                    html.Br(),
                    html.Div(f"Similarité du cosinus des mots-clés: {key_cos_similarity}"),
                    html.Div(f"Similarité de Jaccard des mots-clés: {key_jac_similarity}"),
                    html.Div(f"Distance de Levenshtein des mots-clés: {key_lev_distance}")
                ]), dbc.Row(
                    [
                        html.Div("La Similarité du cosinus mesure la similarité entre deux textes. Plus elle est élevée, plus les textes sont similaires."), 
                        html.Div("La distance de Jaccard mesure la dissimilarité entre deux ensembles de tokens. Plus elle est faible, plus les textes sont similaires."), 
                        html.Div("La distance de Levenshtein mesure le nombre de modifications nécessaires pour transformer un texte en un autre. Plus elle est faible, plus les textes sont similaires."),
                        html.Br(),
                        html.Div("Graphiques de similarité des sous-titres et des mots clés du CV et de la fiche de poste"),
                        dbc.Col(
                            [
                            dcc.Graph(figure=fig_cos), 
                            dcc.Graph(figure=fig_jacc),
                            dcc.Graph(figure=fig_lev)], width=4),
                    ]
                )
        else:
            return "Veuillez sélectionner un CV et une fiche de poste", "", ""
    return "Lancer le traitement", "", ""


def logic_attribution(path):
    if path.endswith('.mp4'):
        subtitles = create_subtitles_with_ai(path)
    if path.endswith('.txt'):
        with open(path, 'r') as file:
            subtitles = file.read()
    
    keywords = keywords_extractor(path)
    return subtitles, keywords
if __name__ == '__main__':
    app.run_server(debug=True)
