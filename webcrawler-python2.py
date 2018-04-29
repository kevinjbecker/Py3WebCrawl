from __future__ import print_function
import httplib2
from bs4 import BeautifulSoup, SoupStrainer
import sys

class Crawler:
    def __init__(self, url):
        self.u = url

def main():
    print(sys.version)
    return None
    # prompts for URL
    url = raw_input("Enter url to scan: ")
    # alerts we are about to begin
    print("Beginning scan on \'%s\'.\n\tsetting up contexts..." % (url), end='')
    sys.stdout.flush()
    # used to silence SSL errors
    context = ssl._create_unverified_context()
    # sets up the parser
    print("parser...", end='')
    sys.stdout.flush()
    crawler = Crawler(url)
    print("done")

def web_crawler(initial_url, initial_domain, csv_dump_location):
    #print 'Running closed-domain crawl on all URLs beginning at', initial_url
    RETRIEVED_URLS = []
    SCANNED_URLS = []
    DUPLICATES = 0
    RETRIEVED_URLS.append(initial_url)
    pages_scanned = 0
    error_count = 0
    for url in RETRIEVED_URLS:
        has_append = False
        pages_scanned += 1
        urls_found = []
        # starts looping until all of the retrieved URLs have been gotten
        # lets the user know which URL is being read
        try:
            # initializaes http to an httplib2.Http() object
            http = httplib2.Http(disable_ssl_certificate_validation=True)
            # sets status and response to the http request of the URL
            status, response = http.request(url)

            # gets the domain so we don't escape RIT
            parsed_uri = urlparse(url)
            uri = parsed_uri
            domain = uri.netloc.lower()
            # end domain get
            count = 0
            # runs through the page using a list given back from BeautifulSoup looking for anchor tags (<a href = 'something'>text</a>
            for link in BeautifulSoup(response, 'html.parser', parse_only=SoupStrainer('a')):
                # if the link (temp element in for loop) has href (so anchor tag), and its actually a direct link
                if link.has_attr('href'):
                    if len(link['href']) > 0 and link['href'][0] == '/':
                        link['href'] = url[0:url.rfind('/')] + link['href']
                    if len(link['href']) > 0 and link['href'][0:4] == 'http':
                        # gets the domain so we don't escape RIT
                        parsed_uri = urlparse(link['href'])
                        uri = parsed_uri
                        domain = uri.netloc.lower()
                        # end domain get
                        try:
                            if domain[domain.index('.')+1:] == initial_domain:
                                urls_found.append(link['href'])
                                # sleep(.5)
                                # use to tell if if the URL has not been retrived before
                                retrieved_index = 0
                                try:
                                    # print (link['href'])
                                    # checks RETRIEVED_URLS to see if there's an index for the current link
                                    retrieved_index = RETRIEVED_URLS.index(link['href'])
                                except ValueError:
                                    # if a ValueError is thrown that means the item doesn't exist and we can set it to -1
                                    retrieved_index = -1

                                if retrieved_index == -1:
                                    count += 1
                                    # if retrieved_index is -1 we can add it to RETRIEVED_URLS
                                    RETRIEVED_URLS.append(link['href'])
                                else:
                                    # if site is a duplicate, mark it as so so we can keep that metric as well
                                    DUPLICATES += 1
                        except ValueError:
                            error_count += 1
                            #print error_count, ': An invalid URL has been found. URL is: ', link['href']
        except httplib2.RedirectLimit:
            error_count += 1
            #print error_count, ': Redirect limit was hit for URL: ', url
            to_append = [url, ['This URL redirected too many times.']]
            has_append = True
        except httplib2.httplib.ResponseNotReady:
            error_count += 1
            #print error_count, ': Response not ready for URL: ', url
            to_append = [url, ['Page took too long to load.']]
            has_append = True
        except KeyboardInterrupt:
            #print "KEYBOARD INTERRUPT HAS BEEN INITIATED, BREAKING..."
            break
        except:
            error_count += 1
            to_append = [url, ['An unknown error with this URL occured']]
            has_append = True

        if not has_append:
            to_append = [url, urls_found]

        with open(csv_dump_location, 'a') as text_file:
            print>>text_file, to_append

        to_append = []


if __name__ == "__main__":
    main()
