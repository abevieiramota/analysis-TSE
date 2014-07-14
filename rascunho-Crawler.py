from bs4 import BeautifulSoup
import urllib2

def extract_pages(url):

    visited_pages = set()
    to_visit_pages = set([url])

    while to_visit_pages:

        top_url = to_visit_pages.pop()
        print 'visitando {}'.format(top_url)

        page = urllib2.urlopen(top_url)
        page_content = page.read()
        page.close()

        soup = BeautifulSoup(page_content)

        hrefs = [a['href'] for a in soup.findAll('a', href=True)]

        urls = set([get_full_url(top_url, href) for href in hrefs])

        for url in urls:

            if url.endswith('.html'):

                to_visit_pages.add(url)
            elif url.endswith('.zip'):

                download_zip(url)

        visited_pages.add(top_url)
    print visited_pages


def get_full_url(base, url):

    if not url.startswith('/'):

        return '{}/{}'.format(base, url)
    else:
        return url

def download_zip(url):
    pass

if __name__ == '__main__':

    extract_pages('http://www.tse.jus.br/hotSites/pesquisas-eleitorais/index.html')
