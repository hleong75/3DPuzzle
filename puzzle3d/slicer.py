"""
3D model slicing functionality for puzzle generation.
"""

import numpy as np
import trimesh


class PuzzleSlicer:
    """Slices a 3D model into sections for puzzle piece generation."""
    
    def __init__(self, mesh, config):
        """
        Initialize the slicer.
        
        Args:
            mesh: trimesh.Trimesh object containing the 3D model
            config: PuzzleConfig object with slicing parameters
        """
        self.mesh = mesh
        self.config = config
        
    def slice_model(self):
        """
        Slice the 3D model into sections along the specified direction.
        
        Returns:
            List of slice planes (position, normal) tuples
        """
        # Get bounding box
        bounds = self.mesh.bounds
        
        # Determine slice direction
        direction_map = {'x': 0, 'y': 1, 'z': 2}
        axis = direction_map[self.config.slice_direction]
        
        # Calculate slice positions
        min_pos = bounds[0][axis]
        max_pos = bounds[1][axis]
        slice_positions = np.linspace(min_pos, max_pos, self.config.num_slices + 1)
        
        # Create slice planes
        slices = []
        for pos in slice_positions[1:-1]:  # Exclude the first and last boundaries
            normal = np.zeros(3)
            normal[axis] = 1.0
            point = np.zeros(3)
            point[axis] = pos
            slices.append((point, normal))
            
        return slices
    
    def create_slice_meshes(self):
        """
        Create mesh sections by slicing the original model.
        
        Returns:
            List of trimesh.Trimesh objects representing puzzle pieces
        """
        slices = self.slice_model()
        
        if not slices:
            # If no slices, return the original mesh
            return [self.mesh]
        
        pieces = []
        
        # Get axis index
        direction_map = {'x': 0, 'y': 1, 'z': 2}
        axis = direction_map[self.config.slice_direction]
        
        # Create sections between slices
        bounds = self.mesh.bounds
        min_pos = bounds[0][axis]
        max_pos = bounds[1][axis]
        
        # All slice positions including boundaries
        all_positions = [min_pos] + [s[0][axis] for s in slices] + [max_pos]
        
        for i in range(len(all_positions) - 1):
            # Create a piece between two consecutive slice positions
            piece = self._extract_piece_between_planes(
                all_positions[i], 
                all_positions[i + 1], 
                axis
            )
            if piece is not None and piece.is_volume:
                pieces.append(piece)
        
        return pieces
    
    def _extract_piece_between_planes(self, pos1, pos2, axis):
        """
        Extract the mesh section between two parallel planes.
        
        Args:
            pos1: Position of first plane
            pos2: Position of second plane
            axis: Axis perpendicular to planes (0=x, 1=y, 2=z)
            
        Returns:
            trimesh.Trimesh object or None
        """
        try:
            # Create a copy of the mesh
            piece = self.mesh.copy()
            
            # Use a different approach: filter vertices by position
            # This is more robust than slice_plane for simple cases
            vertices = piece.vertices.copy()
            
            # Get vertices within the bounds
            mask = (vertices[:, axis] >= pos1) & (vertices[:, axis] <= pos2)
            
            if not mask.any():
                return None
            
            # For now, use a simpler approach: just slice at the boundaries
            # Create plane normals
            normal_pos = np.zeros(3)
            normal_pos[axis] = 1.0
            normal_neg = np.zeros(3)
            normal_neg[axis] = -1.0
            
            # Create plane origins
            origin_pos = np.zeros(3)
            origin_pos[axis] = pos1
            origin_neg = np.zeros(3)
            origin_neg[axis] = pos2
            
            # Slice from below (keep upper part)
            result = piece.slice_plane(origin_pos, normal_pos, cap=True)
            
            if result is None or not isinstance(result, trimesh.Trimesh):
                return None
                
            # Slice from above (keep lower part)
            result = result.slice_plane(origin_neg, normal_neg, cap=True)
            
            if result is None or not isinstance(result, trimesh.Trimesh):
                return None
            
            return result
            
        except Exception as e:
            print(f"Warning: Could not extract piece between {pos1} and {pos2}: {e}")
            return None
    
    def get_slice_boundaries(self):
        """
        Get the boundary information for each slice.
        
        Returns:
            List of (min_bound, max_bound, slice_index) tuples
        """
        slices = self.slice_model()
        direction_map = {'x': 0, 'y': 1, 'z': 2}
        axis = direction_map[self.config.slice_direction]
        
        bounds = self.mesh.bounds
        min_pos = bounds[0][axis]
        max_pos = bounds[1][axis]
        
        all_positions = [min_pos] + [s[0][axis] for s in slices] + [max_pos]
        
        boundaries = []
        for i in range(len(all_positions) - 1):
            boundaries.append((all_positions[i], all_positions[i + 1], i))
            
        return boundaries
