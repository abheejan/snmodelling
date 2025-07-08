"""
Examples and demonstrations for the Social Clustering Simulation

This file shows how to:
1. Use different network types
2. Customize simulation parameters
3. Create custom networks
4. Run multiple simulations
"""

from social_network_data import create_social_network, create_clique_network, create_large_network
from main import SocialClusteringSimulation
from main_enhanced import EnhancedSocialClusteringSimulation

def example_basic_simulation():
    """Run the basic simulation with default settings"""
    print("Running basic social clustering simulation...")
    simulation = SocialClusteringSimulation()
    simulation.run()

def example_enhanced_simulation():
    """Run the enhanced simulation with multiple network types"""
    print("Running enhanced social clustering simulation...")
    simulation = EnhancedSocialClusteringSimulation()
    simulation.run()

def example_custom_parameters():
    """Example of how to customize simulation parameters"""
    print("Creating simulation with custom parameters...")
    
    # Create a custom simulation with different force settings
    simulation = SocialClusteringSimulation(width=1000, height=700)
    
    # Modify parameters for different behavior
    simulation.attraction_force = 8000    # Stronger attraction
    simulation.repulsion_force = 2000     # Weaker repulsion
    simulation.repulsion_distance = 150   # Longer repulsion range
    simulation.damping = 0.95             # More damping (slower movement)
    
    print(f"Attraction force: {simulation.attraction_force}")
    print(f"Repulsion force: {simulation.repulsion_force}")
    print(f"Repulsion distance: {simulation.repulsion_distance}")
    print(f"Damping: {simulation.damping}")
    
    simulation.run()

def example_network_analysis():
    """Analyze different network structures"""
    print("Analyzing different network structures...")
    
    # Test different network types
    networks = [
        ("Basic Network", create_social_network()),
        ("Clique Network", create_clique_network()),
        ("Large Network", create_large_network(25, 0.3))
    ]
    
    for name, network in networks:
        nodes = network['nodes']
        connections = network['connections']
        
        print(f"\n{name}:")
        print(f"  Nodes: {len(nodes)}")
        print(f"  Connections: {len(connections)}")
        print(f"  Groups: {len(set(n.get('group', 'A') for n in nodes))}")
        
        # Calculate connection density
        max_connections = len(nodes) * (len(nodes) - 1) // 2
        density = len(connections) / max_connections
        print(f"  Connection density: {density:.3f}")
        
        # Analyze connection strengths
        strengths = [conn.get('strength', 'medium') for conn in connections]
        strong_count = strengths.count('strong')
        medium_count = strengths.count('medium')
        weak_count = strengths.count('weak')
        
        print(f"  Strong connections: {strong_count}")
        print(f"  Medium connections: {medium_count}")
        print(f"  Weak connections: {weak_count}")

def example_custom_network():
    """Example of creating a custom network"""
    print("Creating custom network...")
    
    def create_custom_network():
        """Create a custom network with specific structure"""
        nodes = [
            {'id': 1, 'name': 'Leader1', 'group': 'Leaders'},
            {'id': 2, 'name': 'Leader2', 'group': 'Leaders'},
            {'id': 3, 'name': 'Member1', 'group': 'Members'},
            {'id': 4, 'name': 'Member2', 'group': 'Members'},
            {'id': 5, 'name': 'Member3', 'group': 'Members'},
            {'id': 6, 'name': 'Member4', 'group': 'Members'},
            {'id': 7, 'name': 'Outsider1', 'group': 'Outsiders'},
            {'id': 8, 'name': 'Outsider2', 'group': 'Outsiders'},
        ]
        
        connections = [
            # Leaders are strongly connected
            {'from': 1, 'to': 2, 'strength': 'strong'},
            
            # Leaders connect to members
            {'from': 1, 'to': 3, 'strength': 'medium'},
            {'from': 1, 'to': 4, 'strength': 'medium'},
            {'from': 2, 'to': 5, 'strength': 'medium'},
            {'from': 2, 'to': 6, 'strength': 'medium'},
            
            # Members have some connections
            {'from': 3, 'to': 4, 'strength': 'weak'},
            {'from': 5, 'to': 6, 'strength': 'weak'},
            
            # Outsiders are isolated
            {'from': 7, 'to': 8, 'strength': 'weak'},
        ]
        
        return {'nodes': nodes, 'connections': connections}
    
    # Create simulation with custom network
    simulation = SocialClusteringSimulation()
    
    # Replace the network creation
    network_data = create_custom_network()
    simulation.nodes = network_data['nodes']
    simulation.connections = network_data['connections']
    
    # Recreate the network
    simulation.create_network()
    
    print("Custom network created with:")
    print(f"  Leaders: 2 nodes")
    print(f"  Members: 4 nodes") 
    print(f"  Outsiders: 2 nodes")
    print(f"  Total connections: {len(simulation.connections)}")
    
    simulation.run()

def main():
    """Main function to run examples"""
    print("Social Clustering Simulation - Examples")
    print("=" * 50)
    
    while True:
        print("\nChoose an example to run:")
        print("1. Basic simulation")
        print("2. Enhanced simulation")
        print("3. Custom parameters")
        print("4. Network analysis")
        print("5. Custom network")
        print("6. Exit")
        
        choice = input("\nEnter your choice (1-6): ").strip()
        
        if choice == '1':
            example_basic_simulation()
        elif choice == '2':
            example_enhanced_simulation()
        elif choice == '3':
            example_custom_parameters()
        elif choice == '4':
            example_network_analysis()
        elif choice == '5':
            example_custom_network()
        elif choice == '6':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")

if __name__ == "__main__":
    main() 