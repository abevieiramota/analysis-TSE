# -*- encoding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib2
import urlparse
import os
import zipfile
import socket

CONFIG = dict(
    PAGE_REQUEST_TIMEOUT = 60,
    DOWNLOAD_REQUEST_TIMEOUT = 60
)

def extract_pages(url):

    visited_pages = set()
    to_visit_pages = set()
    to_download = set()

    to_visit_pages.add(url)

    while to_visit_pages:

        top_url = to_visit_pages.pop()
        print '*visitando {}'.format(top_url)

        try:
            html = read_url(top_url, timeout=CONFIG["PAGE_REQUEST_TIMEOUT"])
        except Exception:
            # adiciona novamente ao conjunto e tenta novamente?
            to_visit_pages.add(top_url)
            pass

        urls = extract_urls(top_url, html)

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
    zip_paths = []

    for download_url in to_download:

        print ">baixando {}".format(download_url)
        try:
            zip_path = download(download_url)
        except urllib2.URLError:
            print "erro ao baixar {}".format(download_url)
            not_downloaded.append(download_url)
        except socket.timeout:
            print "timeout ao baixar {}".format(download_url)
            not_downloaded.append(download_url)
        else:
            downloaded.append(download_url)
            zip_paths.append(zip_path)
            print ">baixado {}".format(download_url)

    # loga zips baixados
    f = open('downloaded.txt', 'w')
    f.write('\n'.join(downloaded))
    f.close()
    # loga zips não baixados

    f = open('not_downloaded.txt', 'w')
    f.write('\n'.join(not_downloaded))
    f.close()

    # unzipa
    for zip_path in zip_paths:

        unzip(zip_path)

def get_full_url(top_url, href):

    return urlparse.urljoin(top_url, href)

def extract_urls(url, html):

    soup = BeautifulSoup(html)
    hrefs = (a['href'] for a in soup.findAll('a', href=True))
    urls = set([get_full_url(url, href) for href in hrefs])

    return urls

def download(url):

    content = read_url(url, timeout=CONFIG["DOWNLOAD_REQUEST_TIMEOUT"])

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

    return zip_path

def unzip(zip_path):

    path_wt_zip = zip_path.rpartition('.')[0]
    os.makedirs(path_wt_zip)

    ziped = zipfile.ZipFile(zip_path)
    ziped.extractall(path=path_wt_zip)
    ziped.close()

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
