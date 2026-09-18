import cadquery as cq
outer_diameter = 40.0
inner_diameter = 30.0
thickness = 20.0
wall_thickness = 3.0
fillet_radius = 2.0
chamfer_distance = 1.0
mount_hole_diameter = 5.0
mount_hole_offset = 10.0
rib_width = 6.0
rib_height = 12.0
rib_thickness = 2.0
rib_spacing = 15.0
rib_count = 4
outer_radius = outer_diameter / 2.0
inner_radius = inner_diameter / 2.0
base = (
    cq.Workplane("XY")
    .rect(outer_diameter, outer_diameter)
    .extrude(thickness)
)
base = (
    base
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(inner_diameter, inner_diameter)
    .cutBlind(-thickness)
)
rib = (
    cq.Workplane("XY")
    .rect(rib_width, rib_height)
    .extrude(rib_thickness)
    .translate((0, 0, thickness))
)
rib_pattern = rib.translate((0, 0, thickness))
rib_pattern = rib_pattern.union(rib)
result = base.union(rib_pattern)
result = result.edges("|Z").fillet(fillet_radius)
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints([(-mount_hole_offset, 0), (mount_hole_offset, 0)])
    .hole(mount_hole_diameter)
)
result = result.edges("|Z").chamfer(chamfer_distance)
