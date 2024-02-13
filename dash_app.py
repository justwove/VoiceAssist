from dash import html, Dash, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from os import path, makedirs, listdir
import plotly.express as px
import plotly.graph_objects as go

import pandas as pd
import base64

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
                        value=[],
                        multi=True,
                        placeholder="Veuillez sélectionner un CV"
                    ),
                    html.Button("Select All", id="cv-select-all"), 
                    html.Button("Unselect All", id="cv-unselect-all"),
                    html.Br(),
                    html.Div("Fiche de poste"),
                    dcc.Dropdown(
                        id='dropdown-fp',
                        options=[{'label': filename, 'value': filename} for filename in listdir('FPs')],
                        value=[],
                        multi=True,
                        placeholder="Veuillez sélectionner une fiche de poste"
                    ),
                    html.Button("Select All", id="fp-select-all"), 
                    html.Button("Unselect All", id="fp-unselect-all"),
                    html.Br(),
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
    Output("dropdown-fp", "value"),
    Output("dropdown-cv", "value"),
    # Output('dropdown-fp', 'options'),
    # Output('dropdown-cv', 'options'),
    Input("fp-select-all", "n_clicks"),
    Input("cv-select-all", "n_clicks"),
    Input("fp-unselect-all", "n_clicks"),
    Input("cv-unselect-all", "n_clicks"),
    # State("dropdown-fp", "options"),
    # State("dropdown-dc", "options"),
    
)
def toggle_all(fp_select_all, cv_select_all, fp_unselect_all, cv_unselect_all):#, fp_options, cv_options):
    fp_options = [{'label': filename, 'value': filename} for filename in listdir('FPs')]
    cv_options = [{'label': filename, 'value': filename} for filename in listdir('CVs')]   
    
    if fp_select_all:
        return [o["value"] for o in fp_options], ""#, fp_options, cv_options
    if cv_select_all:
        return "", [o["value"] for o in cv_options]#, fp_options, cv_options
    elif fp_unselect_all:
        return [], ""#, fp_options, cv_options
    elif cv_unselect_all:
        return "", [], fp_options, cv_options
    return None, None#, fp_options, cv_options

@app.callback(
    Output('upload-files-cv', 'contents'),
    # Output('dropdown-cv', 'options'),
    Input('upload-files-cv', 'contents'),
    Input('upload-files-cv', 'filename'),
    prevent_initial_call=True
)
def upload_files(contents: list[str], filenames: list[str]):
    destination_folder = 'CVs'  # Répertoire de destination des fichiers téléchargés
    if not path.exists(destination_folder):
        makedirs(destination_folder)
    if contents is not None:
        for content, filename in zip(contents, filenames):
            with open(path.join(destination_folder, filename), 'wb') as file:
                file.write(base64.b64decode(content.split(',')[1]))
    # options = [{'label': filename, 'value': filename} for filename in listdir('CVs')]
    return contents#, options, options

@app.callback(
    Output('upload-files-fp', 'contents'),
    # Output('dropdown-fp', 'options'),
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
                file.write(base64.b64decode(content.split(',')[1]))
    # options = [{'label': filename, 'value': filename} for filename in listdir('FPs')]
    return contents#, options, options

    
@app.callback(
    Output('start-working', 'children'),
    Output('finised-working', 'children'),
    Output('graphs', 'children'),
    Input('start-working', 'n_clicks'),
    State('dropdown-cv', 'value'),
    State('dropdown-fp', 'value'),

)
def check_dropdown_values(n_clicks, cvs, fps):
    # print(cvs, fps)
    if n_clicks and cvs and fps:
        results = []
        if cvs > fps:
            for FP in fps:
                FP_path = path.join('FPs', FP)
                FP_subtitles, FP_keywords = logic_attribution(FP_path)
                for CV in cvs:
                    # if (CV and FP) and (CV != FP):
                    CV_path = path.join('CVs', CV)
                    CV_subtitles, CV_keywords = logic_attribution(CV_path)
                    sub_cos_similarity, sub_jac_similarity, sub_lev_distance = get_similarite(CV_subtitles, FP_subtitles)
                    key_cos_similarity, key_jac_similarity, key_lev_distance = get_similarite(CV_keywords, FP_keywords)
                    print(CV, FP, sub_cos_similarity, sub_jac_similarity, sub_lev_distance, key_cos_similarity, key_jac_similarity, key_lev_distance)
                    results.append((CV, FP, sub_cos_similarity, sub_jac_similarity, sub_lev_distance, key_cos_similarity, key_jac_similarity, key_lev_distance))
        else:
            for CV in cvs:
                CV_path = path.join('CVs', CV)
                CV_subtitles, CV_keywords = logic_attribution(CV_path)
                for FP in fps:
                    # if (CV and FP) and (CV != FP):
                    FP_path = path.join('FPs', FP)
                    FP_subtitles, FP_keywords = logic_attribution(FP_path)
                    sub_cos_similarity, sub_jac_similarity, sub_lev_distance = get_similarite(CV_subtitles, FP_subtitles)
                    key_cos_similarity, key_jac_similarity, key_lev_distance = get_similarite(CV_keywords, FP_keywords)
                    print(CV, FP, sub_cos_similarity, sub_jac_similarity, sub_lev_distance, key_cos_similarity, key_jac_similarity, key_lev_distance)
                    results.append((CV, FP, sub_cos_similarity, sub_jac_similarity, sub_lev_distance, key_cos_similarity, key_jac_similarity, key_lev_distance))

            master_div = []
            test_dict = {
                "CV": [],
                "FP": [],
                "Similarité de Jaccard": [],
                "Distance de Levenshtein": [],
                "Similarité du cosinus": [],

            }
            for (CV, FP, sub_cos_similarity, sub_jac_similarity, sub_lev_distance, key_cos_similarity, key_jac_similarity, key_lev_distance) in results:
                master_div.append(html.Div(f'Similarité du CV {CV} avec la fiche de poste {FP}'))
                master_div.append(html.Div(f"Similarité du cosinus des sous-titres: {sub_cos_similarity}"))
                master_div.append(html.Div(f"Similarité de Jaccard des sous-titres: {sub_jac_similarity}"))
                master_div.append(html.Div(f"Distance de Levenshtein des sous-titres:{sub_lev_distance}"))
                master_div.append(html.Div(f"Similarité du cosinus des mots-clés: {key_cos_similarity}"))
                master_div.append(html.Div(f"Similarité de Jaccard des mots-clés: {key_jac_similarity}"))
                master_div.append(html.Div(f"Distance de Levenshtein des mots-clés: {key_lev_distance}"))
                master_div.append(html.Br())
                master_div.append(html.Br())
            
                test_dict["CV"].append(CV)
                test_dict["FP"].append(FP)
                test_dict["Similarité de Jaccard"].append(sub_jac_similarity)
                test_dict["Distance de Levenshtein"].append(sub_lev_distance)
                test_dict["Similarité du cosinus"].append(sub_cos_similarity)

            pd.DataFrame().from_dict(test_dict).to_excel("test.xlsx")

            return "Traitement terminé", "", dbc.Row(
                    [
                        html.Div("La Similarité du cosinus mesure la similarité entre deux textes. Plus elle est élevée, plus les textes sont similaires."), 
                        html.Div("La distance de Jaccard mesure la dissimilarité entre deux ensembles de tokens. Plus elle est faible, plus les textes sont similaires."), 
                        html.Div("La distance de Levenshtein mesure le nombre de modifications nécessaires pour transformer un texte en un autre. Plus elle est faible, plus les textes sont similaires."),
                        html.Br(),
                        html.Div(master_div),
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
    app.run_server(debug=True, port=8081)
