"""
The problem is modeled as a directed cyclic graph.  The graph is stored in an adjacency list like structure.

The colors are encoded from 0..4, and is stored in a dictionary. 
A list, where the index is the vertex index, contains all the edges to other vertices. An edge is a 
tuple of (vertex id, edge color). Another list colors where the index is also the vertex index, contains
the color of that vertex.
""" 
color = {
    'purple': 0, 
    'green': 1, 
    'orange': 2, 
    'black': 3, 
    'blue': 4
}
vertices_count = 23
finish = vertices_count - 1
edges = [
    # (edge to vertex id, color of the edge)
    [(3,  color['purple']), (4,  color['black'])],  # vertex 1
    [(5,  color['green']),  (11, color['purple'])],  # vertex 2
    [(0,  color['orange']), (3,  color['orange'])],  # vertex 3
    [(12, color['black'])],  # vertex 4
    [(8,  color['orange'])],  # vertex 5
    [(8,  color['green']),  (9,  color['purple'])],  # vertex 6
    [(1,  color['green'])],  # vertex 7
    [(2,  color['purple'])],  # vertex 8
    [(3,  color['green']),  (13, color['black'])],  # vertex 9
    [(14, color['green'])],  # vertex 10
    [(9,  color['purple']), (11, color['green'])],  # vertex 11
    [(6,  color['green'])],  # vertex 12
    [(7,  color['green']),  (17, color['green'])],  # vertex 13
    [(19, color['orange']), (finish, color['green'])],  # vertex 14
    [(finish, color['purple']), (21, color['green'])],  # vertex 15
    [(14, color['green'])],  # vertex 16
    [(10, color['black']),  (11, color['purple']), (15, color['black'])],  # vertex 17
    [(8,  color['orange']), (19, color['orange'])],  # vertex 18
    [(17, color['green'])],  # vertex 19
    [(18, color['black']),  (20, color['orange'])],  # vertex 20
    [(finish, color['black']), (21, color['orange'])],  # vertex 21
    [(16, color['orange'])],  # vertex 22
    []  # finish (vertex 23)
]
colors = [
    color['purple'],    # vertex 1
    color['black'],     # vertex 2
    color['green'],     # vertex 3
    color['green'],     # vertex 4
    color['green'],     # vertex 5
    color['orange'],    # vertex 6
    color['orange'],    # vertex 7
    color['purple'],    # vertex 8
    color['purple'],    # vertex 9
    color['black'],     # vertex 10
    color['orange'],    # vertex 11
    color['purple'],    # vertex 12
    color['orange'],    # vertex 13
    color['green'],     # vertex 14
    color['orange'],    # vertex 15
    color['green'],     # vertex 16
    color['green'],     # vertex 17
    color['black'],     # vertex 18
    color['orange'],    # vertex 19
    color['green'],     # vertex 20
    color['black'],     # vertex 21
    color['black'],     # vertex 22
    color['blue'],      # vertex finish
]

print('color', color)
print('vertices_count', vertices_count)
print('edges', edges)
print('colors', colors)

"""
There are 2 players, and each player can make an infinite amount of moves.
If a player is on a colored vertex, the other player can only travel over those colored edges.

Find all the solutions (steps to take for each player) for this problem.
"""


"""
Player 1 starts at position 1.
Player 2 starts at position 2.

A move is represented as a tuple (vertex id, player id), so (0, 0) means that player 1 is at vertex 1.
At each turn, a player can choose to move forward, or stay in the current position. This gives two options.
The other options are created by the edges, but the player can only move if the color of the edge matches
that of the other player's vertex color.

This gives the following options:
    Player A
        Edge 1
        Edge 2
        ...
        Edge n
    Player B
        Edge 1
        Edge 2
        ...
        Edge n

We traverse those options with a recursive backtrack algorithm. 
"""

path = [(0, 0), (1, 1)]
def get_player_pos(player):
    """
    Get the vertex id of the given player. Which is found by traversing
    the path backward until the player is found. Because both player are
    in the initial path, a result is guaranteed.
    """
    for v, p in path[::-1]:
        if p == player:
            return v


def other_player(player):
    """
    Returns the other player id.
    """
    if player == 0: return 1
    return 0


solution_id = 0
def save_solution():
    """
    Save the solution in a file.
    """
    global path, solution_id
    f = open('solutions/solution_{}.md'.format(solution_id), 'w')
    f.write('# Solution {}\n\n'.format(solution_id+1))
    f.write('![img](problem.png)\n\n')
    for v, p in path:
        f.write(' * Player {} move to {}\n'.format(p+1, v+1))
    f.close()
    solution_id += 1


def backtrack(current_vertex, current_player):
    if current_vertex == finish:
        print('solution', path)
        save_solution()
        return
    for player in range(2):
        player_vertex = get_player_pos(player)
        other_player_vertex = get_player_pos(other_player(player))
        other_player_vertex_color = colors[other_player_vertex]
        traversable_vertices = [v for v, c in edges[player_vertex] if c == other_player_vertex_color]
        for vertex in traversable_vertices:
            move = (vertex, player)
            path.append(move)
            backtrack(*move)
            del path[-1]

backtrack(0, 0)

"""
Due to circular references it is possible to walk through an infite loop? This will give a max recursion depth error.
The solution to this is to keep track of the visited vertices, and if we visit the same one again, then we know
we are in a loop, and has already been traversed.

Attempt 1: Keeping track of the visited vertex position gives an error, because there are 2 players, duh.
Attempt 2: Keeping track of the the visited (vertex, player) combination doesn't generate any solutions?
"""

# TODO: Fix that