import json
from pylatex import Document, Tabular, Math,  Axis, Plot, Figure, Matrix
from pylatex.base_classes.command import Command, CommandBase, Options, Arguments
from re import sub


def generate(**data):
    print(json.dumps({"type": "IN GENERATE", "data": data['id']}))


    checkWords = ("\\COMPOUDname", "\\DATAcalibration")
    repWords = (data['compound_name'], str(data['id']))

    fIn = open('ProfilesParagraphIN.tex', 'r')
    fOut = open('ProfilesParagraphOUT.tex', 'w')

    for line in fIn:
        for check, rep in zip(checkWords, repWords):
            line = line.replace(check, rep)
        fOut.write(line)
    fIn.close()
    fOut.close()