import cadquery as cq
outer_diameter = 40.0
inner_diameter = 30.0
thickness = 6.0
rib_width = 4.0
rib_height = 2.0
rib_spacing = 12.0
rib_count = 6
rib_count = 8
chamfer_size = 0.5
hole_diameter = 5.0
hole_spacing = 12.0
hole_offset = 10.0
base = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2)
    .extrude(thickness)
)
rib = (
    cq.Workplane("XY")
    .center(0, 0)
    .rect(rib_width, rib_height)
    .extrude(thickness)
)
rib = rib.translate((0, 0, thickness))
rib = rib.translate((0, 0, thickness))
rib = rib.translate((0, 0, thickness))
combined = base.union(rib)
combined = combined.edges("|Z").chamfer(chamfer_size)
combined = combined.faces(">Z").workplane().hole(hole_diameter)
combined = combined.faces(">Z").workplane().hole(hole_diameter)
combined = combined.faces(">Z").workplane().center(0, 0).hole(hole_diameter)
result = combined
