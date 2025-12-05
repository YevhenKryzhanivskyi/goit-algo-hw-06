import network as nx
import matplotlib.pyplot as plt

def build_london_metro_graph():

        lines = {
        "Central": [
            "Notting Hill Gate", "Queensway", "Lancaster Gate", "Marble Arch",
            "Bond Street", "Oxford Circus", "Tottenham Court Road", "Holborn"
        ],
        "Jubilee": [
            "Bond Street", "Green Park", "Westminster", "Waterloo",
            "Southwark", "London Bridge"
        ],
        "Piccadilly": [
            "South Kensington", "Gloucester Road", "Earl's Court",
            "Barons Court", "Hammersmith", "Turnham Green", "Acton Town"
        ],
        "District": [
            "Notting Hill Gate", "High Street Kensington", "Earl's Court",
            "West Kensington", "Barons Court", "Hammersmith"
        ],
        "Circle": [
            "Paddington", "Edgware Road", "Baker Street", "Great Portland Street",
            "Euston Square", "Farringdon", "Barbican"
        ],
    }

    interchanges = [
        ("Bond Street", ["Central", "Jubilee"]),
        ("Oxford Circus", ["Central"]),
        ("Baker Street", ["Circle"]),
        ("Earl's Court", ["District", "Piccadilly"]),
        ("Hammersmith", ["District", "Piccadilly"]),
        ("South Kensington", ["Piccadilly"]),
        ("Notting Hill Gate", ["Central", "District"]),
        ("Green Park", ["Jubilee"]),
    ]

    graph = nx.Graph()

    for line_name, stations in lines.items():
        for i in range(len(stations) - 1):
            u = stations[i]
            v = stations[i + 1]
            if graph.has_edge(u, v):
                graph[u][v].setdefault("lines", set()).add(line_name)
            else:
                graph.add_edge(u, v, lines={line_name})
    
    for station, lns in interchanges:
        if station in graph.nodes:
             graph.nodes[station]["interchanges"] = True
             graph.nodes[station]["lines"] = sorted(lns)

    
    for node in graph.nodes:
        if "interchanges" not in graph.nodes[node]:
            graph.nodes[node]["interchanges"] = False
            node_lines = set()
            for neighbor in graph.neighbors(node):
                edge_lines = graph.get_edge_data(node, neighbore).get("lines", set())
                node_lines |= edge_lines
            graph.nodes[node]["lines"] = sorted(node_lines)

    return graph


def visualize_graph(graph):
    pos = nx.spring_layout(graph, seed=42)
    plt.figure(figsize=(12, 8))

    line_colors = {
        "Central": "#DC241F",
        "Jubilee": "#A0A5A9",
        "Piccadilly": "#0019A8",
        "District": "#00782A",
        "Circle": "#FFD300",
    }

    