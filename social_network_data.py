def create_social_network():
    """
    Create a sample social network with nodes and connections.
    This represents a social network where individuals are connected to friends.
    """
    
    # Define nodes (individuals in the social network)
    nodes = [
        {'id': 1, 'name': 'Alice', 'group': 'A'},
        {'id': 2, 'name': 'Bob', 'group': 'A'},
        {'id': 3, 'name': 'Charlie', 'group': 'A'},
        {'id': 4, 'name': 'Diana', 'group': 'B'},
        {'id': 5, 'name': 'Eve', 'group': 'B'},
        {'id': 6, 'name': 'Frank', 'group': 'B'},
        {'id': 7, 'name': 'Grace', 'group': 'C'},
        {'id': 8, 'name': 'Henry', 'group': 'C'},
        {'id': 9, 'name': 'Ivy', 'group': 'C'},
        {'id': 10, 'name': 'Jack', 'group': 'A'},
        {'id': 11, 'name': 'Kate', 'group': 'B'},
        {'id': 12, 'name': 'Liam', 'group': 'C'},
        {'id': 13, 'name': 'Mia', 'group': 'A'},
        {'id': 14, 'name': 'Noah', 'group': 'B'},
        {'id': 15, 'name': 'Olivia', 'group': 'C'},
    ]
    
    # Define connections (social relationships)
    # Strong connections within groups, some cross-group connections
    connections = [
        # Group A connections
        {'from': 1, 'to': 2, 'strength': 'strong'},
        {'from': 1, 'to': 3, 'strength': 'strong'},
        {'from': 1, 'to': 10, 'strength': 'strong'},
        {'from': 2, 'to': 3, 'strength': 'strong'},
        {'from': 2, 'to': 10, 'strength': 'medium'},
        {'from': 3, 'to': 10, 'strength': 'medium'},
        {'from': 1, 'to': 13, 'strength': 'strong'},
        {'from': 2, 'to': 13, 'strength': 'medium'},
        {'from': 10, 'to': 13, 'strength': 'strong'},
        
        # Group B connections
        {'from': 4, 'to': 5, 'strength': 'strong'},
        {'from': 4, 'to': 6, 'strength': 'strong'},
        {'from': 5, 'to': 6, 'strength': 'strong'},
        {'from': 4, 'to': 11, 'strength': 'strong'},
        {'from': 5, 'to': 11, 'strength': 'medium'},
        {'from': 6, 'to': 11, 'strength': 'medium'},
        {'from': 4, 'to': 14, 'strength': 'medium'},
        {'from': 5, 'to': 14, 'strength': 'strong'},
        {'from': 11, 'to': 14, 'strength': 'strong'},
        
        # Group C connections
        {'from': 7, 'to': 8, 'strength': 'strong'},
        {'from': 7, 'to': 9, 'strength': 'strong'},
        {'from': 8, 'to': 9, 'strength': 'strong'},
        {'from': 7, 'to': 12, 'strength': 'medium'},
        {'from': 8, 'to': 12, 'strength': 'strong'},
        {'from': 9, 'to': 12, 'strength': 'medium'},
        {'from': 7, 'to': 15, 'strength': 'medium'},
        {'from': 8, 'to': 15, 'strength': 'medium'},
        {'from': 12, 'to': 15, 'strength': 'strong'},
        
        # Cross-group connections (weaker, creating interesting dynamics)
        {'from': 1, 'to': 4, 'strength': 'weak'},    # Alice - Diana
        {'from': 3, 'to': 6, 'strength': 'weak'},    # Charlie - Frank
        {'from': 5, 'to': 8, 'strength': 'weak'},    # Eve - Henry
        {'from': 7, 'to': 10, 'strength': 'weak'},   # Grace - Jack
        {'from': 2, 'to': 11, 'strength': 'weak'},   # Bob - Kate
        {'from': 9, 'to': 14, 'strength': 'weak'},   # Ivy - Noah
        {'from': 13, 'to': 15, 'strength': 'weak'},  # Mia - Olivia
    ]
    
    return {
        'nodes': nodes,
        'connections': connections
    }

def create_large_network(num_nodes=50, connection_probability=0.3):
    """
    Create a larger random social network for more complex simulations.
    
    Args:
        num_nodes: Number of nodes in the network
        connection_probability: Probability of connection between any two nodes
    """
    import random
    
    nodes = []
    for i in range(1, num_nodes + 1):
        group = chr(65 + (i - 1) % 5)  # Groups A, B, C, D, E
        nodes.append({
            'id': i,
            'name': f'Person_{i}',
            'group': group
        })
    
    connections = []
    for i in range(1, num_nodes + 1):
        for j in range(i + 1, num_nodes + 1):
            # Higher probability for same group connections
            node_i = next(n for n in nodes if n['id'] == i)
            node_j = next(n for n in nodes if n['id'] == j)
            
            if node_i['group'] == node_j['group']:
                # Same group: higher connection probability
                if random.random() < connection_probability * 2:
                    connections.append({
                        'from': i,
                        'to': j,
                        'strength': random.choice(['strong', 'medium'])
                    })
            else:
                # Different group: lower connection probability
                if random.random() < connection_probability * 0.3:
                    connections.append({
                        'from': i,
                        'to': j,
                        'strength': 'weak'
                    })
    
    return {
        'nodes': nodes,
        'connections': connections
    }

def create_clique_network():
    """
    Create a network with distinct cliques to demonstrate clustering behavior.
    """
    nodes = [
        # Clique 1: Tech enthusiasts
        {'id': 1, 'name': 'Alex', 'group': 'Tech'},
        {'id': 2, 'name': 'Sam', 'group': 'Tech'},
        {'id': 3, 'name': 'Jordan', 'group': 'Tech'},
        {'id': 4, 'name': 'Taylor', 'group': 'Tech'},
        
        # Clique 2: Artists
        {'id': 5, 'name': 'Casey', 'group': 'Art'},
        {'id': 6, 'name': 'Riley', 'group': 'Art'},
        {'id': 7, 'name': 'Quinn', 'group': 'Art'},
        {'id': 8, 'name': 'Morgan', 'group': 'Art'},
        
        # Clique 3: Athletes
        {'id': 9, 'name': 'Parker', 'group': 'Sports'},
        {'id': 10, 'name': 'Drew', 'group': 'Sports'},
        {'id': 11, 'name': 'Blake', 'group': 'Sports'},
        {'id': 12, 'name': 'Avery', 'group': 'Sports'},
        
        # Bridge nodes (connect different cliques)
        {'id': 13, 'name': 'Cameron', 'group': 'Bridge'},
        {'id': 14, 'name': 'Dakota', 'group': 'Bridge'},
    ]
    
    connections = [
        # Tech clique connections
        {'from': 1, 'to': 2, 'strength': 'strong'},
        {'from': 1, 'to': 3, 'strength': 'strong'},
        {'from': 1, 'to': 4, 'strength': 'strong'},
        {'from': 2, 'to': 3, 'strength': 'strong'},
        {'from': 2, 'to': 4, 'strength': 'strong'},
        {'from': 3, 'to': 4, 'strength': 'strong'},
        
        # Art clique connections
        {'from': 5, 'to': 6, 'strength': 'strong'},
        {'from': 5, 'to': 7, 'strength': 'strong'},
        {'from': 5, 'to': 8, 'strength': 'strong'},
        {'from': 6, 'to': 7, 'strength': 'strong'},
        {'from': 6, 'to': 8, 'strength': 'strong'},
        {'from': 7, 'to': 8, 'strength': 'strong'},
        
        # Sports clique connections
        {'from': 9, 'to': 10, 'strength': 'strong'},
        {'from': 9, 'to': 11, 'strength': 'strong'},
        {'from': 9, 'to': 12, 'strength': 'strong'},
        {'from': 10, 'to': 11, 'strength': 'strong'},
        {'from': 10, 'to': 12, 'strength': 'strong'},
        {'from': 11, 'to': 12, 'strength': 'strong'},
        
        # Bridge connections
        {'from': 13, 'to': 1, 'strength': 'medium'},   # Cameron connects to Tech
        {'from': 13, 'to': 5, 'strength': 'medium'},   # Cameron connects to Art
        {'from': 14, 'to': 5, 'strength': 'medium'},   # Dakota connects to Art
        {'from': 14, 'to': 9, 'strength': 'medium'},   # Dakota connects to Sports
        {'from': 13, 'to': 14, 'strength': 'weak'},    # Bridge nodes connected
    ]
    
    return {
        'nodes': nodes,
        'connections': connections
    } 