import cadquery as cq

# Parameters
handle_length = 80.0
base_radius = 15.0
mid_radius = 10.0
mid_section_length = 30.0
fillet_radius = 2.0
wall_thickness = 3.0
slot_width = 8.0
slot_depth = 4.0
slot_length = 40.0
slot_offset = 20.0
hole_diameter = 5.0
hole_spacing = 30.0
hole_offset = 10.0

# Outer profile sketch on XZ plane
profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(base_radius, 0)
    .lineTo(base_radius, mid_section_length)
    .threePointArc((mid_radius + fillet_radius, mid_section_length + fillet_radius), (mid_radius, mid_section_length + 2 * fillet_radius))
    .lineTo(mid_radius, handle_length)
    .close()
)

# Revolve to create solid handle body
solid = profile.revolve()

# Shell to create hollow interior
hollow = solid.shell(-wall_thickness)

# Create side slot as a rectangular cut intersecting the outer wall
slot = (
    cq.Workplane("XY")
    .box(slot_width, slot_depth, slot_length)
    .translate((0, 0, slot_offset))
)

# Cut slot from hollow body
with_slot = hollow.cut(slot)

# Add mounting holes on the base face
result = (
    with_slot
    .faces("<Z")
    .workplane()
    .pushPoints([(-hole_spacing/2, hole_offset), (hole_spacing/2, hole_offset)])
    .hole(hole_diameter)
)
