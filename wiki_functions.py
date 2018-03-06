import wikipedia #need to run $ pip install wikipedia
import string
from collections import OrderedDict


def first_link(title):
    """Finds the first link of an article and returns it
        title: title of wikipedia article to find link from"""

    links_in_summary = []
    link_dict = {}


    page = wikipedia.page(title)
    summary_string = page.summary.lower().replace('-',' ')
    summary_string = ''.join(i for i in summary_string if i not in string.punctuation)
    summary_list = summary_string.split()

    for i in range(len(summary_list)):
        summary_list[i] = summary_list[i].lower()

    links = page.links

    for i in range(len(links)):
        links[i] = links[i].lower()


    for link in links:
        no_punct = ''.join(i for i in link if i not in string.punctuation)
        if no_punct in summary_string and not no_punct in page.title.lower():
            links_in_summary.append(no_punct)

    for link in links_in_summary:
        if link.split()[0] in summary_list:
            flag = True
            position = summary_list.index(link.split()[0])
            for i in range(len(link.split())):
                if summary_list[position + i] != link.split()[i]:
                    flag = False
            if flag:
                link_dict[link] = position

        if  link.split()[0] + 's' in summary_list:
            position = summary_list.index(link.split()[0] + 's')
            link_dict[link] = position

    ordered_list = sorted(link_dict,key = link_dict.get)
    return ordered_list[0]

def summary_links(title):
    """Finds the first link of an article and returns it"""
    links_in_summary = []
    link_dict = {}


    page = wikipedia.page(title)
    summary_string = page.summary.lower().replace('-',' ')
    summary_string = ''.join(i for i in summary_string if i not in string.punctuation)
    summary_list = summary_string.split()

    for i in range(len(summary_list)):
        summary_list[i] = summary_list[i].lower()

    links = page.links

    for i in range(len(links)):
        links[i] = links[i].lower()


    for link in links:
        no_punct = ''.join(i for i in link if i not in string.punctuation)
        if no_punct in summary_string and not no_punct in page.title.lower():
            links_in_summary.append(no_punct)

    for link in links_in_summary:
        if link.split()[0] in summary_list:
            flag = True
            position = summary_list.index(link.split()[0])
            for i in range(len(link.split())):
                if summary_list[position + i] != link.split()[i]:
                    flag = False
            if flag:
                link_dict[link] = position

        if  link.split()[0] + 's' in summary_list:
            position = summary_list.index(link.split()[0] + 's')
            link_dict[link] = position

    ordered_list = sorted(link_dict,key = link_dict.get)
    return ordered_list

def key_links(title):
    d = dict()

    page = wikipedia.page(title)
    text = page.content.lower()
    links = page.links

    text_list = text.split()

    for i in range(len(links)):
        links[i] = links[i].lower()

    for word in text_list:
        d[word] = d.get(word,0) + 1

    ordered_words = sorted(d, key = d.get, reverse = True)


    res = []
    for word in ordered_words:
        if word in links:
            res.append(word)

    return res


def teach_me(start_page, depth):
    file_name = start_page + '.txt'
    current_page = wikipedia.page(start_page)
    out_file = open(file_name, 'w')
    pages = [current_page.title]

    output = current_page.summary
    for i in range(depth):
        current_title = first_link(current_page.title)
        print(current_title)
        current_page = wikipedia.page(current_title)
        pages.append(current_title)
    return pages


def wiki_distance(start, end):
    page = wikipedia.page(start)
    end_name = wikipedia.page(end).title

    visited = [page.title]
    count = 0
    while not end_name in page.title and count!= -1:

        link = first_link(visited[count])
        if link in visited:
            return -1
        print(link)
        visited.append(link)
        page = wikipedia.page(link)
        count +=1

    return count

def new_html(page, depth):
    tree = PageTree(page)
    text = tree.dive(depth)

    file_name = page + '.html'
    out_file = open(file_name, 'w')
