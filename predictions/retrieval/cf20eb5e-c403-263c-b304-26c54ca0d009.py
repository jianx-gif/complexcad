import cadquery as cq

# Core dimensions (units are scaled, max 100)
plate_length = 80.0
plate_width = 60.0
plate_thickness = 5.0
rib_margin = 5.0
rib_width = 20.0
rib_thickness = 3.0
hole_diameter = 8.0
hole_spacing = 30.0
hole_offset_y = 0.0
chamfer_distance = 0.5

# Derived dimensions
rib_length = plate_length - 2 * rib_margin
total_thickness = plate_thickness + rib_thickness

# Base plate solid
base_plate = (
    cq.Workplane('XY')
    .rect(plate_length, plate_width)
    .extrude(plate_thickness)
)

# Stiffening rib (centered longitudinally, raised on top face)
rib = (
    cq.Workplane('XY')
    .center(0, 0)
    .rect(rib_length, rib_width)
    .extrude(rib_thickness)
    .translate((0, 0, plate_thickness))
)

# Combine base and rib
plate_with_rib = base_plate.union(rib)

# Create through holes (three equally spaced along X)
hole_positions = [
    (-hole_spacing / 2, hole_offset_y),
    (0, hole_offset_y),
    (hole_spacing / 2, hole_offset_y),
]

holes = (
    cq.Workplane('XY')
    .pushPoints(hole_positions)
    .circle(hole_diameter / 2)
    .extrude(total_thickness)
)

# Subtract holes from the combined solid
plate_with_holes = plate_with_rib.cut(holes)

# Add chamfers to all exterior edges for safety
result = (
    plate_with_holes
    .edges()
    .chamfer(chamfer_distance)
)
