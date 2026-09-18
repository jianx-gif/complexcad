import cadquery as cq
knob_max_radius = 25.0
knob_min_radius = 10.0
knob_height = 30.0
shoulder_height = 5.0
set_screw_radius = 2.0
set_screw_offset = 12.0
base_height = 12.0
base_radius = knob_max_radius - knob_min_radius
base = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(base_radius, 0)
    .lineTo(base_radius, base_height)
    .lineTo(shoulder_height, base_height)
    .lineTo(shoulder_height, base_height + shoulder_height)
    .lineTo(0, base_height + shoulder_height)
    .close()
    .revolve()
)
knob_body = base.cut(base)
knob_body = knob_body.edges().first().chamfer(base_height)
knob_body = knob_body.edges().first().fillet(base_radius)
knob_body = knob_body.edges().first().chamfer(base_height)
knob_body = knob_body.faces(">Z").workplane().polarArray(radius=knob_body/2, count=set_screw_radius, startAngle=0, angle=360).hole(set_screw_radius * 2)
knob_body = knob_body.faces(">Z").workplane().polarArray(radius=knob_body/2, count=set_screw_radius, startAngle=0, angle=360).circle(set_screw_radius).cutBlind(set_screw_offset)
knob_body = knob_body.faces(">Z").workplane().polarArray(radius=knob_body/2, count=set_screw_radius, startAngle=0, angle=360).circle(set_screw_radius).extrude(set_screw_height)
knob_body = knob_body.cut(knob_body)
knob_body = knob_body.edges().chamfer(base_height)
knob_body = knob_body.faces(">Z").workplane().polarArray(radius=knob_body/2, count=set_screw_radius, startAngle=0, angle=360).circle(set_screw_radius).extrude(set_screw_height)
knob_body = knob_body.faces(">Z").workplane().polarArray(radius=knob_body/2, count=set_screw_radius, startAngle=0, angle=360).circle(set_screw_radius).extrude(set_screw_height)
result = knob_body
