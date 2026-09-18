import cadquery as cq
coupler_length = 60.0
shoulder_dia = 30.0
inner_dia = 20.0
thread_pitch = 4.0
relief_groove_width = 3.0
relief_groove_depth = 2.0
chamfer_len = 5.0
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_dia/2, 0)
    .lineTo(shoulder_dia/2, 0)
    .lineTo(shoulder_dia/2, shoulder_dia)
    .lineTo(inner_dia/2, shoulder_dia)
    .close()
)
base = profile.revolve()
base = base.faces(">Z").workplane().hole(inner_dia)
base = base.faces(">Z").workplane().circle(relief_groove_width/2).cutBlind(-relief_groove_depth)
base = base.faces(">Z").workplane().circle(relief_groove_width/2).cutBlind(-relief_groove_depth)
base = base.faces(">Z").workplane().circle(relief_groove_width/2).extrude(relief_groove_depth)
base = base.faces(">Z").workplane().circle(relief_groove_width/2).extrude(relief_groove_depth)
base = base.faces(">Z").workplane().polarArray(radius=outer_dia/2 - thread_pitch, count=thread_pitch, startAngle=0, angle=360).circle(relief_groove_width/2).extrude(relief_groove_depth)
base = base.cut(relief_groove)
base = base.faces(">Z").workplane().polarArray(radius=outer_dia/2 - thread_pitch, count=thread_pitch, startAngle=0, angle=360).circle(relief_groove_width/2).extrude(relief_groove_depth)
base = base.union(base)
base = base.faces(">Z").workplane().polarArray(radius=outer_dia/2 - thread_pitch, count=thread_pitch, startAngle=0, angle=360).circle(relief_groove_width/2).extrude(relief_groove_depth)
base = base.faces(">Z").workplane().polarArray(radius=outer_dia/2 - thread_pitch, count=thread_pitch, startAngle=0, angle=360).circle(relief_groove_width/2).extrude(relief_groove_depth)
base = base.faces(">Z").workplane().polarArray(radius=outer_dia/2 - thread_pitch, count=thread_pitch, startAngle=0, angle=360).circle(relief_groove_width/2).extrude(relief_groove_depth)
base = base.faces(">Z").workplane().polarArray(radius=outer_dia/2 - thread_pitch, count=thread_pitch, startAngle=0, angle=360).circle(relief_groove_width/2).extrude(relief_groove_depth)
base = base.faces(">Z").workplane().polarArray(radius=outer_dia/2 - thread_pitch, count=thread_pitch, startAngle=0, angle=360).circle(relief_groove_width/2).extrude(relief_groove_depth)
base = base.edges().chamfer(chamfer_len)
result = base
