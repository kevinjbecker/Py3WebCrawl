# used to flush output streams
import sys
# used to silence ssl errors
import ssl
# used to read the HTML of destination
#import urllib.request
import requests
# used to strain resulting HTML
from bs4 import BeautifulSoup
# used to determine if absolute URL
from urllib.parse import urljoin, urlparse

from time import sleep


# WEB CRAWLER CLASS
class Crawler:
    def __init__(self, url):
        # sets a few fields in place
        print("Setting up crawler...setting attributes...", end='')
        # the start url
        self.u = url
        # the dictionary of visited URLs and their pointees
        self.visited = {}
        # a queue of URLs to visit
        self.to_visit = [self.u]
        # the number of errors encountered
        self.errs_encountered = 0
        ####
        # done setting up new object's attributes
        ####
        print("done.")

    def start(self):
        # set our location to the first in the list
        try:
            while len(self.to_visit) > 0:
                #print("visiting:", self.to_visit[0])
                # grabs our first URL to visit and pops it
                visiting = self.to_visit.pop(0)
                # sets up our first URL in the to_visit list
                response = requests.get(visiting)
                # sets up the pointee list from the current URL
                self.visited[visiting] = []
                # parses out all of the anchors
                for anchor in BeautifulSoup(response.text, 'html.parser').find_all('a'):
                    # if this anchor has an href (we don't care about JS triggers)
                    if anchor.has_attr('href'):
                        print(anchor['href'])
                        # creates a full URL if it isn't already absolute
                        absolute_url = get_absolute_url(self.u, anchor['href'])
                        # if we haven't already visited this URL
                        if absolute_url not in self.visited:
                            # adds to the to_visit list
                            self.to_visit = absolute_url
                            # adds to our pointing list for the visiting URL
                            self.visited[visitng].append(absolute_url)
                            print("added:", absolute_url)
        except:
            self.errs_encountered += 1


# determines if a url is absolute or relative
def absolute(url):
    return bool(urlparse(url).netloc)


# returns the absolute url
def get_absolute_url(base, dest):
    return urljoin(base, dest) if not absolute(dest) else dest


def main():
    # grabs URL from user
    url = input("Enter url to start crawl at: ")

    # sanitizes input
    if(url[0:4] != 'http'):
        print("Invalid URL supplied, assuming HTTP with no SSL.")
        url = 'http://' + url

    # sets up the crawler
    crawler = Crawler(url)

    # alerts we are about to begin
    print("Beginning crawl from \'%s\'." % (url))
    # waits for user to initiate the crawl
    input("To begin crawling, hit enter. ")
    # begins the crawling
    crawler.start()


def launch():
    # allows for a clear command to run
    from os import system as command
    # clears the screen before beginning
    command("clear")
    # unimports it, we are done with it
    del command

    # prints main screen
    print("##########################################################")
    print("#                       PY3 WebCrawl                     #")
    print("#                                                        #")
    print("# Authors:                                               #")
    print("# Kevin Becker <kjb2503@rit.edu>                         #")
    print("# Ben Champion <bwc3252@rit.edu>                         #")
    print("##########################################################")
    # launches main
    main()

if __name__ == "__main__":
    launch()
