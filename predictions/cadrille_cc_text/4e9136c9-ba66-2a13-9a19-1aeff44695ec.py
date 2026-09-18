import cadquery as cq
outer_diameter = 80.0
inner_step1_diameter = 40.0
inner_step2_diameter = 30.0
outer_rim_thickness = 6.0
spacer_height = 20.0
spacer_diameter = outer_diameter - 2 * spacer_height
spacer_height = spacer_height - 2 * spacer_height
central_hole_diameter = 10.0
countersink_diameter = 6.0
countersink_angle = 82.0
mount_hole_diameter = 4.0
mount_hole_spacing = 30.0
slot_width = 4.0
slot_length = 12.0
slot_depth = spacer_height / 2
profile = (
    cq.Workplane("XY")
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, spacer_height)
    .lineTo(inner_radius + spacer_height, spacer_height)
    .lineTo(inner_radius + spacer_height, 0)
    .lineTo(inner_radius, 0)
    .close()
)
solid = profile.revolve()
solid = solid.edges().chamfer(outer_rim_thickness)
solid = solid.faces(">Z").workplane().hole(countersink_diameter, countersink_angle)
solid = solid.faces(">Z").workplane().rect(slot_width, slot_length).cutBlind(-spacer_height)
solid = solid.faces("<Z").workplane().polarArray(radius=outer_radius - spacer_height/2, count=4, startAngle=0, angle=360).rect(slot_width, slot_length).cutBlind(-spacer_height)
solid = solid.faces(">Z").workplane().pushPoints([(-mount_hole_spacing/2, 0), (mount_hole_spacing/2, 0)])
solid = solid.faces(">Z").workplane().pushPoints([(-mount_hole_spacing/2, 0), (mount_hole_spacing/2, 0)])
solid = solid.faces(">Z").workplane().pushPoints([(-mount_hole_spacing/2, 0), (mount_hole_spacing/2, 0)])
solid = solid.faces("<Z").workplane().pushPoints([(-mount_hole_spacing/2, 0), (mount_hole_spacing/2, 0)])
solid = solid.faces("<Z").workplane().pushPoints([(-mount_hole_spacing/2, 0), (mount_hole_spacing/2, 0)])
solid = solid.faces("<Z").workplane().pushPoints([(-mount_hole_spacing/2, 0), (mount_hole_spacing/2, 0)])
solid = solid.faces("<Z").workplane().pushPoints([(-mount_hole_spacing/2, 0), (mount_hole_spacing/2, 0)])
solid = solid.faces("<Z").workplane().pushPoints([(-mount_hole_spacing/2, 0), (mount_hole_spacing/2, 0)])
solid = solid.faces("<Z").workplane().pushPoints([(-mount_hole_spacing/2, 0), (mount_hole_spacing/2, 0)])
solid = solid.faces("<Z").workplane().pushPoints([(-mount_hole_spacing/2, 0), (mount_hole_spacing/2, 0)])
solid = solid.faces("<Z").workplane().pushPoints([(0, -spacer_height/2), (0, spacer_height/2)])
solid = solid.faces("<Z").workplane().pushPoints([(0, -spacer_height/2), (0, spacer_height/2)])
solid = solid.faces("<Z").workplane().pushPoints([(0, -spacer_height/2), (0, -spacer_height/2)])
solid = solid.faces("<Z").workplane().pushPoints([(0, -spacer_height/2), (0, spacer_height/2)])
solid = solid.faces("<Z").workplane().pushPoints([(0, spacer_height/2), (0, -spacer_height/2)])
solid = solid.faces("<Z").workplane().pushPoints([(0, -spacer_height/2), (0, spacer_height/2)])
solid = solid.faces("<Z").workplane().pushPoints([(0, spacer_height/2),