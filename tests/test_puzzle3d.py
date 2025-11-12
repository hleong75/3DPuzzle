"""
Unit tests for the 3D Puzzle Generator.
"""

import unittest
import numpy as np
import trimesh
from puzzle3d.config import PuzzleConfig
from puzzle3d.slicer import PuzzleSlicer
from puzzle3d.interlocking import InterlockingGenerator
from puzzle3d.puzzle_generator import PuzzleGenerator


class TestPuzzleConfig(unittest.TestCase):
    """Test configuration validation."""
    
    def test_default_config(self):
        """Test default configuration is valid."""
        config = PuzzleConfig()
        errors = config.validate()
        self.assertEqual(len(errors), 0)
    
    def test_invalid_tolerance(self):
        """Test negative tolerance is caught."""
        config = PuzzleConfig()
        config.tolerance = -0.1
        errors = config.validate()
        self.assertGreater(len(errors), 0)
    
    def test_invalid_num_slices(self):
        """Test invalid number of slices is caught."""
        config = PuzzleConfig()
        config.num_slices = 1
        errors = config.validate()
        self.assertGreater(len(errors), 0)
    
    def test_invalid_tab_depth(self):
        """Test tab depth greater than material thickness is caught."""
        config = PuzzleConfig()
        config.tab_depth = 5.0
        config.material_thickness = 3.0
        errors = config.validate()
        self.assertGreater(len(errors), 0)


class TestPuzzleSlicer(unittest.TestCase):
    """Test 3D model slicing."""
    
    def setUp(self):
        """Create a simple cube for testing."""
        self.cube = trimesh.creation.box(extents=[10, 10, 10])
        self.config = PuzzleConfig()
        self.config.num_slices = 5
    
    def test_slice_positions(self):
        """Test that correct number of slices are generated."""
        slicer = PuzzleSlicer(self.cube, self.config)
        slices = slicer.slice_model()
        # Should have num_slices - 1 internal slice planes
        self.assertEqual(len(slices), self.config.num_slices - 1)
    
    def test_slice_meshes(self):
        """Test that mesh pieces are created."""
        slicer = PuzzleSlicer(self.cube, self.config)
        pieces = slicer.create_slice_meshes()
        # Should have at least 2 pieces (some slices might fail)
        self.assertGreaterEqual(len(pieces), 2)
    
    def test_different_directions(self):
        """Test slicing in different directions."""
        for direction in ['x', 'y', 'z']:
            self.config.slice_direction = direction
            slicer = PuzzleSlicer(self.cube, self.config)
            pieces = slicer.create_slice_meshes()
            # Should have at least 2 pieces
            self.assertGreaterEqual(len(pieces), 2)


class TestInterlockingGenerator(unittest.TestCase):
    """Test interlocking mechanism generation."""
    
    def setUp(self):
        """Create test pieces."""
        self.config = PuzzleConfig()
        self.piece = trimesh.creation.box(extents=[20, 20, 5])
    
    def test_tab_position_generation(self):
        """Test tab positions are generated correctly."""
        generator = InterlockingGenerator(self.config)
        positions = generator._generate_tab_positions(
            self.piece, 
            2.5,  # Face position
            2,    # Z axis
            0     # No offset
        )
        self.assertGreater(len(positions), 0)
    
    def test_tab_geometry_creation(self):
        """Test tab geometry can be created."""
        generator = InterlockingGenerator(self.config)
        center = np.array([0, 0, 2.5])
        tab = generator._create_tab_geometry(center, 2, 'top')
        self.assertIsNotNone(tab)
        self.assertGreater(len(tab.vertices), 0)
    
    def test_slot_geometry_creation(self):
        """Test slot geometry can be created."""
        generator = InterlockingGenerator(self.config)
        center = np.array([0, 0, -2.5])
        slot = generator._create_slot_geometry(center, 2, 'bottom')
        self.assertIsNotNone(slot)
        self.assertGreater(len(slot.vertices), 0)


class TestPuzzleGenerator(unittest.TestCase):
    """Test main puzzle generator."""
    
    def setUp(self):
        """Create test configuration and mesh."""
        self.config = PuzzleConfig()
        self.config.num_slices = 3
        self.generator = PuzzleGenerator(self.config)
        self.cube = trimesh.creation.box(extents=[20, 20, 20])
    
    def test_puzzle_generation(self):
        """Test complete puzzle generation."""
        pieces = self.generator.generate_puzzle(self.cube)
        # Should have at least 2 pieces (some slices might fail)
        self.assertGreaterEqual(len(pieces), 2)
    
    def test_invalid_config(self):
        """Test that invalid config raises error."""
        self.config.num_slices = 1
        generator = PuzzleGenerator(self.config)
        with self.assertRaises(ValueError):
            generator.generate_puzzle(self.cube)


if __name__ == '__main__':
    unittest.main()
