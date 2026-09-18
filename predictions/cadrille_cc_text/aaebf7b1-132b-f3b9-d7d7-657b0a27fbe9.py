import cadquery as cq
outer_width = 80.0
case_height = 50.0
case_thickness = 2.0
wall_thickness = 2.0
base_thickness = 5.0
latch_width = 15.0
latch_thickness = 5.0
latch_height = 8.0
vent_hole_dia = 3.0
vent_hole_count = 4
outer_radius = outer_width / 2.0
inner_radius = outer_radius - wall_thickness
base = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius, case_height)
    .lineTo(inner_radius, case_height)
    .lineTo(inner_radius, 0)
    .close()
)
base = base.cut(inner_radius)
latch = (
    cq.Workplane("XY")
    .box(latch_thickness, latch_width, latch_height)
    .translate((outer_radius - latch_thickness/2.0, 0, case_height/2.0))
)
base = base.cut(latch)
base = base.faces(">Z").workplane().hole(vent_hole_dia)
base = base.faces(">Z").workplane().rect(latch_thickness, latch_height).cutBlind(-latch_thickness)
base = base.faces(">Z").workplane().polarArray(radius=outer_radius - wall_thickness/2.0, count=vent_hole_count, startAngle=0, angle=360).hole(vent_hole_dia)
base = base.faces(">Z").workplane().polarArray(radius=outer_radius - wall_thickness/2.0, count=vent_hole_count, startAngle=0, angle=360).hole(vent_hole_dia)
base = base.faces(">Z").workplane().polarArray(radius=outer_radius - wall_thickness/2.0, count=vent_hole_count, startAngle=0, angle=360).rect(latch_thickness, latch_height).extrude(base_thickness)
result = base.union(base)
