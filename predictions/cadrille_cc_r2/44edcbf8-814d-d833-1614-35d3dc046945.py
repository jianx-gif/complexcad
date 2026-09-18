import cadquery as cq
outer_diameter = 30.0
inner_diameter = 20.0
wall_thickness = 2.0
fillet_radius = 2.0
chamfer_distance = 0.5
hole_diameter = 4.0
hole_spacing = 12.0
hole_offset = 10.0
rib_width = 6.0
rib_height = 4.0
rib_thickness = 2.0
rib_spacing = 15.0
rib_count = int((outer_diameter - 2 * wall_thickness) // rib_spacing)
base = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2)
    .extrude(wall_thickness)
)
rib = (
    cq.Workplane("XY")
    .rect(rib_width, rib_height)
    .extrude(wall_thickness)
)
rib = rib.translate((0, 0, wall_thickness))
combined = base.union(rib)
combined = combined.edges("|Z").fillet(fillet_radius)
combined = (
    combined.faces(">Z")
    .workplane()
    .rarray(hole_spacing, 0, hole_offset, 1, center=True)
    .hole(hole_diameter)
)
combined = combined.edges("|Z").chamfer(chamfer_distance)
result = combined
