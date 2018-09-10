import urllib3
from bs4 import BeautifulSoup
##url = "https://www.cnn.com"
##http = urllib3.PoolManager()
##response = http.request('GET', url)
##soup = BeautifulSoup(response.data)
##for link in soup.find_all('a'):
##    print(link.get('href'))
class WebsiteCrawler:
    def __init__(self, url):
        self.center = url
        http = urllib3.PoolManager()
        response = http.request('GET', url)
        self.soup = BeautifulSoup(response.data)
        self.externallinks = {}
##    def __eq__(self, other):
##        
##        @staticmethod
##        def list_cleaner(ls):
##            new_map = {}
##            for obj in ls:
##                if obj not in new_map:
##                    new_map[obj] = WebsiteCrawler(obj)
                
    def get_all_links(self):
        alllinks = []
        for link in self.soup.find_all('a'):
            if ".com" not in link.get('href') and  ".it" not in link.get('href'):
                alllinks.append("https://cnn.com"
                                          + link.get('href'))
                
            else:
                alllinks.append(link.get('href'))
        return alllinks
                 
                    
