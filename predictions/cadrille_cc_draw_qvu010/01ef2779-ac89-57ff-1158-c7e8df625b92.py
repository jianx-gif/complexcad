import cadquery as cq
base_length = 80.0
base_width = 40.0
base_thickness = 15.0
wall_thickness = 2.0
chamfer_distance = 1.0
hole_diameter = 5.0
hole_spacing = 12.0
hole_offset = 10.0
rib_width = 6.0
rib_height = 4.0
rib_spacing = 12.0
base = (
    cq.Workplane("XY")
    .rect(base_length, base_width)
    .extrude(base_thickness)
)
base = base.edges("|Z").chamfer(chamfer_distance)
base = (
    base.faces(">Z")
    .workplane()
    .rect(base_length - 2 * wall_thickness, base_width - 2 * wall_thickness)
    .cutBlind(-base_thickness)
)
rib = (
    base.faces(">Z")
    .workplane()
    .rect(rib_width, rib_height)
    .extrude(rib_height)
)
rib = rib.edges("|Z").chamfer(chamfer_distance)
hole_positions = [
    (hole_offset,  hole_offset),
    (-hole_offset,  hole_offset),
    (hole_offset, -hole_offset),
    (-hole_offset, -hole_offset),
]
result = (
    base.faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
