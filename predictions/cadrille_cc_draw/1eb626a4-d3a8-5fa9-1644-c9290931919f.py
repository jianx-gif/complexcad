import cadquery as cq
outer_diameter = 40.0
inner_diameter = 30.0
thickness = 2.0
rib_height = 5.0
rib_width = 6.0
rib_spacing = 12.0
rib_count = 12
chamfer_distance = 0.5
rib_count = 4
rib_spacing = 12.0
rib_count = 6
profile = (
    cq.Workplane("XZ")
    .moveTo(outer_diameter/2, 0)
    .lineTo(outer_diameter/2, thickness)
    .lineTo(outer_diameter/2, thickness + rib_height)
    .lineTo(outer_diameter/2, 0)
    .close()
)
result = profile.revolve()
rib = (
    cq.Workplane("XY")
    .center(outer_diameter/2 + rib_spacing/2, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_height)
)
result = result.union(rib)
result = (
    result.faces(">Z")
    .workplane()
    .center(outer_diameter/2 - rib_spacing/2, 0)
    .rect(rib_width, rib_height)
    .cutBlind(-rib_height)
)
result = (
    result.faces(">Z")
    .workplane()
    .center(outer_diameter/2 - rib_spacing/2, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_height)
)
result = result.union(rib)
