"""
Script to generate example 3D models for testing.
"""

import trimesh
import numpy as np
import os

# Create examples directory
os.makedirs('examples', exist_ok=True)

# Example 1: Simple cube
print("Creating simple cube...")
cube = trimesh.creation.box(extents=[30, 30, 30])
cube.export('examples/cube.stl')
print("  Saved: examples/cube.stl")

# Example 2: Cylinder
print("Creating cylinder...")
cylinder = trimesh.creation.cylinder(radius=15, height=40, sections=32)
cylinder.export('examples/cylinder.stl')
print("  Saved: examples/cylinder.stl")

# Example 3: Sphere
print("Creating sphere...")
sphere = trimesh.creation.icosphere(subdivisions=3, radius=20)
sphere.export('examples/sphere.stl')
print("  Saved: examples/sphere.stl")

# Example 4: Torus
print("Creating torus...")
torus = trimesh.creation.torus(major_radius=20, minor_radius=5, major_sections=32, minor_sections=16)
torus.export('examples/torus.stl')
print("  Saved: examples/torus.stl")

print("\nExample models created successfully!")
