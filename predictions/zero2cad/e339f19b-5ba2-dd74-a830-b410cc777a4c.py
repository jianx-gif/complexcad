import cadquery as cq

handle_length = 80.0
handle_width = 30.0
handle_height = 20.0
grip_radius = 15.0
fillet_radius = 2.0
chamfer_distance = 1.0
hole_diameter = 5.0
hole_spacing = 20.0
hole_count = 3
rib_width = 5.0
rib_height = 10.0
rib_depth = 3.0
rib_spacing = 15.0

base = (
    cq.Workplane("XY")
    .rect(handle_width, handle_height)
    .extrude(handle_length)
)

grip = (
    cq.Workplane("XY")
    .center(0, 0)
    .circle(grip_radius)
    .extrude(handle_length)
)

result = base.union(grip)

result = result.edges("|Z").fillet(fillet_radius)

result = (
    result.faces(">X")
    .workplane()
    .rarray(hole_spacing, 0, hole_count, 1)
    .hole(hole_diameter)
)

result = (
    result.faces("<X")
    .workplane()
    .rarray(hole_spacing, 0, hole_count, 1)
    .hole(hole_diameter)
)

result = (
    result.faces(">Y")
    .workplane()
    .rarray(rib_spacing, 0, int(handle_length / rib_spacing), 1)
    .rect(rib_width, rib_height)
    .cutBlind(rib_depth)
)

result = result.edges("|X or |Y").chamfer(chamfer_distance)
