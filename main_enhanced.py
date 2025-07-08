import pygame
import pymunk
import pymunk.pygame_util
import math
import random
from social_network_data import create_social_network, create_clique_network, create_large_network

class EnhancedSocialClusteringSimulation:
    def __init__(self, width=1400, height=900):
        self.width = width
        self.height = height
        
        # Initialize Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Enhanced Social Attraction & Clustering Simulation")
        self.clock = pygame.time.Clock()
        
        # Initialize Pymunk space
        self.space = pymunk.Space()
        self.space.gravity = (0, 0)
        
        # Drawing options
        self.draw_options = pymunk.pygame_util.DrawOptions(self.screen)
        
        # Simulation parameters - reduced forces for stability
        self.attraction_force = 2000  # Reduced from 5000
        self.repulsion_force = 1500   # Reduced from 3000
        self.repulsion_distance = 80  # Reduced from 100
        self.damping = 0.95           # Increased damping for stability
        
        # Network data
        self.nodes = []
        self.connections = []
        self.node_bodies = {}
        self.node_shapes = {}  # Store shapes for custom drawing
        
        # Color scheme for groups
        self.group_colors = {
            'A': (255, 100, 100),    # Red
            'B': (100, 255, 100),    # Green
            'C': (100, 100, 255),    # Blue
            'Tech': (255, 165, 0),   # Orange
            'Art': (255, 20, 147),   # Deep Pink
            'Sports': (0, 255, 255), # Cyan
            'Bridge': (255, 255, 0), # Yellow
        }
        
        # UI state
        self.show_forces = False
        self.show_metrics = True
        self.paused = False
        self.selected_body = None
        self.mouse_joint = None
        
        # Network selection
        self.network_types = ['basic', 'clique', 'large']
        self.current_network = 0
        
        # Create boundary walls to keep nodes in view
        self.create_boundaries()
        
        # Create initial network
        self.create_network()
        
    def create_boundaries(self):
        """Create boundary walls to keep nodes within the screen"""
        # Create static bodies for boundaries
        thickness = 20
        static_body = pymunk.Body(body_type=pymunk.Body.STATIC)
        
        # Top wall
        top_wall = pymunk.Segment(static_body, (0, thickness), (self.width, thickness), thickness)
        top_wall.elasticity = 0.8
        top_wall.friction = 0.7
        
        # Bottom wall
        bottom_wall = pymunk.Segment(static_body, (0, self.height - thickness), (self.width, self.height - thickness), thickness)
        bottom_wall.elasticity = 0.8
        bottom_wall.friction = 0.7
        
        # Left wall
        left_wall = pymunk.Segment(static_body, (thickness, 0), (thickness, self.height), thickness)
        left_wall.elasticity = 0.8
        left_wall.friction = 0.7
        
        # Right wall
        right_wall = pymunk.Segment(static_body, (self.width - thickness, 0), (self.width - thickness, self.height), thickness)
        right_wall.elasticity = 0.8
        right_wall.friction = 0.7
        
        self.space.add(static_body, top_wall, bottom_wall, left_wall, right_wall)
        
    def create_network(self):
        """Create the social network with nodes and connections"""
        # Only clear node bodies, not the entire space (preserves boundaries)
        for body in list(self.node_bodies.values()):
            if body in self.space.bodies:
                self.space.remove(body)
        self.node_bodies.clear()
        self.node_shapes.clear()
        
        # Select network type
        if self.current_network == 0:
            network_data = create_social_network()
        elif self.current_network == 1:
            network_data = create_clique_network()
        else:
            network_data = create_large_network(30, 0.4)
        
        self.nodes = network_data['nodes']
        self.connections = network_data['connections']
        
        # Create pymunk bodies for each node
        for node in self.nodes:
            body = pymunk.Body(1, pymunk.moment_for_circle(1, 0, 18))
            body.position = (
                random.randint(100, self.width - 100),
                random.randint(100, self.height - 100)
            )
            body.velocity = (0, 0)
            
            # Create shape for the body
            shape = pymunk.Circle(body, 18)
            shape.elasticity = 0.8
            shape.friction = 0.7
            shape.collision_type = 1
            
            self.space.add(body, shape)
            self.node_bodies[node['id']] = body
            self.node_shapes[node['id']] = shape
    
    def apply_social_forces(self):
        """Apply attraction and repulsion forces based on social connections"""
        if self.paused:
            return
            
        bodies = list(self.node_bodies.values())
        
        for i, body1 in enumerate(bodies):
            for j, body2 in enumerate(bodies[i+1:], i+1):
                # Skip if bodies are None or not in space
                if not body1 or not body2 or body1 not in self.space.bodies or body2 not in self.space.bodies:
                    continue
                    
                pos1 = body1.position
                pos2 = body2.position
                
                distance = math.sqrt((pos2.x - pos1.x)**2 + (pos2.y - pos1.y)**2)
                if distance < 1:
                    continue
                
                direction_x = (pos2.x - pos1.x) / distance
                direction_y = (pos2.y - pos1.y) / distance
                
                # Check if nodes are connected
                node1_id = [k for k, v in self.node_bodies.items() if v == body1][0]
                node2_id = [k for k, v in self.node_bodies.items() if v == body2][0]
                
                is_connected = any(
                    (conn['from'] == node1_id and conn['to'] == node2_id) or
                    (conn['from'] == node2_id and conn['to'] == node1_id)
                    for conn in self.connections
                )
                
                if is_connected:
                    # Attraction force - only if not too close
                    if distance > 60:  # Increased minimum distance
                        force_magnitude = min(self.attraction_force * (distance - 60) / 100, 1000)  # Cap maximum force
                        force_x = direction_x * force_magnitude
                        force_y = direction_y * force_magnitude
                        
                        body1.apply_force_at_local_point((force_x, force_y), (0, 0))
                        body2.apply_force_at_local_point((-force_x, -force_y), (0, 0))
                else:
                    # Repulsion force - only if too close
                    if distance < self.repulsion_distance:
                        force_magnitude = min(self.repulsion_force * (self.repulsion_distance - distance) / self.repulsion_distance, 800)  # Cap maximum force
                        force_x = -direction_x * force_magnitude
                        force_y = -direction_y * force_magnitude
                        
                        body1.apply_force_at_local_point((force_x, force_y), (0, 0))
                        body2.apply_force_at_local_point((-force_x, -force_y), (0, 0))
                
                # Apply damping to velocities
                body1.velocity = (body1.velocity.x * self.damping, body1.velocity.y * self.damping)
                body2.velocity = (body2.velocity.x * self.damping, body2.velocity.y * self.damping)
    
    def handle_mouse_interaction(self, event):
        """Handle mouse events for dragging nodes"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                mouse_pos_pymunk = pymunk.pygame_util.from_pygame(mouse_pos, self.screen)
                
                query_info = self.space.point_query_nearest(mouse_pos_pymunk, 0, pymunk.ShapeFilter())
                if query_info:
                    self.selected_body = query_info.shape.body
                    self.mouse_joint = pymunk.PinJoint(self.selected_body, self.space.static_body, 
                                                     (0, 0), mouse_pos_pymunk)
                    self.space.add(self.mouse_joint)
        
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and self.mouse_joint:
                self.space.remove(self.mouse_joint)
                self.mouse_joint = None
                self.selected_body = None
        
        elif event.type == pygame.MOUSEMOTION:
            if self.mouse_joint and self.selected_body:
                mouse_pos = pygame.mouse.get_pos()
                mouse_pos_pymunk = pymunk.pygame_util.from_pygame(mouse_pos, self.screen)
                self.mouse_joint.anchor_b = mouse_pos_pymunk
    
    def draw_network(self):
        """Draw the network with enhanced visualization"""
        # Draw connections with varying thickness based on strength
        for connection in self.connections:
            try:
                from_body = self.node_bodies[connection['from']]
                to_body = self.node_bodies[connection['to']]
                
                # Check if bodies exist and have valid positions
                if not from_body or not to_body:
                    continue
                
                start_pos = pymunk.pygame_util.to_pygame(from_body.position, self.screen)
                end_pos = pymunk.pygame_util.to_pygame(to_body.position, self.screen)
                
                # Validate positions
                if (not isinstance(start_pos, (tuple, list)) or not isinstance(end_pos, (tuple, list)) or
                    len(start_pos) != 2 or len(end_pos) != 2):
                    continue
                
                # Additional validation for numeric values
                if not all(isinstance(x, (int, float)) for x in start_pos + end_pos):
                    continue
                
                # Line thickness based on connection strength
                thickness = 1
                if connection.get('strength') == 'strong':
                    thickness = 3
                    color = (150, 150, 150)
                elif connection.get('strength') == 'medium':
                    thickness = 2
                    color = (120, 120, 120)
                else:
                    color = (80, 80, 80)
                
                pygame.draw.line(self.screen, color, start_pos, end_pos, thickness)
            except Exception as e:
                # Skip this connection if there's any error
                continue
        
        # Draw nodes with custom colors
        for node in self.nodes:
            try:
                body = self.node_bodies[node['id']]
                if not body:
                    continue
                    
                pos = pymunk.pygame_util.to_pygame(body.position, self.screen)
                
                # Validate position
                if not isinstance(pos, (tuple, list)) or len(pos) != 2:
                    continue
                if not all(isinstance(x, (int, float)) for x in pos):
                    continue
                
                # Get color for the group
                group = node.get('group', 'A')
                color = self.group_colors.get(group, (200, 200, 200))
                
                # Draw node circle
                pygame.draw.circle(self.screen, color, pos, 18)
                pygame.draw.circle(self.screen, (255, 255, 255), pos, 18, 2)  # White border
                
                # Draw node ID
                font = pygame.font.Font(None, 24)
                text = font.render(str(node['id']), True, (0, 0, 0))
                text_rect = text.get_rect(center=(pos[0], pos[1]))
                self.screen.blit(text, text_rect)
            except Exception as e:
                # Skip this node if there's any error
                continue
    
    def draw_ui(self):
        """Draw user interface elements"""
        font_small = pygame.font.Font(None, 24)
        font_large = pygame.font.Font(None, 36)
        
        # Background for UI
        ui_bg = pygame.Surface((400, 200))
        ui_bg.set_alpha(200)
        ui_bg.fill((20, 20, 20))
        self.screen.blit(ui_bg, (10, 10))
        
        # Title
        title = font_large.render("Social Clustering Simulation", True, (255, 255, 255))
        self.screen.blit(title, (20, 20))
        
        # Controls
        controls = [
            "Controls:",
            "Mouse: Drag nodes",
            "R: Reset simulation",
            "N: Next network",
            "P: Pause/Resume",
            "F: Toggle force display",
            "ESC: Quit"
        ]
        
        for i, control in enumerate(controls):
            color = (255, 255, 255) if i == 0 else (200, 200, 200)
            text = font_small.render(control, True, color)
            self.screen.blit(text, (20, 60 + i * 20))
        
        # Network info
        network_names = ['Basic Network', 'Clique Network', 'Large Network']
        network_text = font_small.render(f"Network: {network_names[self.current_network]}", True, (255, 255, 0))
        self.screen.blit(network_text, (20, 200))
        
        # Status
        status = "PAUSED" if self.paused else "RUNNING"
        status_color = (255, 100, 100) if self.paused else (100, 255, 100)
        status_text = font_small.render(f"Status: {status}", True, status_color)
        self.screen.blit(status_text, (20, 220))
        
        # Metrics
        if self.show_metrics:
            self.draw_metrics()
    
    def draw_metrics(self):
        """Draw network metrics"""
        font_small = pygame.font.Font(None, 20)
        
        # Calculate metrics
        total_nodes = len(self.nodes)
        total_connections = len(self.connections)
        
        # Calculate average distance between connected nodes
        connected_distances = []
        for connection in self.connections:
            from_body = self.node_bodies[connection['from']]
            to_body = self.node_bodies[connection['to']]
            distance = math.sqrt((to_body.position.x - from_body.position.x)**2 + 
                               (to_body.position.y - from_body.position.y)**2)
            connected_distances.append(distance)
        
        avg_distance = sum(connected_distances) / len(connected_distances) if connected_distances else 0
        
        # Display metrics
        metrics = [
            f"Nodes: {total_nodes}",
            f"Connections: {total_connections}",
            f"Avg Distance: {avg_distance:.1f}",
            f"Groups: {len(set(n.get('group', 'A') for n in self.nodes))}"
        ]
        
        for i, metric in enumerate(metrics):
            text = font_small.render(metric, True, (200, 200, 200))
            self.screen.blit(text, (self.width - 200, 20 + i * 20))
    
    def run(self):
        """Main simulation loop"""
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_r:
                        self.create_network()
                    elif event.key == pygame.K_n:
                        self.current_network = (self.current_network + 1) % len(self.network_types)
                        self.create_network()
                    elif event.key == pygame.K_p:
                        self.paused = not self.paused
                    elif event.key == pygame.K_f:
                        self.show_forces = not self.show_forces
                
                self.handle_mouse_interaction(event)
            
            # Apply social forces
            self.apply_social_forces()
            
            # Update physics
            if not self.paused:
                self.space.step(1/60.0)
            
            # Draw everything
            self.screen.fill((30, 30, 30))
            self.draw_network()
            self.draw_ui()
            
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()

if __name__ == "__main__":
    simulation = EnhancedSocialClusteringSimulation()
    simulation.run() 