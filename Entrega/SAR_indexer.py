# Cardona Lorenzo, Victor
# Gavilán Gil, Marc
# Martínez Bernia, Javier
# Murcia Serrano, Andrea

######      Indexer      ######
# Extrae las noticias de una
# colección de documentos alojados
# en un directorio, las indexa y
# guarda en disco los índices creados

import sys
import ALT_library as altL
import os
import pprint
import json
import re
import pickle


def syntax():
    print("argumentos <coleccion dir> <fichero indice>")
    exit(1)


def indexarCuerpo(directorioInicio):
    """ Devuelve una tupla con (IndiceInvertido, DiccionarioDocumentos, idsNoticias, IndicesStemming) """

    indiceInvertidoArticle = {}
    indiceInvertidoTitle = {}
    indiceInvertidoSummary = {}
    indiceInvertidoKeywords = {}
    indiceInvertidoDate = {}
    indices = {}
    tries = {}
    diccionarioDocumentos = {}

    articleString = ""
    titleString = ""
    summaryString = ""
    keywordsString = ""
    dateString = ""

    idsNoticias = []
    nNoticias = 0
    numeroDocumento = 0

    for dirName, _, fileList in os.walk(directorioInicio):
        for fname in fileList:
            numeroNoticia = 0
            rel_file = os.path.join(dirName, fname)
            with open(rel_file, 'r') as json_file:
                data = json.load(json_file)

            for i in range(len(data)):
                nNoticias += 1
                idNoticia = (numeroDocumento, numeroNoticia)
                idsNoticias.append(idNoticia)
                diccionarioDocumentos[idNoticia] = (rel_file, numeroNoticia)
                numeroNoticia = numeroNoticia+1
                er = re.compile(r'\w+')

                articleString += data[i]['article']
                titleString += data[i]['title']
                summaryString += data[i]['summary']
                keywordsString += data[i]['keywords']
                dateString += data[i]['date']

                for word in er.findall(str(data[i]['article'])):

                    indiceInvertidoArticle.setdefault(word.lower(), [])
                    indiceInvertidoArticle[word.lower()] = list(set().union(
                        indiceInvertidoArticle[word.lower()], [idNoticia]))

                for word in er.findall(str(data[i]['title'])):
                    indiceInvertidoTitle.setdefault(word.lower(), [])
                    indiceInvertidoTitle[word.lower()] = list(set().union(
                        indiceInvertidoTitle[word.lower()], [idNoticia]))

                for word in er.findall(str(data[i]['summary'])):
                    indiceInvertidoSummary.setdefault(word.lower(), [])
                    indiceInvertidoSummary[word.lower()] = list(set().union(
                        indiceInvertidoSummary[word.lower()], [idNoticia]))

                for word in er.findall(str(data[i]['keywords'])):
                    indiceInvertidoKeywords.setdefault(word.lower(), [])
                    indiceInvertidoKeywords[word.lower()] = list(set().union(
                        indiceInvertidoKeywords[word.lower()], [idNoticia]))

                for word in data[i]['date'].split():
                    indiceInvertidoDate.setdefault(word.lower(), [])
                    indiceInvertidoDate[word.lower()] = list(set().union(
                        indiceInvertidoDate[word.lower()], [idNoticia]))

            numeroDocumento = numeroDocumento+1

    indices["article"] = indiceInvertidoArticle
    indices["title"] = indiceInvertidoTitle
    indices["summary"] = indiceInvertidoSummary
    indices["keywords"] = indiceInvertidoKeywords
    indices["date"] = indiceInvertidoDate

    tries["article"] = altL.generarTrie(articleString)
    tries["title"] = altL.generarTrie(titleString)
    tries["summary"] = altL.generarTrie(summaryString)
    tries["keywords"] = altL.generarTrie(keywordsString)
    tries["date"] = altL.generarTrie(dateString)

    return (indices, diccionarioDocumentos, idsNoticias, tries)


if __name__ == "__main__":
    directorioColeccion = ""
    ficheroIndice = ""
    if len(sys.argv) != 3:
        syntax()

    directorioColeccion = sys.argv[1]
    ficheroIndice = sys.argv[2]

    pickle.dump(indexarCuerpo(directorioColeccion),
                open(ficheroIndice, "wb"))
