"""
Test script for the Social Clustering Simulation

This script tests:
1. Import functionality
2. Network data creation
3. Basic simulation initialization
4. Parameter validation
"""

import sys
import traceback

def test_imports():
    """Test that all required modules can be imported"""
    print("Testing imports...")
    
    try:
        import pygame
        print("✓ Pygame imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import pygame: {e}")
        return False
    
    try:
        import pymunk
        print("✓ Pymunk imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import pymunk: {e}")
        return False
    
    try:
        from social_network_data import create_social_network, create_clique_network, create_large_network
        print("✓ Social network data imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import social_network_data: {e}")
        return False
    
    try:
        from main import SocialClusteringSimulation
        print("✓ Basic simulation imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import basic simulation: {e}")
        return False
    
    try:
        from main_enhanced import EnhancedSocialClusteringSimulation
        print("✓ Enhanced simulation imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import enhanced simulation: {e}")
        return False
    
    return True

def test_network_data():
    """Test network data creation"""
    print("\nTesting network data creation...")
    
    try:
        from social_network_data import create_social_network, create_clique_network, create_large_network
        
        # Test basic network
        basic_network = create_social_network()
        assert 'nodes' in basic_network
        assert 'connections' in basic_network
        assert len(basic_network['nodes']) > 0
        print(f"✓ Basic network created: {len(basic_network['nodes'])} nodes, {len(basic_network['connections'])} connections")
        
        # Test clique network
        clique_network = create_clique_network()
        assert 'nodes' in clique_network
        assert 'connections' in clique_network
        print(f"✓ Clique network created: {len(clique_network['nodes'])} nodes, {len(clique_network['connections'])} connections")
        
        # Test large network
        large_network = create_large_network(20, 0.3)
        assert 'nodes' in large_network
        assert 'connections' in large_network
        print(f"✓ Large network created: {len(large_network['nodes'])} nodes, {len(large_network['connections'])} connections")
        
        return True
        
    except Exception as e:
        print(f"✗ Network data test failed: {e}")
        traceback.print_exc()
        return False

def test_simulation_initialization():
    """Test simulation initialization without running"""
    print("\nTesting simulation initialization...")
    
    try:
        from main import SocialClusteringSimulation
        
        # Test basic simulation
        simulation = SocialClusteringSimulation(width=800, height=600)
        assert simulation.width == 800
        assert simulation.height == 600
        assert simulation.attraction_force > 0
        assert simulation.repulsion_force > 0
        assert len(simulation.nodes) > 0
        assert len(simulation.connections) > 0
        print("✓ Basic simulation initialized successfully")
        
        return True
        
    except Exception as e:
        print(f"✗ Simulation initialization test failed: {e}")
        traceback.print_exc()
        return False

def test_enhanced_simulation_initialization():
    """Test enhanced simulation initialization"""
    print("\nTesting enhanced simulation initialization...")
    
    try:
        from main_enhanced import EnhancedSocialClusteringSimulation
        
        # Test enhanced simulation
        simulation = EnhancedSocialClusteringSimulation(width=1000, height=700)
        assert simulation.width == 1000
        assert simulation.height == 700
        assert len(simulation.group_colors) > 0
        assert simulation.current_network == 0
        print("✓ Enhanced simulation initialized successfully")
        
        return True
        
    except Exception as e:
        print(f"✗ Enhanced simulation initialization test failed: {e}")
        traceback.print_exc()
        return False

def test_parameter_validation():
    """Test parameter validation and edge cases"""
    print("\nTesting parameter validation...")
    
    try:
        from main import SocialClusteringSimulation
        
        # Test with very small window
        simulation = SocialClusteringSimulation(width=400, height=300)
        assert simulation.width == 400
        assert simulation.height == 300
        print("✓ Small window size handled correctly")
        
        # Test parameter modification
        simulation.attraction_force = 10000
        simulation.repulsion_force = 5000
        simulation.damping = 0.99
        assert simulation.attraction_force == 10000
        assert simulation.repulsion_force == 5000
        assert simulation.damping == 0.99
        print("✓ Parameter modification works correctly")
        
        return True
        
    except Exception as e:
        print(f"✗ Parameter validation test failed: {e}")
        traceback.print_exc()
        return False

def run_all_tests():
    """Run all tests and report results"""
    print("Social Clustering Simulation - Test Suite")
    print("=" * 50)
    
    tests = [
        ("Import Test", test_imports),
        ("Network Data Test", test_network_data),
        ("Basic Simulation Test", test_simulation_initialization),
        ("Enhanced Simulation Test", test_enhanced_simulation_initialization),
        ("Parameter Validation Test", test_parameter_validation),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            if test_func():
                passed += 1
                print(f"✓ {test_name} PASSED")
            else:
                print(f"✗ {test_name} FAILED")
        except Exception as e:
            print(f"✗ {test_name} FAILED with exception: {e}")
            traceback.print_exc()
    
    print(f"\n{'='*50}")
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The simulation is ready to run.")
        print("\nTo run the simulation:")
        print("  python main.py              # Basic simulation")
        print("  python main_enhanced.py     # Enhanced simulation")
        print("  python examples.py          # Interactive examples")
    else:
        print("❌ Some tests failed. Please check the error messages above.")
        return False
    
    return True

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1) 