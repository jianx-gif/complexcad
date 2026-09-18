import cadquery as cq
import math

# Parameters
outer_radius = 45.0
inner_radius = 30.0
flange_thickness = 10.0
flange_width = 12.0
body_length = 40.0
seal_pocket_depth = 8.0
seal_pocket_radial_offset = 2.0
bolt_hole_dia = 5.0
bolt_circle_radius = 30.0
bolt_hole_count = 4
vent_slot_width = 3.0
vent_slot_height = 6.0
vent_slot_count = 4
chamfer_size = 1.0

# Base profile for revolve (XZ plane)
profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(outer_radius, 0)                          # Base outer wall
    .lineTo(outer_radius, body_length)               # Body height
    .lineTo(outer_radius + flange_thickness, body_length)  # Outward to flange outer radius
    .lineTo(outer_radius + flange_thickness, body_length + flange_width)  # Flange top
    .lineTo(outer_radius, body_length + flange_width)   # Inner side of flange
    .lineTo(outer_radius, body_length + seal_pocket_depth)  # Up for seal pocket region
    .lineTo(inner_radius, body_length + seal_pocket_depth)  # Transition to inner radius
    .lineTo(inner_radius, 0)                         # Down inner wall to base
    .close()
)

# Revolve profile to create solid
result = profile.revolve(360)

# Internal seal pocket (blind cylindrical cavity)
seal_pocket_radius = inner_radius - seal_pocket_radial_offset
seal_cylinder = (
    cq.Workplane("XY")
    .center(0, 0)
    .circle(seal_pocket_radius)
    .extrude(seal_pocket_depth)
    .translate((0, 0, body_length + seal_pocket_depth / 2))
)
result = result.cut(seal_cylinder)

# Bolt holes on flange top (through holes)
bolt_positions = [
    (
        bolt_circle_radius * math.cos(math.radians(i * 360 / bolt_hole_count)),
        bolt_circle_radius * math.sin(math.radians(i * 360 / bolt_hole_count))
    )
    for i in range(bolt_hole_count)
]
result = (
    result
    .faces(">Z")
    .workplane()
    .pushPoints(bolt_positions)
    .hole(bolt_hole_dia)
)

# Vent slots on outer cylindrical surface (rectangular cuts rotated around Z)
slot = (
    cq.Workplane("XY")
    .rect(vent_slot_width, vent_slot_height)
    .extrude(flange_thickness)
    .translate((outer_radius + flange_thickness / 2, 0, body_length + flange_width / 2))
)
for i in range(vent_slot_count):
    angle = i * 360 / vent_slot_count
    rotated_slot = slot.rotate((0, 0, 0), (0, 0, 1), angle)
    result = result.cut(rotated_slot)

# Chamfer outer edges for safety
result = result.edges().chamfer(chamfer_size)
