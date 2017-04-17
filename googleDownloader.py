#!/usr/bin/python3
#
# This program does a Google search for "quick and dirty" and returns
# 50 results.
#
import optparse
import sys
import requests
import re
import urllib.request
from bs4 import BeautifulSoup
from multiprocessing import Queue
import threading
import logging
import ssl

class Downloader(threading.Thread):
    def __init__(self, queue):
        super(Downloader, self).__init__()
        self.queue = queue

    def run(self):
        while True:
            download_url, save_as = queue.get()
            # sentinal
            if not download_url:
                return
            try:
                urllib.request.urlretrieve(download_url, filename=save_as)
            except Exception as e:
                logging.warning("error downloading %s: %s" % (download_url, e))

def main():
    #URL = 'http://google.com/search?q=%(query)s&num=%(count)s&start=%(startindex)s'
    ssl._create_default_https_context = ssl._create_unverified_context
    page = requests.get("http://google.com/search?q=species+latitude+longitude+sample%20filetype%3Axls&num=300&start=1")
    soup = BeautifulSoup(page.content)
    links = soup.findAll("a")

    for i in range(5):
		    threads.append(Downloader(queue))
		    threads[-1].start()

    for link in soup.find_all("a",href=re.compile("(?<=/url\?q=)(htt.*://.*)")):
        link_href = (re.split(":(?=http)",link["href"].replace("/url?q=","")))
        url = link_href[0].split("&")[0]
        if url.endswith("xls"):
            #print(url)
            filename = url.split('/')[-1]
            print(filename)
            queue.put((url, filename))
            #urllib.request.urlretrieve(principal)


    # if we get here, stdin has gotten the ^D
    print("Finishing current downloads... Please wait.")
    for i in range(5):
	    queue.put((None, None))


if __name__ == "__main__":
    queue = Queue()
    threads = []
    main()
    print("Fim!")
