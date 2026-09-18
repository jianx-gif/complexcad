import cadquery as cq

outer_radius = 40.0
wall_thickness = 5.0
inner_radius = outer_radius - wall_thickness
length = 70.0
slot_width = 5.0
slot_length = 30.0
slot_depth = wall_thickness + 0.5
chamfer_size = 0.5
hole_diameter = 4.0
hole_spacing = 20.0
hole_count = 3

profile = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius, length)
    .lineTo(inner_radius, length)
    .close()
)

solid = profile.revolve()

slot = (
    cq.Workplane("XY")
    .box(slot_depth, slot_width, slot_length)
    .translate((outer_radius - slot_depth/2, 0, 0))
)

solid = solid.cut(slot)

solid = solid.edges().chamfer(chamfer_size)

hole_positions = [(-hole_spacing, 0), (0, 0), (hole_spacing, 0)]

solid = (
    solid.faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)

result = solid