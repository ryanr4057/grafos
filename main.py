import PySimpleGUI as sg
import networkx as nx
import matplotlib.pyplot as plt
import funcoes as f

num_vertices, num_arestas = f.criar_janela_input()

arestas = []
arestas_inseridas = set()
if num_arestas != None:
    for i in range(int(num_arestas)):
        v1, v2, peso = f.cria_janela_aresta(i)

        while f.verifica_aresta(arestas_inseridas, v1, v2) == False:
            v1, v2, peso = f.cria_janela_aresta(i)
        arestas_inseridas.add((v1, v2))
        arestas.append((v1, v2, peso))

    arvore_minima = f.algoritmo_kruskal(int(num_vertices), int(num_arestas), arestas)
    arestas_arvore_minima = [(u, v) for u, v, _ in arvore_minima]

    f.criar_janela_arvore(arestas, arvore_minima)


