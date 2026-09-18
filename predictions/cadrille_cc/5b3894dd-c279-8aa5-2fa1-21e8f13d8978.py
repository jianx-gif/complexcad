import cadquery as cq
outer_diameter = 60.0
inner_diameter = 30.0
thickness = 15.0
wall_thickness = 2.0
fillet_radius = 2.0
chamfer_distance = 1.0
mount_hole_diameter = 5.0
mount_hole_offset = 10.0
rib_width = 10.0
rib_height = 5.0
rib_thickness = 2.0
rib_spacing = 12.0
rib_count = 4
outer_radius = outer_diameter / 2.0
inner_radius = inner_diameter / 2.0
base = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(thickness)
)
base = (
    base
    .faces(">Z")
    .workplane()
    .hole(inner_diameter)
)
base = (
    base
    .faces(">Z")
    .workplane()
    .hole(inner_diameter)
)
rib = (
    cq.Workplane("XY")
    .rect(rib_width, rib_height)
    .extrude(rib_thickness)
    .translate((0, 0, thickness))
)
base = base.union(rib)
base = (
    base
    .faces(">Z")
    .workplane()
    .hole(mount_hole_diameter)
)
base = (
    base
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_thickness)
)
base = base.union(base)
base = base.edges("|Z").fillet(fillet_radius)
result = base
