import cadquery as cq
outer_dia_full = 60.0
outer_dia_mid = 40.0
outer_dia_small = 20.0
length_big = 30.0
length_small = 30.0
length_mid = 30.0
length_small = 30.0
length_small = 30.0
length_bore_dia = 8.0
counterbore_dia = 12.0
counterbore_depth = 5.0
fillet_radius = 2.0
outer_radius = outer_dia_full / 2.0
outer_radius = outer_dia_full / 2.0
inner_radius = outer_radius - outer_dia_full / 2.0
base = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(length_bore_dia)
)
base = base.edges().fillet(fillet_radius)
base = base.faces(">Z").workplane().hole(through_hole_dia)
base = base.faces(">Z").workplane().hole(through_hole_dia)
base = base.faces(">Z").workplane().hole(inner_radius * 2)
base = base.faces(">Z").workplane().rect(length_bore_dia_full, length_bore_dia_small).cutBlind(-length_bore_depth)
base = base.faces(">Z").workplane().circle(counterbore_dia/2).cutBlind(-length_bore_depth)
base = base.faces(">Z").workplane().center(0, 0).hole(mount_hole_dia)
base = base.faces(">Z").workplane().center(0, 0).hole(mount_hole_dia)
base = base.faces("<Z").workplane().center(0, 0).hole(mount_hole_dia)
base = base.faces("<Z").workplane().center(0, 0).hole(mount_hole_dia)
base = base.faces("<Z").workplane().center(0, 0).hole(mount_hole_dia)
base = base.faces("<Z").workplane().center(0, 0).hole(mount_hole_dia)
base = base.faces("<Z").edges().chamfer(length_bore_dia/2)
result = base
