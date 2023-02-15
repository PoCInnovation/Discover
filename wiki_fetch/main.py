# PoC Project 2023
# Discover

import wikipediaapi as wiki
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx

from Subject import Subject


def get_page_from_input():
    """Returns the page from the input"""
    name = input("Enter title of wikipedia page: ")
    page = wrapper.page(name)

    if (
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


wrapper = wiki.Wikipedia('en')

subject = Subject(get_page_from_input())
subject.fetch_is_keyword()
subject.fetch_other_subjects_from_eponymous_category()

relations = [
    {
        'source': subject.page.title,
        'target': x,
        'object': wrapper.page(x)
    }
    for x in subject.subjects]
df_relations = pd.DataFrame(relations)
G = nx.from_pandas_edgelist(df_relations)

plt.figure(figsize=(10, 10))
pos = nx.kamada_kawai_layout(G)
nx.draw(G, with_labels=True, node_color='skyblue', edge_cmap=plt.cm.Blues, pos=pos)
plt.show()
