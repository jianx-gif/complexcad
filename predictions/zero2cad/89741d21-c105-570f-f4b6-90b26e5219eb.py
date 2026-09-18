import cadquery as cq

# Parameters
outer_radius = 45.0
inner_radius = 10.0
hub_height = 15.0
flange_thickness = 5.0
flange_width = 30.0
flange_height = 6.0
chamfer_size = 2.0
hole_diameter = 5.0
hole_count = 6
hole_radius = outer_radius - 5.0
slot_width = 4.0
slot_length = 12.0
slot_depth = 3.0

# Base impeller profile and revolve
profile = (
    cq.Workplane("XY")
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, hub_height)
    .threePointArc((inner_radius + 5, hub_height + 5), (outer_radius, hub_height + 10))
    .lineTo(0, hub_height + 10)
    .close()
)
impeller = profile.revolve()

# Chamfer outer rim edge
impeller = impeller.edges(">Z").chamfer(chamfer_size)

# Add mounting flange on bottom face
flange = (
    impeller.faces("<Z")
    .workplane()
    .rect(flange_width, flange_height)
    .extrude(flange_thickness)
)
impeller = impeller.union(flange)

# Add radial slots on outer rim for weight reduction
slot = (
    cq.Workplane("XY")
    .center(outer_radius - slot_depth/2, 0)
    .rect(slot_width, slot_length)
    .extrude(slot_depth)
)
for i in range(4):
    angle = i * 90
    impeller = impeller.cut(slot.rotate((0, 0, 0), (0, 0, 1), angle))

# Add mounting holes on flange
impeller = (
    impeller.faces("<Z")
    .workplane()
    .polarArray(radius=hole_radius, startAngle=0, angle=360, count=hole_count)
    .hole(hole_diameter)
)

result = impeller