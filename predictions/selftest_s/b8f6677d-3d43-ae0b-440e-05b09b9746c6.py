import cadquery as cq

clamp_length = 80
clamp_width = 40
clamp_height = 20
cavity_radius = 8
cavity_offset = 10
material_thickness = 4
vent_hole_diameter = 4
vent_rows = 4
vent_columns = 6
vent_spacing_x = 10
vent_spacing_y = 6
chamfer_dist = 0.8
rib_height = 6
rib_thickness = 12
boss_radius = 6
boss_height = 10
mount_hole_dia = 3
slot_width = 6

base = (
    cq.Workplane("XY")
    .rect(clamp_width, clamp_length)
    .extrude(clamp_height)
)

cavity_cut = (
    cq.Workplane("XY")
    .center(0, cavity_offset)
    .circle(cavity_radius)
    .extrude(clamp_height)
)

slot = (
    cq.Workplane("XY")
    .center(0, clamp_length/2 - slot_width/2)
    .rect(slot_width, clamp_height)
    .extrude(material_thickness)
)

body = base.cut(cavity_cut).cut(slot)

body = body.edges("|Z").chamfer(chamfer_dist)

vent_face = body.faces(">Y")
body = (
    vent_face.workplane()
    .rarray(vent_spacing_x, vent_spacing_y, vent_columns, vent_rows)
    .hole(vent_hole_diameter)
)

rib = (
    cq.Workplane("XY")
    .center(0, clamp_length/2 - rib_thickness/2)
    .polygon(3, rib_thickness)
    .extrude(rib_height)
)
body = body.union(rib)

boss = (
    cq.Workplane("XY")
    .center(-clamp_width/2 + material_thickness + boss_radius, 0)
    .circle(boss_radius)
    .extrude(boss_height)
)
body = body.union(boss)

body = body.faces(">X").workplane().hole(mount_hole_dia)

result = body
