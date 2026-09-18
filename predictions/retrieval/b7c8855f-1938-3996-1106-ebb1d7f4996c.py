import cadquery as cq

# Parameters
block_width = 80.0
block_depth = 50.0
block_height = 20.0
lug_width = 20.0
fillet_radius = 4.0
corner_fillet = 3.0
hole_diameter = 5.0
bolt_rows = 2
bolt_cols = 2
bolt_spacing_x = 30.0
bolt_spacing_y = 20.0
pocket_diameter = 15.0
pocket_depth = 10.0
side_pocket_width = 30.0
side_pocket_height = 20.0
side_pocket_depth = 8.0
side_pocket_circle_dia = 8.0
rib_width = 10.0
rib_height = 30.0
rib_thickness = 4.0

# Base block
base = cq.Workplane("XY").box(block_width, block_depth, block_height)

# Lug protrusion on +X side
lug = cq.Workplane("XY").box(lug_width, block_depth, block_height).translate((block_width/2 + lug_width/2, 0, 0))

# Combine base and lug
result = base.union(lug)

# 90° fillet on internal corner between base and lug (vertical edges on +X side)
result = result.edges("|Z and >X").fillet(fillet_radius)

# Corner fillet on outer vertical edges for safety
result = result.edges("|Z and <X").fillet(corner_fillet)

# Top face bolt pattern (rectangular array)
result = (
    result.faces("+Z")
    .workplane()
    .rarray(bolt_spacing_x, bolt_spacing_y, bolt_cols, bolt_rows, center=True)
    .hole(hole_diameter)
)

# Central circular pocket on bottom face (blind cut)
result = (
    result.faces("-Z")
    .workplane()
    .circle(pocket_diameter/2)
    .cutBlind(pocket_depth)
)

# Side pocket on +Y face: rectangular cut then circular cut (composite)
result = (
    result.faces("+Y")
    .workplane()
    .center(-side_pocket_width/2, -side_pocket_height/2)
    .rect(side_pocket_width, side_pocket_height)
    .cutBlind(side_pocket_depth)
)
result = (
    result.faces("+Y")
    .workplane()
    .center(0, 0)
    .circle(side_pocket_circle_dia/2)
    .cutBlind(side_pocket_depth)
)

# Reinforcing rib on -Y back face
rib = (
    cq.Workplane("XY")
    .rect(rib_width, rib_height)
    .extrude(rib_thickness)
    .translate((0, -(block_depth/2 + rib_thickness/2), 0))
)
result = result.union(rib)
