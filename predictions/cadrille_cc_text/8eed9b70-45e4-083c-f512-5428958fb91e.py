import cadquery as cq
outer_diameter = 80.0
inner_diameter = 70.0
height = 30.0
wall_thickness = 2.0
lip_height = 5.0
lip_width = 8.0
snap_beam_width = 8.0
snap_beam_height = 3.0
snap_beam_length = 12.0
snap_beam_thickness = 1.0
chamfer_distance = 0.8
vent_width = 4.0
vent_height = 10.0
vent_spacing = 12.0
vent_rows = 2
vent_cols = 3
vent_rows = 2
vent_rows = 2
outer_radius = outer_diameter / 2.0
inner_radius = inner_diameter / 2.0
profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius, height)
    .lineTo(inner_radius, height)
    .lineTo(inner_radius, 0)
    .close()
)
solid = profile.revolve()
solid = solid.faces(">Z").edges().chamfer(chamfer_distance)
solid = solid.faces(">Z").workplane().circle(snap_beam_width / 2.0).cutBlind(snap_beam_length)
solid = solid.faces(">Z").workplane().circle(snap_beam_width / 2.0).extrude(snap_beam_length)
solid = solid.faces(">Z").workplane().rect(snap_beam_width, snap_beam_length).extrude(snap_beam_thickness)
solid = solid.faces(">Z").workplane().polarArray(radius=vent_spacing, startAngle=0, angle=360, count=vent_cols).rect(vent_width, vent_height).extrude(vent_height)
solid = solid.faces(">Z").workplane().pushPoints([(vent_rows - 1) for y in vent_rows]).rect(vent_width, vent_height).extrude(vent_height)
solid = solid.faces(">Z").edges().chamfer(chamfer_distance)
result = solid
