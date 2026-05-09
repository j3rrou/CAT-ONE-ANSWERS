import heapq
 
class Node:
    """Represents a node in the search space."""
    def __init__(self, state, parent=None, g=0, h=0):
        self.state  = state    # Current state (e.g., city name)
        self.parent = parent   # Parent node for path reconstruction
        self.g      = g        # Cost from start to this node
        self.h      = h        # Heuristic: estimated cost to goal
        self.f      = g + h    # Total evaluation function f(n) = g + h
 
    # Allow comparison by f value (used by the priority queue)
    def __lt__(self, other):
        return self.f < other.f
 
 
def astar(graph, heuristics, start, goal):
    """
    A* Search Algorithm.
    graph      : dict of {node: [(neighbour, cost), ...]}
    heuristics : dict of {node: h_value}
    start      : starting state
    goal       : target state
    Returns    : optimal path as a list, or None if no path exists.
    """
    # Priority queue (min-heap) initialised with the start node
    open_list = []
    start_node = Node(state=start, g=0, h=heuristics[start])
    heapq.heappush(open_list, start_node)
 
    # Track best known g-cost for each state
    visited = {}          # {state: best_g_seen}
 
    while open_list:
        current = heapq.heappop(open_list)   # Pop node with lowest f
 
        # ── Goal test ──────────────────────────────────────────────
        if current.state == goal:
            return reconstruct_path(current)
 
        # Skip if we've already processed this state with lower cost
        if current.state in visited and visited[current.state] <= current.g:
            continue
        visited[current.state] = current.g
 
        # ── Expand neighbours ──────────────────────────────────────
        for neighbour, edge_cost in graph.get(current.state, []):
            g_new = current.g + edge_cost
            h_new = heuristics.get(neighbour, 0)
            child = Node(state=neighbour, parent=current, g=g_new, h=h_new)
            heapq.heappush(open_list, child)
 
    return None   # No path found
 
 
def reconstruct_path(node):
    """Trace back from goal node to start to build the path."""
    path = []
    while node:
        path.append((node.state, node.g))   # (state, cumulative cost)
        node = node.parent
    return list(reversed(path))
 
 
# ─── Example: Romania Road Map ────────────────────────────────────────────
# Classic AI textbook graph (Arad → Bucharest)
graph = {
    'Arad':          [('Zerind', 75),  ('Timisoara', 118), ('Sibiu', 140)],
    'Zerind':        [('Arad', 75),    ('Oradea', 71)],
    'Oradea':        [('Zerind', 71),  ('Sibiu', 151)],
    'Timisoara':     [('Arad', 118),   ('Lugoj', 111)],
    'Lugoj':         [('Timisoara',111),('Mehadia', 70)],
    'Mehadia':       [('Lugoj', 70),   ('Drobeta', 75)],
    'Drobeta':       [('Mehadia', 75), ('Craiova', 120)],
    'Sibiu':         [('Arad', 140),   ('Oradea', 151), ('Fagaras', 99), ('Rimnicu Vilcea', 80)],
    'Rimnicu Vilcea':[('Sibiu', 80),   ('Pitesti', 97), ('Craiova', 146)],
    'Fagaras':       [('Sibiu', 99),   ('Bucharest', 211)],
    'Pitesti':       [('Rimnicu Vilcea',97),('Craiova',138),('Bucharest',101)],
    'Craiova':       [('Drobeta',120), ('Rimnicu Vilcea',146),('Pitesti',138)],
    'Bucharest':     [('Fagaras',211), ('Pitesti',101),('Giurgiu',90),('Urziceni',85)],
}
 
# Straight-line distance heuristic to Bucharest (admissible)
heuristics = {
    'Arad': 366, 'Zerind': 374, 'Oradea': 380, 'Timisoara': 329,
    'Lugoj': 244, 'Mehadia': 241, 'Drobeta': 242, 'Craiova': 160,
    'Sibiu': 253, 'Rimnicu Vilcea': 193, 'Fagaras': 176, 'Pitesti': 100,
    'Bucharest': 0,
}
 
# ─── Run A* ───────────────────────────────────────────────────────────────
path = astar(graph, heuristics, start='Arad', goal='Bucharest')
 
if path:
    print('Optimal path found:')
    for state, cost in path:
        print(f'  {state:20s}  cumulative cost = {cost} km')
    print(f'\nTotal optimal cost: {path[-1][1]} km')
else:
    print('No path found.')
