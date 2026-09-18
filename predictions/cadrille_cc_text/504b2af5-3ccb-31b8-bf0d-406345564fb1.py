import cadquery as cq
body_length = 80.0
body_width = 30.0
shoulder_width = 12.0
shoulder_height = 15.0
shoulder_thickness = 6.0
fillet_radius = 2.0
hole_diameter = 6.0
hole_offset_along = 20.0
rib_width = 5.0
rib_thickness = 2.0
rib_offset_from_edge = 5.0
rib_count = 4
rib_length = body_length - shoulder_width
rib_height = shoulder_height - shoulder_height
rib_length = body_length - shoulder_width
rib_offset_from_edge = 5.0
base = (
    cq.Workplane("XY")
    .rect(body_length, body_width)
    .extrude(body_thickness)
)
shoulder = (
    base.faces(">Z").workplane()
    .rect(shoulder_width, shoulder_height)
    .extrude(shoulder_thickness)
)
rib = (
    shoulder.faces(">Z").workplane()
    .rect(rib_width, rib_thickness)
    .extrude(rib_height)
)
combined = base.union(rib)
combined = (
    combined.faces(">Z").workplane()
    .rarray(rib_offset_from_edge, 0, rib_count, 1, center=True)
    .rect(rib_width, rib_thickness)
    .extrude(rib_height)
)
combined = combined.union(rib)
combined = (
    combined.faces(">Z").workplane()
    .rarray(0, hole_offset_along, 1, 2)
    .hole(hole_diameter)
)
result = combined
