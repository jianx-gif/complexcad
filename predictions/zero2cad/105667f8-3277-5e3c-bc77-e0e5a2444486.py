import cadquery as cq

# Parameters
base_length = 80.0
base_width = 60.0
base_thickness = 10.0
rib_length = 50.0
rib_width = 20.0
rib_height = 5.0
hole_diameter = 6.0
hole_spacing = 40.0
fillet_radius = 2.0
chamfer_distance = 1.0
side_hole_diameter = 4.0
side_hole_offset = 15.0
side_hole_spacing = 30.0
side_hole_count = 2
tab_length = 15.0
tab_width = 10.0
tab_thickness = 5.0

# Base plate
result = (
    cq.Workplane("XY")
    .rect(base_length, base_width)
    .extrude(base_thickness)
)

# Central rib on bottom face
result = (
    result
    .faces("<Z")
    .workplane()
    .rect(rib_length, rib_width)
    .extrude(rib_height)
)

# Through holes on top face
result = (
    result
    .faces(">Z")
    .workplane()
    .pushPoints([(-hole_spacing/2, 0), (hole_spacing/2, 0)])
    .hole(hole_diameter)
)

# Fillet vertical edges of the main body (before adding tab)
result = result.edges("|Z").fillet(fillet_radius)

# Side mounting tab on +Y face
result = (
    result
    .faces(">Y")
    .workplane()
    .rect(tab_thickness, tab_width)
    .extrude(tab_length)
)

# Side mounting holes on -Y face
result = (
    result
    .faces("<Y")
    .workplane()
    .center(-base_length/2 + side_hole_offset, 0)
    .rarray(side_hole_spacing, 0, side_hole_count, 1)
    .hole(side_hole_diameter)
)

# Chamfer top edges
result = result.edges(">Z").chamfer(chamfer_distance)
