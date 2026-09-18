import cadquery as cq

bracket_length = 80.0
bracket_width = 50.0
bracket_thickness = 8.0
cavity_width = 40.0
cavity_height = 30.0
hole_diameter = 6.0
hole_spacing = 30.0
hole_offset_y = -15.0
fillet_radius = 2.0
chamfer_distance = 0.8

profile = (
    cq.Sketch()
    .rect(bracket_length, bracket_width)
    .rect(cavity_width, cavity_height, mode="s")
)

base = (
    cq.Workplane("XY")
    .placeSketch(profile)
    .extrude(bracket_thickness)
)

chamfered = base.faces(">Z").edges().chamfer(chamfer_distance)

filleted = chamfered.faces(">Z").edges().fillet(fillet_radius)

with_holes = (
    filleted.faces("+Z")
    .workplane()
    .pushPoints([(-hole_spacing/2, hole_offset_y), (hole_spacing/2, hole_offset_y)])
    .hole(hole_diameter)
)

result = with_holes
