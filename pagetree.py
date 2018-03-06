import wikipedia #need to run $ pip install wikipedia
import string
from wiki_functions import summary_links
from wiki_functions import key_links
from collections import OrderedDict


class PageTree:
    """a tree of wikipedia pages based on links
    attributes: title, summary_links"""

    def __init__(self, title, links = None):
        """creates a PageTree objects with a title (the title of the page), and
            links, the default value being None
                title: string of page title
                links: list containing links from page"""
        self.title = title
        self.links = links

    def __str__(self):
        """prints all of the links withing a PageTree and all the links within
            each of its links"""
        if self.links == None:
            return self.title

        else:
            res = ''
            for link in self.links:
                res += '\n' + PageTree.__str__(link)
            return res

    def get_summary_links(self, num_links = 3):
        """finds the links in the summary paragraph of the wikipedia page of a
            PageTree and makes a list 'links' with 'num_links' number of links in it
            num_links: number of links to put in self.links"""
        summary = summary_links(self.title)
        links = []
        for link in summary:
            links.append(PageTree(link))
        self.links = links[:num_links]

    def get_key_links(self, num_links = 3):
        """returns a list containing a list with the num_links page trees containing
            the links which occur most in the article's histogram
            num_links: number of links to put in self.links"""
        keys = key_links(self.title)
        links = []
        for link in keys:
            links.append(PageTree(link))
        self.links = links[:num_links]


    def dive(self, num_links = 3):
        """gets the the key links of a PageTree, their key links, and their key links
            num_links: number of key links gotten at each step (gets passed in to
            get_key_links)"""
        self.get_key_links(num_links)
        for branch in self.links:
            branch.get_key_links(num_links)
            for link in branch.links:
                link.get_key_links(num_links)


    def summary_dive(self, num_links = 2):
        """gets the the summary links of a PageTree, their summary links,
            and summary key links num_links: number of summary links gotten at
            each step
            num_links: the number of links gotten at each step (gets passed in
            get_summary_links)"""
        self.get_summary_links(num_links)
        for branch in self.links:
            branch.get_summary_links(num_links)
            for link in branch.links:
                link.get_summary_links(num_links)

    def internals(self):
        """returns a list containing all of the titles of a tree of wikipedia pages_to_view
        branching from the outermost PageTree"""

        if self.links == None:
            return [self.title]

        else:
            res = []
            for link in self.links:
                res.extend(PageTree.internals(link))
            return res
    def output(self):
        """returns a string containing titles and summaries of a PageTree of wikipedia
            articles with repeats removed formatted in htlm markup"""

        pages_to_view = [self.title]
        for i in range(len(self.links)):
            pages_to_view.append(self.links[i].title)
        pages_to_view += self.internals()

        pages_to_view.reverse()
        pages_to_view = list(OrderedDict.fromkeys(pages_to_view))

        summaries_string = ''
        for link in pages_to_view:
            page = wikipedia.page(link)
            summaries_string += '<p>' '\n' + page.title.upper() + '<br>' '\n' + page.summary + '\n' + '</p>'
        return summaries_string
