import networkx as nx
import matplotlib.pyplot as plt
from collections import deque


def build_london_metro_graph():
    """Створює фрагмент мережі метро Лондона як граф NetworkX."""
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

    # Додаємо ребра для кожної лінії
    for line_name, stations in lines.items():
        for i in range(len(stations) - 1):
            u, v = stations[i], stations[i + 1]
            if graph.has_edge(u, v):
                graph[u][v].setdefault("lines", set()).add(line_name)
            else:
                graph.add_edge(u, v, lines={line_name})

    # Позначаємо пересадкові вузли
    for station, lns in interchanges:
        if station in graph.nodes:
            graph.nodes[station]["interchange"] = True
            graph.nodes[station]["lines"] = sorted(lns)

    # Інші вузли
    for node in graph.nodes:
        if "interchange" not in graph.nodes[node]:
            graph.nodes[node]["interchange"] = False
            node_lines = set()
            for neighbor in graph.neighbors(node):
                edge_lines = graph.get_edge_data(node, neighbor).get("lines", set())
                node_lines |= edge_lines
            graph.nodes[node]["lines"] = sorted(node_lines)

    return graph


def visualize_graph(graph):
    """Візуалізує граф метро Лондона."""
    pos = nx.spring_layout(graph, seed=42)
    plt.figure(figsize=(12, 8))

    line_colors = {
        "Central": "#DC241F",
        "Jubilee": "#A0A5A9",
        "Piccadilly": "#0019A8",
        "District": "#00782A",
        "Circle": "#FFD300",
    }

    # Малюємо ребра з кольорами ліній
    for u, v, data in graph.edges(data=True):
        lines_set = data.get("lines", {"Unknown"})
        line = next(iter(lines_set))
        color = line_colors.get(line, "#999999")
        nx.draw_networkx_edges(
            graph, pos, edgelist=[(u, v)], width=2.0, edge_color=color
        )

    # Вузли: пересадки та звичайні
    interchange_nodes = [n for n, d in graph.nodes(data=True) if d["interchange"]]
    regular_nodes = [n for n, d in graph.nodes(data=True) if not d["interchange"]]

    nx.draw_networkx_nodes(
        graph, pos, nodelist=regular_nodes, node_size=500,
        node_color="#87CEFA", alpha=0.9
    )
    nx.draw_networkx_nodes(
        graph, pos, nodelist=interchange_nodes, node_size=800,
        node_color="#FF8C00", alpha=0.95
    )

    nx.draw_networkx_labels(graph, pos, font_size=9)

    plt.title("Фрагмент мережі метро Лондона")
    plt.axis("off")
    plt.tight_layout()
    plt.show()


def analyze_graph(graph):
    """Виводить основні характеристики графа."""
    num_nodes = graph.number_of_nodes()
    num_edges = graph.number_of_edges()
    degrees = dict(graph.degree())
    avg_degree = sum(degrees.values()) / num_nodes
    density = nx.density(graph)
    components = list(nx.connected_components(graph))

    print("=== ПІДСУМКИ ГРАФА ===")
    print(f"Кількість станцій: {num_nodes}")
    print(f"Кількість з’єднань: {num_edges}")
    print(f"Середній ступінь вершини: {avg_degree:.2f}")
    print(f"Щільність графа: {density:.4f}")
    print(f"Кількість компонент зв’язності: {len(components)}")

    print("\n=== Ступені вершин (приклад) ===")
    for node, degree in list(degrees.items())[:10]:
        print(f"{node}: {degree}")


def dfs_path(graph, start, goal):
    """Пошук шляху за допомогою DFS."""
    stack = [(start, [start])]
    visited = set()

    while stack:
        node, path = stack.pop()
        if node == goal:
            return path
        if node not in visited:
            visited.add(node)
            for neighbor in graph.neighbors(node):
                if neighbor not in visited:
                    stack.append((neighbor, path + [neighbor]))
    return None


def bfs_path(graph, start, goal):
    """Пошук шляху за допомогою BFS."""
    queue = deque([(start, [start])])
    visited = set()

    while queue:
        node, path = queue.popleft()
        if node == goal:
            return path
        if node not in visited:
            visited.add(node)
            for neighbor in graph.neighbors(node):
                if neighbor not in visited:
                    queue.append((neighbor, path + [neighbor]))
    return None


if __name__ == "__main__":
    metro_graph = build_london_metro_graph()
    visualize_graph(metro_graph)
    analyze_graph(metro_graph)

    start_station = "Notting Hill Gate"
    goal_station = "London Bridge"

    dfs_result = dfs_path(metro_graph, start_station, goal_station)
    bfs_result = bfs_path(metro_graph, start_station, goal_station)

    print("\n=== DFS шлях ===")
    print(" -> ".join(dfs_result))

    print("\n=== BFS шлях ===")
    print(" -> ".join(bfs_result))

    print("\n=== Пояснення різниці ===")
    print("DFS йде вглиб графа, тому шлях може бути довший і не оптимальний.")
    print("BFS шукає у ширину, тому знаходить найкоротший шлях у незваженому графі.")