import cadquery as cq

# Parameters
base_radius = 30.0
step_radius = 20.0
tip_radius = 8.0
base_height = 15.0
step_flat_height = 5.0
cone_height = 12.0
total_height = base_height + step_flat_height + cone_height
insert_radius = 4.0
insert_length = 25.0
fillet_radius = 1.5
mounting_hole_dia = 5.0
mounting_hole_offset = 12.0

# 2‑D profile for revolved connector block
profile = (
    cq.Workplane("YZ")
    .moveTo(base_radius, 0)
    .lineTo(base_radius, base_height)
    .lineTo(step_radius, base_height)
    .lineTo(step_radius, base_height + step_flat_height)
    .lineTo(tip_radius, total_height)
    .lineTo(0, total_height)
    .close()
)
revolved_body = profile.revolve(360)

# Central insert pocket (simple cylinder)
insert_cylinder = (
    cq.Workplane("XY")
    .center(0, 0)
    .circle(insert_radius)
    .extrude(insert_length)
)
body_with_insert = revolved_body.cut(insert_cylinder)

# Fillet the sharp step shoulder (edge not parallel to Z)
filleted_body = body_with_insert.edges("not Z").fillet(fillet_radius)

# Four mounting holes on the top face in a cross pattern
final_body = (
    filleted_body
    .faces(">Z")
    .workplane()
    .pushPoints([
        (mounting_hole_offset, 0),
        (-mounting_hole_offset, 0),
        (0, mounting_hole_offset),
        (0, -mounting_hole_offset),
    ])
    .hole(mounting_hole_dia)
)

result = final_body