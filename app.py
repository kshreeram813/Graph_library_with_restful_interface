from flask import Flask, request, render_template
from collections import defaultdict

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

class Graph:
    def __init__(self):
        self.edges = defaultdict(list)    # A dictionary to store the edges of the graph
        self.weights = {}  # A dictionary to store the weights of the edges

    def add_edge(self, from_node, to_node, weight):     # The code iterates over the edges and adds them to the graph
        self.edges[from_node].append(to_node)
        self.edges[to_node].append(from_node)
        self.weights[(from_node, to_node)] = weight
        self.weights[(to_node, from_node)] = weight

graph = Graph()     # Create the graph and add edges
edges = [
    ('A', 'B', 1),
    ('A', 'C', 2),
    ('B', 'F', 1),
    ('F', 'E', 1),
    ('E', 'D', 1),
    ('D', 'C', 2),
    ('B', 'D', 3),
    ('C', 'E', 2),
    ('C', 'F', 4),
    ('D', 'F', 2),
    ('E', 'A', 3),
]

for edge in edges:
    graph.add_edge(*edge)

@app.route('/shortest_path', methods=['POST', 'GET'])
def shortest_path():
    if request.method == 'POST':
        # If the request method is POST, retrieve the source and destination values from the form
        source = request.form['source']
        destination = request.form['destination']
        print("Received POST request")
        print("Source:", source)
        print("Destination:", destination)

    elif request.method == 'GET':
        # If the request method is GET, retrieve the source and destination values from the query parameters
        source = request.args.get('source')
        destination = request.args.get('destination')
        print("Received GET request")
        print("Source:", source)
        print("Destination:", destination)
    else:
        # If the request method is neither POST nor GET, return an error message
        return {"Error": "Invalid request method"}

    if source.upper() not in graph.edges:    # Check if source node is available in the graph
        return render_template('result.html', result={"Message": f"Source '{source}' is not available."})

    if destination.upper() not in graph.edges:   # Check if destination node is available in the graph
        return render_template('result.html', result={"Message": f"Destination '{destination}' is not available."})

    path, distance = dijsktra(graph, source.upper(), destination.upper()) # Find the shortest path and distance using Dijkstra's algorithm
    if path == "Route Not Possible":    # If the path is "Route Not Possible", display an error message
        return render_template('result.html', result={"Message": "Route not possible"})
    else:
        # dictionary is created to store the result of the shortest path calculation
        result_data = {"Path": "=>".join(path), "Distance": distance}  
        store_result(result_data)
        return render_template('result.html', result=result_data)

def dijsktra(graph, initial, end):
    shortest_paths = {initial: (None, 0)}
    current_node = initial
    visited = set()

    while current_node != end:         # Continue until the current_node becomes the end node
        visited.add(current_node)    # Mark the current_node as visited
        destinations = graph.edges[current_node]
        weight_to_current_node = shortest_paths[current_node][1]

        for next_node in destinations:  # Iterate over the neighboring nodes
            weight = graph.weights[(current_node, next_node)] + weight_to_current_node
            if next_node not in shortest_paths:  # If next_node is not in shortest_paths, add it
                shortest_paths[next_node] = (current_node, weight)
            else:
                current_shortest_weight = shortest_paths[next_node][1]
                if current_shortest_weight > weight:    # If the new weight is smaller, update the shortest_paths dictionary
                    shortest_paths[next_node] = (current_node, weight)

        next_destinations = {node: shortest_paths[node] for node in shortest_paths if node not in visited}
        if not next_destinations:   # If there are no unvisited nodes, the route is not possible
            return "Route Not Possible"
        # Find the next node with the minimum weight and update the current_node
        current_node = min(next_destinations, key=lambda k: next_destinations[k][1])

    path = []    # Reconstruct the path from end to start
    distance = shortest_paths[end][1]     # swap method
    while current_node is not None:
        path.append(current_node)
        next_node = shortest_paths[current_node][0]
        current_node = next_node

    path = path[::-1]    # Reverse the path to start from the source node
    return path, distance

def store_result(data):     # Writes the path and distance data to a text file named 'result.txt'.
    with open('result.txt', 'w') as file:
        file.write(f"Path: {data['Path']}\n")
        file.write(f"Distance: {data['Distance']}")

def read_result():   # Reads the path and distance data from the 'result.txt' file and returns it as a dictionary.
    with open('result.txt', 'r') as file:
        path = file.readline().split(": ")[1].strip()
        distance = file.readline().split(": ")[1].strip()
    return {"Path": path, "Distance": distance}

@app.route('/display_result')
def display_result():
    result_data = read_result()
    return render_template('result.html', result=result_data)   # pass- data to reult.html page

if __name__ == "__main__":
    app.run(debug=True)
    # app.run(debug=True, host='2409:40f2:2e:71b3:b8ad:172e:4ac5:43cb', port=5000)







