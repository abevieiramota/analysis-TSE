# -*- encoding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib2
import urlparse
import os
import zipfile

def extract_pages(url):

    visited_pages = set()
    to_visit_pages = set([url])
    to_download = set()

    while to_visit_pages:

        top_url = to_visit_pages.pop()
        print 'visitando {}'.format(top_url)

        try:
            page = urllib2.urlopen(top_url)
        except urllib2.HTTPError:
            print 'não foi possível acessar a url {}'.format(top_url)

        page_content = page.read()
        page.close()

        soup = BeautifulSoup(page_content)
        hrefs = (a['href'] for a in soup.findAll('a', href=True))
        urls = set([get_full_url(top_url, href) for href in hrefs])

        for url in urls:

            if url.endswith('.html') and not url in visited_pages and url != top_url:

                to_visit_pages.add(url)
            elif url.endswith('.zip'):

                to_download.add(url)

        visited_pages.add(top_url)

    # salvar as urls dos .zip num arquivo para analisar
    print 'total de urls de download {}'.format(len(to_download))
    f = open('download.txt', 'w')
    f.write('\n'.join(to_download))
    f.close()
    for download_url in to_download:

        print 'baixando {}'.format(download_url)
        download_zip(download_url)

def get_full_url(top_url, href):

    return urlparse.urljoin(top_url, href)
    if not href.startswith('/'):
        base = top_url.rpartition('/')[0]

        return '{}/{}'.format(base, href)
    else:
        return href

def download_zip(url):

    try:
        url_opened = urllib2.urlopen(url)
    except urllib2.HTTPError:
        print 'não foi possível baixar o zip {}'.format(url)
        raise
    content = url_opened.read()
    url_opened.close()

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

    path_wt_zip = zip_path.rpartition('.')[0]
    os.makedirs(path_wt_zip)

    ziped = zipfile.ZipFile(zip_path)
    ziped.extractall(path=path_wt_zip)
    ziped.close()



if __name__ == '__main__':

    extract_pages('http://www.tse.jus.br/hotSites/pesquisas-eleitorais/index.html')
