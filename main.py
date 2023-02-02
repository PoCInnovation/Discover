# PoC Project 2023
# Discover

import wikipediaapi as wiki
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
from nltk.tokenize import word_tokenize

def get_page_from_input():
    """Returns the page from the input"""
    name = input("Enter title of wikipedia page: ")
    page = wrapper.page(name)

    if  (
            "Category:All article disambiguation pages" in page.categories or
            "Category:All disambiguation pages" in page.categories or
            "Category:Disambiguation pages" in page.categories
        ):
        print("Your input is a little vague... please choose from the following:")
        for example in page.links:
            if "Talk:" in example:
                continue
            if "Python" in example:
                print(example)
        print()
        return get_page_from_input()

    if page.exists() is True:
        print(f"Found page {name} at {page.fullurl}")
        return page

    print(f"Page {name} does not exist")
    print()
    get_page_from_input()

def index_of(li, val, start):
    try:
        return li.index(val, start)
    except ValueError:
        return -1

class Subject():
    """Main class for subjects"""
    def __init__(self, page : wiki.WikipediaPage):
        self.page = page
        self.subjects = set()

    def fetch_other_subjects_from_eponymal_category(self):
        category_title = "Category:" + self.page.title
        if category_title not in self.page.categories:
            return
        eponymal_cateogry = self.page.categories[category_title]
        for member in eponymal_cateogry.categorymembers:
            self.subjects.add(member)

    def from_keyword_to_end_of_sentence(self, index, summary):
        """Returns the end of the sentence of the keyword"""
        keywords_indexes = [index_of(summary, x, index) for x in ".;:"]
        end = min(filter(lambda x: x != -1, keywords_indexes))

        return summary[(index + 1):(end)]

    def fetch_is_keyword(self):
        """Extracts pages which are linked
        following keywords such as 'is'"""
        keywords = ["is", "are", "was", "were"]
        sentences = []
        summary = word_tokenize(self.page.text)

        for index, word in enumerate(summary):
            if word in keywords:
                sentences.append(
                    self.from_keyword_to_end_of_sentence(index, summary)
                )

        for sentence in sentences:
            sentence_str = ' '.join(sentence).upper()
            for link in self.page.links:
                if sentence_str.find(link.upper()) != -1:
                    self.subjects.add(link)

wrapper = wiki.Wikipedia('en')

subject = Subject(get_page_from_input())
subject.fetch_is_keyword()
subject.fetch_other_subjects_from_eponymal_category()

relations = [
    {
        'source': subject.page.title,
        'target': x,
        'object': wrapper.page(x)
    }
    for x in subject.subjects]
df_relations = pd.DataFrame(relations)
G = nx.from_pandas_edgelist(df_relations)

plt.figure(figsize=(10,10))
pos = nx.kamada_kawai_layout(G)
nx.draw(G, with_labels=True, node_color='skyblue', edge_cmap=plt.cm.Blues, pos = pos)
plt.show()