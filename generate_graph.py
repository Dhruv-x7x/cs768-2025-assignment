"""
Build and analyze the citation graph.
"""

import os
import argparse
import re
import networkx as nx
import matplotlib.pyplot as plt
from tqdm import tqdm
import random

def normalize(text):
    """
    Normalize text by removing non-alphanumeric chars and lowercasing.
    """
    return re.sub(r'\W+', '', text).lower()


def parse_bib_titles(bib_path):
    """
    Naively parse a .bib file to extract titles.
    """
    titles = []
    with open(bib_path, 'r', encoding='utf-8', errors='ignore') as f:
        text = f.read()
    # Split entries by '@'
    entries = text.split('@')[1:]
    for entry in entries:
        for line in entry.splitlines():
            if line.strip().lower().startswith('title'):
                parts = line.split('=', 1)
                if len(parts) == 2:
                    val = parts[1].strip().rstrip(',').strip()
                    # Remove enclosing braces
                    if val.startswith('{') and val.endswith('}'):
                        val = val[1:-1]
                    titles.append(val)
                break
    return titles


def main():
    parser = argparse.ArgumentParser(description="Build and analyze the citation graph.")
    parser.add_argument(
        '--dataset-path', type=str, required=True,
        help='Root folder containing all paper subdirectories.'
    )
    args = parser.parse_args()
    dataset_dir = args.dataset_path

    # Build title -> folder mapping
    title_map = {}
    print("Indexing paper titles...")
    for folder in os.listdir(dataset_dir):
        folder_path = os.path.join(dataset_dir, folder)
        if os.path.isdir(folder_path):
            title_file = os.path.join(folder_path, 'title.txt')
            if os.path.isfile(title_file):
                with open(title_file, 'r', encoding='utf-8', errors='ignore') as f:
                    title = f.read().strip()
                norm = normalize(title)
                title_map[norm] = folder

    # Initialize directed graph
    G = nx.DiGraph()
    G.add_nodes_from(title_map.values())

    # Parse bibliographies and add edges
    print("Parsing bibliographies and adding edges...")
    for folder in tqdm(title_map.values(), desc="Processing papers"):
        folder_path = os.path.join(dataset_dir, folder)
        # Look for .bib file
        bib_files = [f for f in os.listdir(folder_path) if f.endswith('.bib')]
        if bib_files:
            bib_path = os.path.join(folder_path, bib_files[0])
            cited_titles = parse_bib_titles(bib_path)
        else:
            cited_titles = []

        for cited in cited_titles:
            norm = normalize(cited)
            if norm in title_map:
                G.add_edge(folder, title_map[norm])

    # Compute metrics
    num_edges = G.number_of_edges()
    num_isolated = len(list(nx.isolates(G)))
    in_degs = [d for _, d in G.in_degree()]
    out_degs = [d for _, d in G.out_degree()]
    avg_in = sum(in_degs) / len(in_degs)
    avg_out = sum(out_degs) / len(out_degs)

    # Diameter: use largest connected component on undirected graph
    uG = G.to_undirected()
    comps = list(nx.connected_components(uG))
    largest = max(comps, key=len)
    subg = uG.subgraph(largest)
    diameter = nx.diameter(subg)

    # Output results
    print(f"Number of edges: {num_edges}")
    print(f"Number of isolated nodes: {num_isolated}")
    print(f"Average in-degree: {avg_in:.4f}")
    print(f"Average out-degree: {avg_out:.4f}")
    print(f"Diameter (largest CC): {diameter}")

    # Plot and save degree distribution histogram
    degrees = [d for _, d in uG.degree()]
    plt.figure(figsize=(10, 6))
    plt.hist(degrees, bins=50, color='skyblue', edgecolor='black')
    plt.title('Degree Distribution')
    plt.xlabel('Degree')
    plt.ylabel('Number of Nodes')
    plt.tight_layout()
    plt.savefig('degree_histogram.png')
    print("Saved degree histogram to degree_histogram.png")

if __name__ == '__main__':
    main()
