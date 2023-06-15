from flask import Flask, request, render_template
from collections import defaultdict

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

class Graph:
    def __init__(self):
        self.edges = defaultdict(list)
        self.weights = {}

    def add_edge(self, from_node, to_node, weight):
        self.edges[from_node].append(to_node)
        self.edges[to_node].append(from_node)
        self.weights[(from_node, to_node)] = weight
        self.weights[(to_node, from_node)] = weight

# Create the graph and add edges
graph = Graph()
edges = [
    ('X', 'A', 7),
    ('X', 'B', 2),
    ('X', 'C', 3),
    ('X', 'E', 4),
    ('A', 'B', 3),
    ('A', 'D', 4),
    ('B', 'D', 4),
    ('B', 'H', 5),
    ('C', 'L', 2),
    ('D', 'F', 1),
    ('F', 'H', 3),
    ('G', 'H', 2),
    ('G', 'Y', 2),
    ('I', 'J', 6),
    ('I', 'K', 4),
    ('I', 'L', 4),
    ('J', 'L', 1),
    ('K', 'Y', 5),
]

for edge in edges:
    graph.add_edge(*edge)

@app.route('/shortest_path', methods=['POST', 'GET'])
def shortest_path():
    if request.method == 'POST':
        source = request.form['source']
        destination = request.form['destination']
        print("Received POST request")
        print("Source:", source)
        print("Destination:", destination)

    elif request.method == 'GET':
        source = request.args.get('source')
        destination = request.args.get('destination')
        print("Received GET request")
        print("Source:", source)
        print("Destination:", destination)
    else:
        return {"Error": "Invalid request method"}

    if source.upper() not in graph.edges:
        return render_template('result.html', result={"Message": f"Source '{source}' is not available."})

    if destination.upper() not in graph.edges:
        return render_template('result.html', result={"Message": f"Destination '{destination}' is not available."})

    path, distance = dijsktra(graph, source.upper(), destination.upper())
    if path == "Route Not Possible":
        return render_template('result.html', result={"Message": "Route not possible"})
    else:
        return render_template('result.html', result={"Path": "->".join(path), "Distance": distance})

def dijsktra(graph, initial, end):
    shortest_paths = {initial: (None, 0)}
    current_node = initial
    visited = set()

    while current_node != end:
        visited.add(current_node)
        destinations = graph.edges[current_node]
        weight_to_current_node = shortest_paths[current_node][1]

        for next_node in destinations:
            weight = graph.weights[(current_node, next_node)] + weight_to_current_node
            if next_node not in shortest_paths:
                shortest_paths[next_node] = (current_node, weight)
            else:
                current_shortest_weight = shortest_paths[next_node][1]
                if current_shortest_weight > weight:
                    shortest_paths[next_node] = (current_node, weight)

        next_destinations = {node: shortest_paths[node] for node in shortest_paths if node not in visited}
        if not next_destinations:
            return "Route Not Possible"

        current_node = min(next_destinations, key=lambda k: next_destinations[k][1])

    path = []
    distance = shortest_paths[end][1]
    while current_node is not None:
        path.append(current_node)
        next_node = shortest_paths[current_node][0]
        current_node = next_node

    path = path[::-1]
    return path, distance

if __name__ == "__main__":
    app.run(debug=True)
