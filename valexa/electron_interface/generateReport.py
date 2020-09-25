import json
from kaleido.scopes.plotly import PlotlyScope
import plotly.graph_objects as go

def generate(**data):
    commands = {
        "\\COMPOUNDname": data['compound_name'],
        "\\DATAcalibration": createTabular(data['calibration_data']), #serie, level, x, y
        "\\DATAvalidation": createTabular(data['validation_data']),
        "\\GRAPHcompound": "DATAvalidation"  #TODO
    }


    ## Fichier Paragraphe Profile
    fIn = open("filesTex/TemplateProfileParagraph.tex", 'r')
    fOut = open("filesTex/Profile_" + data['compound_name'] + str(data['id']) + ".tex", 'w')
    for line in fIn:
        for cle, val in commands.items():
            line = line.replace(cle, val)
        fOut.write(line)
    fIn.close()
    fOut.close()

    ## Fichier listing des profiles
    f = open('filesTex/ListParagraphsProfile.tex', 'a')
    f.write("\\input{ParagraphsProfile/Profile_" + data['compound_name'] + str(data['id']) + "}\n")
    f.close()


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


