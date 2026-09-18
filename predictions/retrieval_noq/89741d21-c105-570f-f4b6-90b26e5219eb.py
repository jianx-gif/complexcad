import cadquery as cq

# Parameters
arm_length = 80
arm_height = 20
base_thickness = 10
concave_depth = 12
chamfer_size = 1.5
shaft_hole_diameter = 8
slot_width = 4
number_of_slots = 4
rib_thickness = 2
rib_height = 6

# Base lever body via revolve of a composite profile using Workplane
lever_body = (
    cq.Workplane("XY")
    .lineTo(0, base_thickness)
    .lineTo(arm_length, arm_height)
    .threePointArc((arm_length / 2, arm_height - concave_depth), (0, 0))
    .close()
    .revolve()
)

# Chamfer top outer edge (apply to all edges for robustness)
lever_body = lever_body.edges().chamfer(chamfer_size)

# Shaft mounting hole at base (subtract a central cylinder)
hole_cylinder = (
    cq.Workplane("XY")
    .center(0, 0)
    .circle(shaft_hole_diameter / 2)
    .extrude(arm_height * 2)
)
lever_body = lever_body.cut(hole_cylinder)

# Create a rib using sweep for internal reinforcement
rib_profile = (
    cq.Workplane("YZ")
    .moveTo(0, 0)
    .lineTo(0, arm_height)
    .lineTo(rib_thickness, arm_height)
    .lineTo(rib_thickness, 0)
    .close()
)
rib_path = (
    cq.Workplane("XY")
    .lineTo(arm_length, 0)
    .wire()
)
rib = rib_profile.sweep(rib_path)
lever_body = lever_body.union(rib)

# Create circular slots around outer circumference
slot = (
    cq.Workplane("XY")
    .center(arm_length, 0)
    .circle(slot_width / 2)
    .extrude(arm_height)
)
slots = slot
for i in range(1, number_of_slots):
    angle = i * 360 / number_of_slots
    slots = slots.union(slot.rotate((0, 0, 0), (0, 0, 1), angle))
lever_body = lever_body.cut(slots)

result = lever_body