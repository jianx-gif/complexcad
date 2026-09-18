import cadquery as cq
base_radius = 30.0
base_height = 15.0
step_radius = 20.0
step_flat_height = 5.0
step_height = 12.0
insert_radius = 8.0
insert_length = 25.0
fillet_radius = 1.5
mounting_hole_dia = 5.0
mounting_hole_offset = 12.0
profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(base_radius, 0)
    .lineTo(base_radius, step_flat_height)
    .lineTo(step_radius, step_flat_height)
    .lineTo(step_radius, step_flat_height + step_flat_height)
    .lineTo(0, step_flat_height + step_flat_height)
    .close()
)
base = profile.revolve()
base = base.edges().fillet(fillet_radius)
base = (
    base.faces(">Z")
    .workplane()
    .polarArray(radius=mounting_hole_offset, count=mounting_hole_offset, startAngle=0, angle=360)
    .hole(mounting_hole_dia)
)
base = (
    base.faces(">Z")
    .workplane()
    .polarArray(radius=mounting_hole_offset, count=mounting_hole_offset, startAngle=0, angle=360)
    .hole(mounting_hole_dia)
)
base = (
    base.faces(">Z")
    .workplane()
    .polarArray(radius=mounting_hole_offset, count=mounting_hole_offset, angle=360)
    .hole(mounting_hole_dia)
)
base = base.edges().fillet(fillet_radius)
result = base
