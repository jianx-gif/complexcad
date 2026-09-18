import cadquery as cq

lever_length = 80
base_radius = 20
tip_radius = 5
taper_length = 30
rounded_end_fillet = 3
hole_diameter = 5
hole_depth = 8
hole_spacing = 15
hole_cols = 3
hole_rows = 2
mount_hole_dia = 8
outer_chamfer = 0.5

profile = (
    cq.Workplane("YZ")
    .lineTo(base_radius, 0)
    .lineTo(base_radius, lever_length - taper_length)
    .lineTo(tip_radius, lever_length)
    .lineTo(0, lever_length)
    .close()
)

result = (
    profile
    .revolve()
    .edges("<Z").chamfer(outer_chamfer)
    .edges(">Z").fillet(rounded_end_fillet)
    .faces(">Z").workplane()
    .rarray(hole_spacing, hole_spacing, hole_cols, hole_rows)
    .hole(hole_diameter, depth=hole_depth)
    .faces("<Z").workplane()
    .hole(mount_hole_dia)
)
