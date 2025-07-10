# Requires: pip install pygame pymunk
import pygame
import pymunk
import pymunk.pygame_util
import math
import random

# --- Minimal Social Network Data ---
def create_social_network():
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
    connections = [
        {'from': 1, 'to': 2}, {'from': 1, 'to': 3}, {'from': 1, 'to': 10},
        {'from': 2, 'to': 3}, {'from': 2, 'to': 10}, {'from': 3, 'to': 10},
        {'from': 1, 'to': 13}, {'from': 2, 'to': 13}, {'from': 10, 'to': 13},
        {'from': 4, 'to': 5}, {'from': 4, 'to': 6}, {'from': 5, 'to': 6},
        {'from': 4, 'to': 11}, {'from': 5, 'to': 11}, {'from': 6, 'to': 11},
        {'from': 4, 'to': 14}, {'from': 5, 'to': 14}, {'from': 11, 'to': 14},
        {'from': 7, 'to': 8}, {'from': 7, 'to': 9}, {'from': 8, 'to': 9},
        {'from': 7, 'to': 12}, {'from': 8, 'to': 12}, {'from': 9, 'to': 12},
        {'from': 7, 'to': 15}, {'from': 8, 'to': 15}, {'from': 12, 'to': 15},
        {'from': 1, 'to': 4}, {'from': 3, 'to': 6}, {'from': 5, 'to': 8},
        {'from': 7, 'to': 10}, {'from': 2, 'to': 11}, {'from': 9, 'to': 14},
        {'from': 13, 'to': 15},
    ]
    return {'nodes': nodes, 'connections': connections}

# --- Minimal Enhanced Simulation ---
class EnhancedSocialClusteringSimulation:
    def __init__(self, width=1200, height=800):
        self.width = width
        self.height = height
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Social Attraction & Clustering Simulation")
        self.clock = pygame.time.Clock()
        self.space = pymunk.Space()
        self.space.gravity = (0, 0)
        self.draw_options = pymunk.pygame_util.DrawOptions(self.screen)
        self.attraction_force = 2000
        self.repulsion_force = 1500
        self.repulsion_distance = 80
        self.damping = 0.95
        self.nodes = []
        self.connections = []
        self.node_bodies = {}
        self.selected_body = None
        self.mouse_joint = None
        # Color map for groups
        self.group_colors = {'A': (255, 80, 80), 'B': (80, 255, 80), 'C': (80, 80, 255)}
        self.create_network()

    def create_network(self):
        network_data = create_social_network()
        self.nodes = network_data['nodes']
        self.connections = network_data['connections']
        for node in self.nodes:
            body = pymunk.Body(1, pymunk.moment_for_circle(1, 0, 18))
            body.position = pymunk.Vec2d(
                random.randint(100, self.width - 100),
                random.randint(100, self.height - 100)
            )
            body.velocity = pymunk.Vec2d(0, 0)
            shape = pymunk.Circle(body, 18)
            shape.elasticity = 0.8
            shape.friction = 0.7
            shape.collision_type = 1
            self.space.add(body, shape)
            self.node_bodies[node['id']] = body

    def apply_social_forces(self):
        bodies = list(self.node_bodies.values())
        for i, body1 in enumerate(bodies):
            for j, body2 in enumerate(bodies[i+1:], i+1):
                pos1 = body1.position
                pos2 = body2.position
                distance = (pos2 - pos1).length
                if distance < 1:
                    continue
                direction = (pos2 - pos1).normalized()
                node1_id = [k for k, v in self.node_bodies.items() if v == body1][0]
                node2_id = [k for k, v in self.node_bodies.items() if v == body2][0]
                is_connected = any(
                    (conn['from'] == node1_id and conn['to'] == node2_id) or
                    (conn['from'] == node2_id and conn['to'] == node1_id)
                    for conn in self.connections
                )
                if is_connected:
                    if distance > 60:
                        force_magnitude = min(self.attraction_force * (distance - 60) / 100, 1000)
                        force = direction * force_magnitude
                        body1.apply_force_at_local_point(force, (0, 0))
                        body2.apply_force_at_local_point(-force, (0, 0))
                else:
                    if distance < self.repulsion_distance:
                        force_magnitude = min(self.repulsion_force * (self.repulsion_distance - distance) / self.repulsion_distance, 800)
                        force = -direction * force_magnitude
                        body1.apply_force_at_local_point(force, (0, 0))
                        body2.apply_force_at_local_point(-force, (0, 0))
                body1.velocity = body1.velocity * self.damping
                body2.velocity = body2.velocity * self.damping

    def handle_mouse_interaction(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                mouse_pos_pymunk = pymunk.pygame_util.from_pygame(mouse_pos, self.screen)
                query_info = self.space.point_query_nearest(mouse_pos_pymunk, 0, pymunk.ShapeFilter())
                if query_info:
                    self.selected_body = query_info.shape.body
                    self.mouse_joint = pymunk.PinJoint(self.selected_body, self.space.static_body, (0, 0), mouse_pos_pymunk)
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
        for connection in self.connections:
            try:
                from_body = self.node_bodies[connection['from']]
                to_body = self.node_bodies[connection['to']]
                start_pos = pymunk.pygame_util.to_pygame(from_body.position, self.screen)
                end_pos = pymunk.pygame_util.to_pygame(to_body.position, self.screen)
                pygame.draw.line(self.screen, (100, 100, 100), start_pos, end_pos, 2)
            except Exception:
                continue
        # Draw nodes as colored circles
        for node in self.nodes:
            try:
                body = self.node_bodies[node['id']]
                pos = pymunk.pygame_util.to_pygame(body.position, self.screen)
                color = self.group_colors.get(node.get('group'), (180, 180, 180))
                pygame.draw.circle(self.screen, color, (int(pos[0]), int(pos[1])), 18)
            except Exception:
                continue
        # Draw node labels
        font = pygame.font.Font(None, 24)
        for node in self.nodes:
            try:
                body = self.node_bodies[node['id']]
                pos = pymunk.pygame_util.to_pygame(body.position, self.screen)
                text = font.render(str(node['id']), True, (255, 255, 255))
                text_rect = text.get_rect(center=(pos[0], pos[1] - 25))
                self.screen.blit(text, text_rect)
            except Exception:
                continue

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                self.handle_mouse_interaction(event)
            self.screen.fill((30, 30, 40))
            self.apply_social_forces()
            self.space.step(1/60)
            self.draw_network()
            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()

if __name__ == "__main__":
    EnhancedSocialClusteringSimulation().run() 