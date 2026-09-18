import cadquery as cq
outer_diameter = 50.0
inner_diameter = 30.0
wall_thickness = 5.0
rib_height = 8.0
rib_width = 12.0
rib_thickness = 2.0
rib_spacing = 12.0
chamfer_size = 1.0
hole_diameter = 4.0
hole_spacing = 15.0
hole_count = 6
hole_offset = 10.0
base = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2)
    .extrude(outer_diameter)
)
rib = (
    cq.Workplane("XY")
    .center(outer_diameter / 2 - wall_thickness / 2, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_thickness)
)
rib = rib.translate((outer_diameter / 2 - wall_thickness / 2, 0, 0))
combined = base.union(rib)
combined = (
    combined
    .faces(">Z")
    .workplane()
    .pushPoints([(-hole_spacing / 2, 0), (hole_spacing / 2, 0)])
    .hole(hole_diameter)
)
combined = combined.edges("|Z").chamfer(chamfer_size)
hole_positions = [
    (inner_diameter / 2 + wall_thickness + i * hole_spacing, 0)
    for i in range(hole_count)
]
result = (
    combined
    .faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
