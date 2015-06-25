# -*- encoding: utf-8 -*-
import urllib2
import os
import zipfile

DADOS_DIR = 'dados'
ANOS_ELEICOES = [1945, 1947, 1950, 1954, 1955, 1958, 1960, 1962, 1965, 1966, 1970, 1974, 1978, 1982, 1986, 1989, 1990, 1994, 1996, 1998, 2000, 2002, 2004, 2006, 2008, 2010, 2012, 2014]

ELEITORADO = {
'url_base': "http://agencia.tse.jus.br/estatistica/sead/odsele/perfil_eleitorado/perfil_eleitorado_%(ano)d.zip",
'adicionais': ['http://agencia.tse.jus.br/estatistica/sead/odsele/perfil_eleitorado/perfil_eleitorado_ATUAL.zip'],
              'folder_name': 'eleitorado' }

CANDIDATOS = {'url_base': "http://agencia.tse.jus.br/estatistica/sead/odsele/consulta_cand/consulta_cand_%(ano)d.zip",
              'folder_name': 'candidatos'}

CANDIDATOS_BENS = {'url_base': 'http://agencia.tse.jus.br/estatistica/sead/odsele/bem_candidato/bem_candidato_%(ano)d.zip',
              'folder_name': 'candidatos_bens'}

CANDIDATOS_LEGENDAS = {'url_base': "http://agencia.tse.jus.br/estatistica/sead/odsele/consulta_legendas/consulta_legendas_%(ano)d.zip",
                       'folder_name': 'candidatos_legendas' }

CANDIDATOS_VAGAS = {'url_base': "http://agencia.tse.jus.br/estatistica/sead/odsele/consulta_vagas/consulta_vagas_%(ano)d.zip",
                    'folder_name': 'candidatos_vagas'
                    }

RESULTADOS_APURACAO = {'url_base': "http://agencia.tse.jus.br/estatistica/sead/odsele/detalhe_votacao_uf/detalhe_votacao_uf_%(ano)d.zip",
                       'folder_name': 'resultados_apuracao'}

RESULTADOS_VOTACAO_NOMINAL = {'url_base': "http://agencia.tse.jus.br/estatistica/sead/odsele/votacao_candidato_uf/votacao_candidato_uf_%(ano)d.zip",
                              'folder_name': 'resultados_votacao_nominal'}

RESULTADOS_VOTACAO_PARTIDO = {'url_base': "http://agencia.tse.jus.br/estatistica/sead/odsele/votacao_partido_uf/votacao_partido_uf_%(ano)d.zip",
                              'folder_name': 'resultados_votacao_partido'}

PRESTACAO_CONTAS = {'url_base': "http://agencia.tse.jus.br/estatistica/sead/odsele/prestacao_contas/prestacao_contas_%(ano)d.zip",
                    'folder_name': 'prestacao_contas',
                    'adicionais': ["http://agencia.tse.jus.br/estatistica/sead/odsele/prestacao_contas/prestacao_final_2012.zip",
                                   "http://agencia.tse.jus.br/estatistica/sead/odsele/prestacao_contas/segunda_parcial_2012.zip",
                                   "http://agencia.tse.jus.br/estatistica/sead/odsele/prestacao_contas/primeira_parcial_2012.zip"]
                    }


TO_DOWNLOAD = [CANDIDATOS_VAGAS, ELEITORADO, CANDIDATOS, CANDIDATOS_BENS, CANDIDATOS_LEGENDAS, RESULTADOS_APURACAO, RESULTADOS_VOTACAO_NOMINAL, RESULTADOS_VOTACAO_PARTIDO, PRESTACAO_CONTAS]

def _TSEDownload(url_base, folder_path, passo=None, adicionais=None, **kwargs):
    """Realiza o download das páginas
    i) formadas pelo padrão
    url_base % {'ano': ano}, onde ano é um dos anos de eleição
    ii) contidas na lista 'adicionais'"""

    if not adicionais:
        adicionais = []

    url_anos = [url_base % {'ano': ano} for ano in ANOS_ELEICOES]

    urls_download = url_anos + adicionais

    for url in urls_download:

        try:
            _download_extract(url, folder_path)
        except urllib2.HTTPError:
            print 'Não foi possível fazer o download de %s' % url

def _download_extract(url, folder_path):

    filename = url.rpartition('/')[2]

    try:
        url_opened = urllib2.urlopen(url)
        content = url_opened.read()
    except urllib2.HTTPError:
        print 'Não foi possível fazer o download de %s' % url
        raise
    else:
        url_opened.close()

    filepath = os.path.join(folder_path, filename)

    f = open(filepath, 'w')
    f.write(content)
    f.close()

    file_folder = os.path.join(folder_path, filename.partition('.')[0])
    os.makedirs(file_folder)

    ziped = zipfile.ZipFile(filepath)
    ziped.extractall(path=file_folder)
    ziped.close()

def _cria_folder(folder_name):

    folder_path = os.path.join(DADOS_DIR, folder_name)

    if not os.path.exists(folder_path):

        os.makedirs(folder_path)

    return folder_path


if __name__ == '__main__':


    for base in TO_DOWNLOAD:

        folder_path = _cria_folder(base['folder_name'])
        _TSEDownload(folder_path=folder_path, **base)
