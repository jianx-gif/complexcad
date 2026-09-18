import cadquery as cq
clip_length = 80.0
clip_width = 30.0
clip_thickness = 5.0
hole_diameter = 4.0
hole_spacing_x = 20.0
hole_spacing_y = 12.0
hole_rows = 2
hole_cols = 3
chamfer_size = 0.8
rib_width = 6.0
rib_height = 3.0
rib_length = clip_length - 2 * rib_width
rib_depth = clip_thickness - 2 * rib_width
base = (
    cq.Workplane("XY")
    .rect(clip_length, clip_width)
    .extrude(clip_thickness)
    .edges("|Z")
    .fillet(0.5)
)
hole_positions = [
    (-hole_spacing_x/2, -hole_spacing_y/2),
    ( hole_spacing_x/2, -hole_spacing_y/2),
    (-hole_spacing_x/2, hole_spacing_y/2),
    ( hole_spacing_x/2, hole_spacing_y/2),
]
base = (
    base.faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .circle(hole_diameter/2)
    .cutBlind(-clip_thickness)
)
rib = (
    cq.Workplane("XY")
    .rect(rib_width, rib_length)
    .extrude(rib_depth)
    .translate((0, 0, rib_depth))
)
result = base.union(rib)
result = result.edges("|Z").chamfer(chamfer_size)
