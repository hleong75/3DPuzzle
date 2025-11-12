"""
Configuration settings for 3D puzzle generation.
"""

class PuzzleConfig:
    """Configuration for puzzle generation with default values suitable for wood manufacturing."""
    
    def __init__(self):
        # Cutting and manufacturing tolerances (in mm)
        self.tolerance = 0.2  # Tolerance for interlocking parts
        self.kerf_width = 0.1  # Laser/saw blade width
        
        # Material properties
        self.material_thickness = 3.0  # Default wood thickness in mm
        self.min_piece_size = 10.0  # Minimum piece dimension in mm
        
        # Interlocking mechanism
        self.tab_width = 5.0  # Width of tabs in mm
        self.tab_depth = 1.5  # Depth of tabs (should be < material_thickness)
        self.tab_spacing = 15.0  # Spacing between tabs in mm
        
        # Puzzle complexity
        self.num_slices = 10  # Number of slices to divide the model into
        self.slice_direction = 'z'  # Direction to slice: 'x', 'y', or 'z'
        
        # Output settings
        self.export_format = 'stl'  # Export format: 'stl' or 'dxf'
        self.separate_pieces = True  # Export each piece as separate file
        
    def validate(self):
        """Validate configuration parameters."""
        errors = []
        
        if self.tolerance < 0:
            errors.append("Tolerance must be positive")
        if self.material_thickness <= 0:
            errors.append("Material thickness must be positive")
        if self.tab_depth >= self.material_thickness:
            errors.append("Tab depth must be less than material thickness")
        if self.num_slices < 2:
            errors.append("Number of slices must be at least 2")
        if self.slice_direction not in ['x', 'y', 'z']:
            errors.append("Slice direction must be 'x', 'y', or 'z'")
            
        return errors
