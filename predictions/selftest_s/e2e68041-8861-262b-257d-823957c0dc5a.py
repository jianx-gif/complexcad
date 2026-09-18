import cadquery as cq

# Parameters
handle_length = 80.0
handle_thickness = 20.0
handle_height = 12.0
flange_width = 35.0
flange_height = 6.0
mount_hole_diameter = 5.0
countersink_diameter = 10.0
mount_hole_depth = handle_height + flange_height
chamfer_distance = 1.0
grip_cylinder_dia = 10.0
grip_cylinder_len = 30.0
rib_height = 3.0
rib_width = 4.0
rib_spacing = 12.0
slot_width = 4.0
slot_length = 25.0
slot_offset = 10.0

# Base extruded handle body
base_body = (
    cq.Workplane("XY")
    .rect(handle_length, handle_thickness)
    .extrude(handle_height)
)

# Central flange (wider than base)
central_flange = (
    cq.Workplane("XY")
    .center(0, 0)
    .rect(handle_length, flange_width)
    .extrude(flange_height)
    .translate((0, 0, handle_height))
)

# Grip cylinder on side of handle for ergonomics
grip_cylinder = (
    cq.Workplane("YZ")
    .center(handle_length / 2 - grip_cylinder_len / 2, 0)
    .circle(grip_cylinder_dia / 2)
    .extrude(grip_cylinder_len)
    .rotate((0, 0, 0), (0, 0, 1), 90)
    .translate((0, 0, handle_height / 2))
)

# Underside ribs for stiffness (patterned along length)
rib_base = (
    cq.Workplane("XY")
    .center(0, -(handle_thickness / 2 + rib_width / 2))
    .rect(rib_width, rib_height)
    .extrude(handle_height)
)

rib_count = int(handle_length / rib_spacing) + 1
rib_union = None
for i in range(rib_count):
    offset = -handle_length / 2 + i * rib_spacing
    rib_i = rib_base.translate((offset, 0, 0))
    rib_union = rib_i if rib_union is None else rib_union.union(rib_i)

# Side slot for cable routing (solid to cut later)
slot = (
    cq.Workplane("XY")
    .center(-handle_length / 2 + slot_offset, 0)
    .rect(slot_width, slot_length)
    .extrude(handle_height)
)

# Assemble main solid
assembled = base_body.union(central_flange).union(grip_cylinder)
if rib_union is not None:
    assembled = assembled.union(rib_union)

# Add countersunk mounting hole through top center
assembled = assembled.faces(">Z").workplane().cskHole(mount_hole_diameter, countersink_diameter, mount_hole_depth)

# Apply chamfer to all top edges for safety
assembled = assembled.faces(">Z").edges().chamfer(chamfer_distance)

# Cut the side slot for cable routing
result = assembled.cut(slot)
