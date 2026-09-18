import cadquery as cq
outer_diameter = 80.0
inner_diameter = 30.0
thickness = 10.0
wall_thickness = 2.0
fillet_radius = 2.0
chamfer_distance = 0.5
hole_diameter = 4.0
hole_spacing = 20.0
hole_offset = 15.0
rib_width = 6.0
rib_height = 4.0
rib_thickness = 2.0
rib_spacing = 12.0
rib_count = int((outer_diameter - 2 * wall_thickness) // rib_spacing)
base = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2)
    .extrude(thickness)
)
base = base.edges("|Z").fillet(fillet_radius)
base = (
    base.faces(">Z")
    .workplane()
    .circle(inner_diameter / 2)
    .cutBlind(-thickness)
)
base = (
    base.faces(">Z")
    .workplane()
    .circle(inner_diameter / 2)
    .cutBlind(-thickness)
)
rib = (
    cq.Workplane("XY")
    .rect(rib_width, rib_height)
    .extrude(rib_thickness)
    .translate((0, 0, thickness - rib_height))
)
base = base.union(rib)
hole_positions = [
    (hole_offset, hole_offset),
    (-hole_offset, hole_offset),
    (hole_offset, -hole_offset),
    (hole_offset, hole_offset),
]
base = (
    base.faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
base = base.edges("|Z").chamfer(chamfer_distance)
result = base
