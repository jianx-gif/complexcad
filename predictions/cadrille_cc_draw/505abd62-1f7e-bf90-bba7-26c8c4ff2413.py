import cadquery as cq
outer_width = 60.0
outer_height = 80.0
outer_height = 70.0
wall_thickness = 2.0
rib_width = 10.0
rib_height = 4.0
rib_spacing = 12.0
rib_count = 6
chamfer_size = 0.5
hole_diameter = 4.0
hole_spacing = 20.0
hole_count = 4
hole_offset = 15.0
base = (
    cq.Workplane("XY")
    .rect(outer_width, outer_height)
    .extrude(outer_height)
)
rib = (
    cq.Workplane("XY")
    .rect(rib_width, outer_height)
    .extrude(rib_height)
    .translate((0, 0, outer_height))
)
combined = base.union(rib)
combined = (
    combined
    .faces(">Z")
    .workplane()
    .hole(hole_diameter)
)
combined = (
    combined
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .hole(hole_diameter)
)
combined = (
    combined
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .hole(hole_diameter)
)
result = (
    combined
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .hole(hole_diameter)
)
