import sys
import gensim, logging
import networkx as nx
import matplotlib.pyplot as plt

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

def open_model (model):
    if model.endswith('.vec.gz'):
        model = gensim.models.KeyedVectors.load_word2vec_format(model, binary=False)
    elif model.endswith('.bin.gz'):
        model = gensim.models.KeyedVectors.load_word2vec_format(model, binary=True)
    else:
        model = gensim.models.KeyedVectors.load(model)
    model.init_sims(replace=True)
    return model

def create_nodes (words):
    graph = nx.Graph()
    graph.add_nodes_from(words)
    return graph

def create_edges (model, words, graph):
    i = -1
    while i < len(words)-1:
        i += 1
        if words[i] in model:
            j = i+1
            while j < len(words):
                if model.similarity (words[i], words[j]) > 0.5:
                    graph.add_edge(words[i], words[j])
                j += 1
    return graph

def visualisation (graph):
    pos=nx.spring_layout(graph)
    nx.draw_networkx_nodes(graph, pos, node_color='blue', node_size=50)
    nx.draw_networkx_edges(graph, pos, edge_color='yellow')
    nx.draw_networkx_labels(graph, pos, font_size=16, font_family='Arial')
    plt.axis('off')
    plt.show()
    return

def center (graph):
    deg = nx.degree_centrality(graph)
    n = len(graph.nodes())//5
    if n < 2:
        n = 2
    i = 0
    print (n, 'most central nodes:')
    for nodeid in sorted(deg, key=deg.get, reverse=True):
        i+=1
        print('№', i, '\t', nodeid)
        if i == n:
            break
    return

def radius (graph):
    try:
        print('radius:\t', nx.radius(graph))
    except nx.exception.NetworkXError:
        print('graph is not connected')
    return

def clustering (graph):
    print('clustering:\t', nx.average_clustering(graph))
    return
    
model = 'ruscorpora_upos_skipgram_300_5_2018.vec.gz'
model = open_model (model)
words = ['кот_NOUN', 'кошка_NOUN', 'котенок_NOUN', 'кота_NOUN', 'котенка_NOUN', 'котяра_NOUN', 'мыш_NOUN', 'пес_NOUN', 'котище_NOUN', 'дворняга_NOUN', 'кошечка_NOUN', 'собака_NOUN', 'волкодав_NOUN', 'дворняга_NOUN', 'овчарка_NOUN', 'собачонка_NOUN', 'дворняжка_NOUN', 'кобель_NOUN', 'щенок_NOUN', 'сенбернар_NOUN', 'песятина_NOUN']
graph = create_nodes (words)
graph = create_edges(model, words, graph)
center (graph)
radius (graph)
clustering (graph)
visualisation (graph)
