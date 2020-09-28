import json
from kaleido.scopes.plotly import PlotlyScope
import plotly.graph_objects as go
from zipfile import ZipFile
import os


###   MAIN   ###
def generate(**data):
    idProfile = data['compound_name'] + str(data['id'])

    createGraphs(id=idProfile,
                 data=data['graphs']['profile']['data'],
                 layout=data['graphs']['profile']['layout'])
    commands = {
        "\\COMPOUNDname": data['compound_name'],
        "\\DATAcalibration": createTabular(data['calibration_data']), #serie, level, x, y
        "\\DATAvalidation": createTabular(data['validation_data']),
        "\\GRAPHcompound": "\\fbox{\\includegraphics[width=150mm]{profiles/fig_" + idProfile + "}}"
    }


    ## Fichier Paragraphe Profile
    fIn = open("filesTex/TemplateProfileParagraph.tex", 'r')
    fOut = open("filesTex/profiles/Profile_" + idProfile + ".tex", 'w')
    for line in fIn:
        for cle, val in commands.items():
            line = line.replace(cle, val)
        fOut.write(line)
    fIn.close()
    fOut.close()

    ## Fichier listing des profiles
    f = open('filesTex/ListParagraphsProfile.tex', 'a')
    f.write("\\input{profiles/Profile_" + idProfile + "}\n")
    f.close()


def createZip():
    # create zipfile
    file_paths = []
    for root, directories, files in os.walk('filesTex/'):
        for filename in files:
            # join the two strings in order to form the full filepath.
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)
    file_paths.remove('filesTex/TemplateProfileParagraph.tex')
    dirDownloads = os.path.join(os.path.expanduser("~"), "Downloads")
    with ZipFile(dirDownloads+'/FichiersTEX.zip', 'w') as zip:
        for file in file_paths:
            zip.write(file)


 ###   METHODES   ###
def createTabular(listData):
    """
    Create lines of the {tabular} object in .tex
    """
    line = ""
    for d in listData:
        d = {str(key): str(round(val, 3)) if isinstance(val, float) else str(val) for key, val in d.items()}  # convert values into str
        line += " & ".join(d.values())
        line += " \\\\\n"
    return line


def createGraphs(id, data, layout):  #data=list, layout=dict
    """
    Create .png with graphs from the Profile vue
    """
    layout['title']['x'] = 0.5
    layout['title']['y'] = 0.92
    layout['legend']['x'] = 0.9
    layout['legend']['y'] = 1
    scope = PlotlyScope()
    fig = go.Figure(data=data, layout=layout)
    with open("filesTex/profiles/fig_" + id + ".png", "wb") as f:
        f.write(scope.transform(fig, format="png"))
