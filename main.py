import pygame
import pymunk
import pymunk.pygame_util
import math
import random
from social_network_data import create_social_network

class SocialClusteringSimulation:
    def __init__(self, width=1200, height=800):
        self.width = width
        self.height = height
        
        # Initialize Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Social Attraction & Clustering Simulation")
        self.clock = pygame.time.Clock()
        
        # Initialize Pymunk space
        self.space = pymunk.Space()
        self.space.gravity = (0, 0)  # No gravity for social simulation
        
        # Drawing options
        self.draw_options = pymunk.pygame_util.DrawOptions(self.screen)
        
        # Simulation parameters
        self.attraction_force = 5000  # Force between connected nodes
        self.repulsion_force = 3000   # Force between unconnected nodes
        self.repulsion_distance = 100 # Distance for repulsion effect
        self.damping = 0.98           # Velocity damping
        
        # Network data
        self.nodes = []
        self.connections = []
        self.node_bodies = {}  # Map node IDs to pymunk bodies
        
        # Create initial network
        self.create_network()
        
        # Mouse interaction
        self.selected_body = None
        self.mouse_joint = None
        
    def create_network(self):
        """Create the social network with nodes and connections"""
        network_data = create_social_network()
        self.nodes = network_data['nodes']
        self.connections = network_data['connections']
        
        # Create pymunk bodies for each node
        for node in self.nodes:
            body = pymunk.Body(1, pymunk.moment_for_circle(1, 0, 15))
            body.position = (
                random.randint(50, self.width - 50),
                random.randint(50, self.height - 50)
            )
            body.velocity = (0, 0)
            
            # Create shape for the body
            shape = pymunk.Circle(body, 15)
            shape.elasticity = 0.8
            shape.friction = 0.7
            shape.collision_type = 1
            
            self.space.add(body, shape)
            self.node_bodies[node['id']] = body
    
    def apply_social_forces(self):
        """Apply attraction and repulsion forces based on social connections"""
        bodies = list(self.node_bodies.values())
        
        for i, body1 in enumerate(bodies):
            for j, body2 in enumerate(bodies[i+1:], i+1):
                # Get positions
                pos1 = body1.position
                pos2 = body2.position
                
                # Calculate distance and direction
                distance = math.sqrt((pos2.x - pos1.x)**2 + (pos2.y - pos1.y)**2)
                if distance < 1:  # Avoid division by zero
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
                    # Attraction force (stronger when further apart)
                    if distance > 50:  # Only attract if not too close
                        force_magnitude = self.attraction_force * (distance - 50) / 100
                        force_x = direction_x * force_magnitude
                        force_y = direction_y * force_magnitude
                        
                        body1.apply_force_at_local_point((force_x, force_y), (0, 0))
                        body2.apply_force_at_local_point((-force_x, -force_y), (0, 0))
                else:
                    # Repulsion force (stronger when closer)
                    if distance < self.repulsion_distance:
                        force_magnitude = self.repulsion_force * (self.repulsion_distance - distance) / self.repulsion_distance
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
            if event.button == 1:  # Left click
                mouse_pos = pygame.mouse.get_pos()
                mouse_pos_pymunk = pymunk.pygame_util.from_pygame(mouse_pos, self.screen)
                
                # Find body under mouse
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
        """Draw the network connections and nodes"""
        # Draw connections
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
                
                # Draw connection line
                pygame.draw.line(self.screen, (100, 100, 100), start_pos, end_pos, 2)
            except Exception as e:
                # Skip this connection if there's any error
                continue
        
        # Draw nodes (handled by pymunk's draw_options)
        self.space.debug_draw(self.draw_options)
        
        # Draw node labels
        font = pygame.font.Font(None, 24)
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
                
                # Draw node ID
                text = font.render(str(node['id']), True, (255, 255, 255))
                text_rect = text.get_rect(center=(pos[0], pos[1] - 25))
                self.screen.blit(text, text_rect)
            except Exception as e:
                # Skip this node if there's any error
                continue
    
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
                        # Reset simulation
                        self.space.clear()
                        self.node_bodies.clear()
                        self.create_network()
                
                self.handle_mouse_interaction(event)
            
            # Apply social forces
            self.apply_social_forces()
            
            # Update physics
            self.space.step(1/60.0)
            
            # Draw everything
            self.screen.fill((30, 30, 30))
            self.draw_network()
            
            # Draw UI
            font = pygame.font.Font(None, 36)
            info_text = font.render("ESC: Quit | R: Reset | Drag nodes to move them", True, (200, 200, 200))
            self.screen.blit(info_text, (10, 10))
            
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()

if __name__ == "__main__":
    simulation = SocialClusteringSimulation()
    simulation.run() 