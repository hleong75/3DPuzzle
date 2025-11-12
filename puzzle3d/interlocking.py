"""
Interlocking mechanism generation for puzzle pieces.
"""

import numpy as np
import trimesh
from scipy.spatial import ConvexHull


class InterlockingGenerator:
    """Generates interlocking tabs and slots for puzzle pieces."""
    
    def __init__(self, config):
        """
        Initialize the interlocking generator.
        
        Args:
            config: PuzzleConfig object with interlocking parameters
        """
        self.config = config
    
    def add_interlocking_features(self, pieces):
        """
        Add interlocking tabs and slots to adjacent puzzle pieces.
        
        Args:
            pieces: List of trimesh.Trimesh objects representing puzzle pieces
            
        Returns:
            List of modified trimesh.Trimesh objects with interlocking features
        """
        if len(pieces) < 2:
            return pieces
        
        modified_pieces = []
        
        for i, piece in enumerate(pieces):
            modified_piece = piece.copy()
            
            # Add tabs to the top face (connects to next piece)
            if i < len(pieces) - 1:
                modified_piece = self._add_tabs_to_face(
                    modified_piece, 
                    direction='top',
                    pattern_offset=i % 2  # Alternate pattern
                )
            
            # Add slots to the bottom face (connects to previous piece)
            if i > 0:
                modified_piece = self._add_slots_to_face(
                    modified_piece,
                    direction='bottom',
                    pattern_offset=(i - 1) % 2  # Match previous piece's tabs
                )
            
            modified_pieces.append(modified_piece)
        
        return modified_pieces
    
    def _add_tabs_to_face(self, mesh, direction='top', pattern_offset=0):
        """
        Add tabs (protrusions) to a face of the mesh.
        
        Args:
            mesh: trimesh.Trimesh object
            direction: 'top' or 'bottom'
            pattern_offset: Offset for alternating pattern
            
        Returns:
            Modified trimesh.Trimesh object
        """
        try:
            # Get the face to add tabs to
            bounds = mesh.bounds
            direction_map = {'x': 0, 'y': 1, 'z': 2}
            axis = direction_map[self.config.slice_direction]
            
            if direction == 'top':
                face_position = bounds[1][axis]
            else:
                face_position = bounds[0][axis]
            
            # Create tabs along the face
            tabs = self._generate_tab_positions(mesh, face_position, axis, pattern_offset)
            
            # Create tab geometries and union with mesh
            for tab_center in tabs:
                tab_mesh = self._create_tab_geometry(tab_center, axis, direction)
                if tab_mesh is not None:
                    try:
                        mesh = trimesh.boolean.union([mesh, tab_mesh], engine='blender')
                    except:
                        # If boolean fails, try simple concatenation
                        mesh = mesh + tab_mesh
            
            return mesh
            
        except Exception as e:
            print(f"Warning: Could not add tabs: {e}")
            return mesh
    
    def _add_slots_to_face(self, mesh, direction='bottom', pattern_offset=0):
        """
        Add slots (indentations) to a face of the mesh.
        
        Args:
            mesh: trimesh.Trimesh object
            direction: 'top' or 'bottom'
            pattern_offset: Offset for alternating pattern
            
        Returns:
            Modified trimesh.Trimesh object
        """
        try:
            # Get the face to add slots to
            bounds = mesh.bounds
            direction_map = {'x': 0, 'y': 1, 'z': 2}
            axis = direction_map[self.config.slice_direction]
            
            if direction == 'top':
                face_position = bounds[1][axis]
            else:
                face_position = bounds[0][axis]
            
            # Create slots along the face
            slots = self._generate_tab_positions(mesh, face_position, axis, pattern_offset)
            
            # Create slot geometries and subtract from mesh
            for slot_center in slots:
                slot_mesh = self._create_slot_geometry(slot_center, axis, direction)
                if slot_mesh is not None:
                    try:
                        mesh = trimesh.boolean.difference([mesh, slot_mesh], engine='blender')
                    except:
                        # If boolean fails, skip this slot
                        print(f"Warning: Could not create slot at {slot_center}")
            
            return mesh
            
        except Exception as e:
            print(f"Warning: Could not add slots: {e}")
            return mesh
    
    def _generate_tab_positions(self, mesh, face_position, axis, offset=0):
        """
        Generate positions for tabs/slots along a face.
        
        Args:
            mesh: trimesh.Trimesh object
            face_position: Position of the face along the slice axis
            axis: Slice axis (0=x, 1=y, 2=z)
            offset: Pattern offset for alternating tabs
            
        Returns:
            List of 3D positions for tab/slot centers
        """
        bounds = mesh.bounds
        positions = []
        
        # Determine the two axes perpendicular to slice axis
        axes = [0, 1, 2]
        axes.remove(axis)
        axis1, axis2 = axes
        
        # Get the range along the perpendicular axes
        min1, max1 = bounds[0][axis1], bounds[1][axis1]
        min2, max2 = bounds[0][axis2], bounds[1][axis2]
        
        # Use the longer dimension for tab placement
        if (max1 - min1) > (max2 - min2):
            primary_axis = axis1
            min_pos, max_pos = min1, max1
            secondary_pos = (min2 + max2) / 2
            secondary_axis = axis2
        else:
            primary_axis = axis2
            min_pos, max_pos = min2, max2
            secondary_pos = (min1 + max1) / 2
            secondary_axis = axis1
        
        # Calculate tab positions with spacing
        total_length = max_pos - min_pos
        num_tabs = max(1, int(total_length / self.config.tab_spacing))
        
        if num_tabs > 0:
            spacing = total_length / (num_tabs + 1)
            start_offset = spacing * (0.5 + offset * 0.5)  # Alternate pattern
            
            for i in range(num_tabs):
                pos = np.zeros(3)
                pos[axis] = face_position
                pos[primary_axis] = min_pos + start_offset + i * spacing
                pos[secondary_axis] = secondary_pos
                positions.append(pos)
        
        return positions
    
    def _create_tab_geometry(self, center, axis, direction):
        """
        Create a tab (protrusion) geometry.
        
        Args:
            center: 3D position of tab center
            axis: Slice axis
            direction: 'top' or 'bottom'
            
        Returns:
            trimesh.Trimesh object representing the tab
        """
        try:
            # Create a box representing the tab
            tab_size = [self.config.tab_width, self.config.tab_width, self.config.tab_depth]
            
            # Adjust size based on axis
            axes = [0, 1, 2]
            axes.remove(axis)
            
            extents = np.array([1.0, 1.0, 1.0])
            extents[axes[0]] = self.config.tab_width
            extents[axes[1]] = self.config.tab_width
            extents[axis] = self.config.tab_depth
            
            # Adjust tolerance for fit
            extents[axes[0]] -= self.config.tolerance
            extents[axes[1]] -= self.config.tolerance
            
            tab = trimesh.creation.box(extents=extents)
            
            # Position the tab
            offset = np.array(center)
            if direction == 'top':
                offset[axis] += self.config.tab_depth / 2
            else:
                offset[axis] -= self.config.tab_depth / 2
            
            tab.apply_translation(offset)
            
            return tab
            
        except Exception as e:
            print(f"Warning: Could not create tab geometry: {e}")
            return None
    
    def _create_slot_geometry(self, center, axis, direction):
        """
        Create a slot (indentation) geometry.
        
        Args:
            center: 3D position of slot center
            axis: Slice axis
            direction: 'top' or 'bottom'
            
        Returns:
            trimesh.Trimesh object representing the slot
        """
        try:
            # Create a box representing the slot (slightly larger than tab for tolerance)
            axes = [0, 1, 2]
            axes.remove(axis)
            
            extents = np.array([1.0, 1.0, 1.0])
            extents[axes[0]] = self.config.tab_width
            extents[axes[1]] = self.config.tab_width
            extents[axis] = self.config.tab_depth
            
            # Add tolerance for fit
            extents[axes[0]] += self.config.tolerance
            extents[axes[1]] += self.config.tolerance
            
            slot = trimesh.creation.box(extents=extents)
            
            # Position the slot
            offset = np.array(center)
            if direction == 'top':
                offset[axis] += self.config.tab_depth / 2
            else:
                offset[axis] -= self.config.tab_depth / 2
            
            slot.apply_translation(offset)
            
            return slot
            
        except Exception as e:
            print(f"Warning: Could not create slot geometry: {e}")
            return None
