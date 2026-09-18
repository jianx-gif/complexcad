import cadquery as cq

# Parameters
base_length = 80.0
base_width = 40.0
base_thickness = 8.0
flange_radius = 30.0
flange_thickness = 6.0
hole_diameter = 6.0
hole_clearance = 0.5
hole_spacing_x = 50.0
hole_spacing_y = 20.0
chamfer_size = 1.0
rib_height = 5.0
rib_thickness = 3.0
rib_offset = 10.0

# Base loft between rectangle and circle
base = (
    cq.Workplane("XY")
    .rect(base_length, base_width)
    .workplane(offset=base_thickness)
    .circle(flange_radius)
    .loft()
)

# Flange extrusion on top of base
flange = (
    cq.Workplane("XY")
    .workplane(offset=base_thickness)
    .circle(flange_radius)
    .extrude(flange_thickness)
)

# Combine base and flange
bracket = base.union(flange)

# Add four clearance holes on the top face of the flange
hole_positions = [
    (-hole_spacing_x/2, -hole_spacing_y/2),
    ( hole_spacing_x/2, -hole_spacing_y/2),
    (-hole_spacing_x/2,  hole_spacing_y/2),
    ( hole_spacing_x/2,  hole_spacing_y/2),
]
bracket = (
    bracket
    .faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter + hole_clearance)
)

# Add a reinforcing rib on the underside of the base
rib = (
    cq.Workplane("XY")
    .workplane(offset=0)
    .center(-base_length/2 + rib_offset, 0)
    .rect(rib_thickness, rib_height)
    .extrude(-rib_thickness)
)
bracket = bracket.union(rib)

# Apply chamfer to all vertical edges
bracket = bracket.edges("|Z").chamfer(chamfer_size)

result = bracket