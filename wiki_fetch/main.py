# PoC Project 2023
# Discover

import wikipediaapi as wiki
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
from neo4j import GraphDatabase

from Subject import Subject

from neo4j_driver import Neo4jConnection
import os.path as path
import re

conn = Neo4jConnection(uri="bolt://localhost:7687", user="superman", pwd="pizza")
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

subject = Subject(get_page_from_input(), wrapper)
subject.fetch_is_keyword(5)
subject.fetch_other_subjects_from_eponymous_category()

def dataframe_to_neo4j(df, subject, index):
    conn.add_word(subject.page.title)
    index = re.sub('[^A-zÀ-ÿ]', '_', index)
    for target in df["target"]:
        conn.add_word(target)
        conn.create_link(subject.page.title, target, index)
        # print(f"Added link from {subject.page.title} to {target}")

for index, value in subject.subjects.items():
    print(f"Index: {index}")
    if path.exists(f"relations_{subject.page.title}_{index}.csv"):
        # print(f"Found relations_{subject.page.title}_{index}.csv")
        df_relations = pd.read_csv(f"relations_{subject.page.title}_{index}.csv")
        dataframe_to_neo4j(df_relations, subject, index)
        continue
        
        
    
    relations = [
        {
            'source': subject.page.title,
            'target': x,
            'object': wrapper.page(x)
        }
        for x in value]
    df_relations = pd.DataFrame(relations)
    
    
    df_relations.to_csv(f"relations_{subject.page.title}_{index}.csv", index=False)
    dataframe_to_neo4j(df_relations, subject, index)

    # G = nx.from_pandas_edgelist(df_relations)

    # plt.figure(figsize=(10, 10))
    # pos = nx.kamada_kawai_layout(G)
    # nx.draw(G, with_labels=True, node_color='skyblue', edge_cmap=plt.cm.Blues, pos=pos)
    # plt.show()

