# -*- encoding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib2
import urlparse
import os
import zipfile
import socket

PAGE_REQUEST_TIMEOUT = 60 # um minuto
DOWNLOAD_REQUEST_TIMEOUT = 60 # 10 minutos

def extract_pages(url):

    visited_pages = set()
    to_visit_pages = set([url])
    to_download = set()

    while to_visit_pages:

        top_url = to_visit_pages.pop()
        print '*visitando {}'.format(top_url)

        try:
            page_content = read_url(top_url, PAGE_REQUEST_TIMEOUT)
        except Exception:
            # adiciona novamente ao conjunto e tenta novamente?
            to_visit_pages.add(top_url)

        soup = BeautifulSoup(page_content)
        hrefs = (a['href'] for a in soup.findAll('a', href=True))
        urls = set([get_full_url(top_url, href) for href in hrefs])

        for url in urls:

            if url.endswith('.html') and not url in visited_pages and url != top_url:

                to_visit_pages.add(url)
            elif url.endswith('.zip'):

                to_download.add(url)

        visited_pages.add(top_url)

    f = open('download.txt', 'w')
    f.write('\n'.join(to_download))
    f.close()

    downloaded = []
    not_downloaded = []
    for download_url in to_download:

        try:
            download_zip(download_url)
        except urllib2.URLError:
            print "erro ao baixar {}".format(download_url)
            not_downloaded.append(download_url)
        except socket.timeout:
            print "timeout ao baixar {}".format(download_url)
            not_downloaded.append(download_url)
        else:
            downloaded.append(download_url)

    # loga zips baixados
    f = open('downloaded.txt', 'w')
    f.write('\n'.join(downloaded))
    f.close()
    # loga zips não baixados

    f = open('not_downloaded.txt', 'w')
    f.write('\n'.join(not_downloaded))
    f.close()

def get_full_url(top_url, href):

    return urlparse.urljoin(top_url, href)

def download_zip(url):

    print '#baixando {}'.format(url)
    content = read_url(url, DOWNLOAD_REQUEST_TIMEOUT)
    print "#baixado {}".format(url)

    parsed_url = urlparse.urlparse(url)
    dir_path = parsed_url.path.rpartition('/')[0][1:]
    zip_path = parsed_url.path[1:]
    # cria diretório
    if not os.path.exists(dir_path):

        os.makedirs(dir_path)

    # salva conteúdo
    zip_file = open(zip_path, 'w')
    zip_file.write(content)
    zip_file.close()

    # extrai
    print '@extraindo'
    path_wt_zip = zip_path.rpartition('.')[0]
    os.makedirs(path_wt_zip)

    ziped = zipfile.ZipFile(zip_path)
    ziped.extractall(path=path_wt_zip)
    ziped.close()
    print '@extraido'

def read_url(url, timeout):

    try:
        page = urllib2.urlopen(url, timeout=timeout)
        page_content = page.read()
    except urllib2.HTTPError as e:
        print "HTTPError: {} ({})".format(url, e.code)
        raise
    except urllib2.URLError as e:
        print "URLError: {} ({})".format(url, e.reason)
        raise
    except socket.timeout:
        print "timeout: {} time: {}".format(url, timeout)
        raise
    else:
        return page_content

if __name__ == '__main__':

    extract_pages('http://www.tse.jus.br/hotSites/pesquisas-eleitorais/index.html')
