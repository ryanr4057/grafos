import PySimpleGUI as sg
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

#cria a janela inicial, coletando o número de vértices e arestas
def criar_janela_input():
    layout = [[sg.Text('      ', background_color="#000000")],
            [sg.Text('NÚMERO DE VÉRTICES:', background_color="#000000", font=('gotham', 16, "bold"), text_color="#F7004F")],
            [sg.Text('      ', background_color="#000000")],
            [sg.InputText(key='-VERTICES-', font=('gotham', 20), background_color="#454041", text_color="#FFFFFF")],
            [sg.Text('      ', background_color="#000000")],
            [sg.Text('      ', background_color="#000000")],
            [sg.Text('NÚMERO DE ARESTAS:', background_color="#000000", font=('gotham', 16, "bold"), text_color="#F7004F")],
            [sg.Text('      ', background_color="#000000")],
            [sg.InputText(key='-ARESTAS-',  font=('gotham', 20), background_color="#454041", text_color="#FFFFFF")],
            [sg.Text('      ', background_color="#000000")],
            [sg.Text('      ', background_color="#000000")],
            [sg.Button('OK', size=10, font=('gotham', 15, "bold"), button_color= ("#FFFFFF","#F7004F" ))]]

    janela_1 = sg.Window('KRUSKAL', layout, size= (300, 400), background_color= "#000000" )
    evento, valores = janela_1.read()

    janela_1.close()

    return valores['-VERTICES-'], valores['-ARESTAS-']

#cria o grafo e a janela de exibição do grafo
def criar_janela_grafo(arestas, arestas_arvore):
    G = nx.Graph()
    G.add_weighted_edges_from(arestas)
    pos = nx.spring_layout(G)

    plt.figure(figsize=(8, 6))
    nx.draw_networkx_nodes(G, pos, node_color='#00C000', node_size=600,)
    nx.draw_networkx_labels(G, pos)
    labels = {(u, v): f"{int(peso)}" for (u, v, peso) in arestas}

    widths = [data['weight'] for _, _, data in G.edges(data=True)]
    scaled_widths = [(w - min(widths))/(max(widths) - min(widths)) for w in widths]
    scaled_widths = [w * 5 for w in scaled_widths]  # Ajuste o fator de escala conforme necessário

    nx.draw_networkx_edges(G, pos, edgelist=arestas, width=scaled_widths, alpha=0.5, edge_color='#000000')
    nx.draw_networkx_edges(G, pos, edgelist=arestas_arvore, width=3.5, alpha=0.8, edge_color='#008000')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_color='#000000', font_size=12)
    nx.draw_networkx_nodes(G, pos, node_color='#00C000', node_size=600,)
    nx.draw_networkx_labels(G, pos)

    plt.axis('off')
    plt.tight_layout()
    plt.show()

#função com o algoritmo kruskal
def algoritmo_kruskal(num_vertices, num_arestas, arestas):

    #função auxiliar do kruskal
    def encontrar_pai(pai, i):
        if pai[i] == i:
            return i
        return encontrar_pai(pai, pai[i])

    #função auxiliar do kruskal
    def unir_conjuntos(pai, rank, x, y):
        x_raiz = encontrar_pai(pai, x)
        y_raiz = encontrar_pai(pai, y)

        if rank[x_raiz] < rank[y_raiz]:
            pai[x_raiz] = y_raiz
        elif rank[x_raiz] > rank[y_raiz]:
            pai[y_raiz] = x_raiz
        else:
            pai[y_raiz] = x_raiz
            rank[x_raiz] += 1

    arestas = sorted(arestas, key=lambda x: x[2])
    arvore_geradora_minima = []
    pai = []
    rank = []

    for vertice in range(num_vertices):
        pai.append(vertice)
        rank.append(0)

    i = 0
    e = 0

    while e < num_vertices - 1:
        if i < len(arestas):
            u, v, peso = arestas[i]
            i += 1
            x = encontrar_pai(pai, u - 1)  # Subtrai 1 dos índices para ajustar a indexação
            y = encontrar_pai(pai, v - 1)  # Subtrai 1 dos índices para ajustar a indexação

            if x != y:
                e += 1
                arvore_geradora_minima.append((u, v, peso))
                unir_conjuntos(pai, rank, x, y)
        else:
            e += 1

    return arvore_geradora_minima

#cria a janela que exibe a árvore geradora minima
def criar_janela_arvore(arestas, arvore_minima):
    layout = [
        [sg.Text('      ', background_color="#000000")],
        [sg.Text('Árvore Geradora Mínima:',  background_color="#000000", font=('gotham', 16, "bold"), text_color="#F7004F")],
        [sg.Text('      ', background_color="#000000")],
        *[[sg.Text(f'Vértice {u} - Vértice {v}: Peso {peso}', background_color="#000000", font=('gotham', 13),  text_color="#FFFFFF")] for u, v, peso in arvore_minima],
        [sg.Text('      ', background_color="#000000")],
        [sg.Button('FECHAR', size=8, font=('gotham', 15, "bold"), button_color= ("#FFFFFF","#F7004F" )),sg.Button('VER GRAFO', size=13,font=('gotham', 15, "bold"), button_color= ("#FFFFFF","#F7004F" )) ]
    ]

    window = sg.Window('Árvore Geradora Mínima', layout, size= (300, 400), background_color= "#000000")

    while True:
        evento, valores = window.read()
        if evento == sg.WINDOW_CLOSED or evento == 'FECHAR':
            break

        elif evento == 'VER GRAFO':
            criar_janela_grafo(arestas,arvore_minima)
            window.close()
    window.close()

#cria a janela responsável por coletar os vértices e o peso de cada aresta
def cria_janela_aresta(i):
    layout =[
                [sg.Text(f'          Aresta {i+1}', background_color="#000000", font=('gotham', 20, "bold"),  text_color="#F7004F")],
                [sg.Text('      ', background_color="#000000")],
                [sg.Text('Vértice 1:', background_color="#000000", font=('gotham', 18, "bold"),  text_color="#F7004F")],
                [sg.Input(key=f'-V1{i+1}-', font=('gotham', 20, ),  background_color="#454041", text_color="#FFFFFF")],
                [sg.Text('Vértice 2:', background_color="#000000", font=('gotham', 18, "bold"),  text_color="#F7004F")],
                [sg.Input(key=f'-V2{i+1}-', font=('gotham', 20, ),  background_color="#454041", text_color="#FFFFFF")],
                [sg.Text('Peso:', background_color="#000000", font=('gotham', 18, "bold"),  text_color="#F7004F")],
                [sg.Input(key=f'-PESO{i+1}-', font=('gotham', 20,),  background_color="#454041", text_color="#FFFFFF")],
                [sg.Text('      ', background_color="#000000")],
                [sg.Button('Próxima Aresta', size=13, font=('gotham', 15, "bold"), button_color= ("#FFFFFF","#F7004F" ))],
        ]

    janela = sg.Window('ARESTAS', layout, size= (300, 400), background_color= "#000000" )
    evento, valores = janela.read()
    janela.close()

    v1 = int(valores[f'-V1{i+1}-'])
    v2 = int(valores[f'-V2{i+1}-'])
    peso = float(valores[f'-PESO{i+1}-'])

    return v1, v2, peso

#função que verifica se a aresta é válida
def verifica_aresta(arestas_inseridas, v1, v2):
    result = True

    if (v1, v2) in arestas_inseridas or (v2, v1) in arestas_inseridas:
        sg.popup('Aresta duplicada!\nInsira uma aresta válida.\n', background_color="#000000", font=('gotham', 16),button_color=("#FFFFFF","#F7004F" ),text_color="#FFFFFF", title= "AVISO" )
        result = False

    return result
