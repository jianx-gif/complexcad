import cadquery as cq
import math

# Parameters
outer_side = 70.0
wall_thickness = 5.0
channel_length = 80.0
fillet_radius = 3.0
chamfer_distance = 1.0
flange_width = 15.0
flange_thickness = 5.0
flange_hole_dia = 5.0
hole_offset = 20.0
rib_width = 4.0
rib_height = 10.0
rib_count = 8
slot_width = 8.0
slot_length = 20.0
slot_depth = 5.0

tolerance = 0.01

# Derived dimensions
outer_radius = outer_side * math.sqrt(2) / 2.0
inner_square_side = outer_side - 2 * wall_thickness

# Revolve a rectangular profile to create a solid cylinder enclosing the square channel
cyl = (
    cq.Workplane("XZ")
    .moveTo(0, -channel_length / 2.0)
    .lineTo(outer_radius, -channel_length / 2.0)
    .lineTo(outer_radius, channel_length / 2.0)
    .lineTo(0, channel_length / 2.0)
    .close()
    .revolve(360, (0, 0, 0), (0, 1, 0))
)

# Internal square void (exact length) with filleted corners
inner_void = (
    cq.Workplane("XY")
    .box(inner_square_side, inner_square_side, channel_length)
    .edges("|Z")
    .fillet(fillet_radius)
)

# Subtract the void, creating a hollow square channel
result = cyl.cut(inner_void)

# Chamfer outer rim edges (non‑parallel to Z)
result = result.edges("not(|Z)").chamfer(chamfer_distance)

# Add flanges by extruding from the end faces with overlap (both sides)
flange_neg = (
    result.faces("<Z")
    .workplane()
    .rect(flange_width, outer_side + 2 * flange_width)
    .extrude(flange_thickness, both=True)
)
flange_pos = (
    result.faces(">Z")
    .workplane()
    .rect(flange_width, outer_side + 2 * flange_width)
    .extrude(flange_thickness, both=True)
)
result = result.union(flange_neg).union(flange_pos)

# Mounting holes in flanges (grid pattern)
hole = (
    cq.Workplane("XY")
    .circle(flange_hole_dia / 2.0)
    .extrude(flange_thickness + 2 * tolerance)
)
for sign in (-1, 1):
    for x_mult in (-1, 1):
        for y_mult in (-1, 1):
            hx = x_mult * hole_offset
            hy = y_mult * hole_offset
            hz = sign * (channel_length / 2.0 + flange_thickness / 2.0)
            result = result.cut(hole.translate((hx, hy, hz)))

# Ribs on outer cylinder surface, positioned to intersect interior
rib_profile = (
    cq.Workplane("XY")
    .rect(rib_width, rib_height)
    .extrude(wall_thickness + tolerance)
)
rib_center_radius = outer_radius - wall_thickness - 0.5
for i in range(rib_count):
    angle = 360.0 * i / rib_count
    rib = rib_profile.rotate((0, 0, 0), (0, 0, 1), angle)
    rib = rib.translate((rib_center_radius, 0, 0))
    result = result.union(rib)

# Cable access slot on side of outer cylinder
slot = (
    cq.Workplane("XY")
    .rect(slot_width, slot_length)
    .extrude(slot_depth + tolerance)
    .translate((outer_radius - slot_depth / 2.0, 0, 0))
)
result = result.cut(slot)
