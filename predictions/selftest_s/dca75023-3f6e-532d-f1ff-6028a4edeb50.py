import cadquery as cq

# Parameters
spacer_width = 60.0
spacer_length = 40.0
spacer_thickness = 12.0
rib_width = 6.0
rib_height = 4.0
rib_spacing = 10.0
counterbore_diam = 15.0
counterbore_depth = 6.0
through_hole_diam = 6.0
key_slot_width = 8.0
key_slot_depth = 5.0
chamfer_size = 1.0

# Base block
base = (
    cq.Workplane("XY")
    .rect(spacer_width, spacer_length)
    .extrude(spacer_thickness)
)

# Add side ribs (four ribs on each long side)
rib = (
    cq.Workplane("XY")
    .rect(rib_width, spacer_length - 2 * rib_spacing)
    .extrude(rib_height)
)
# Position ribs along each long side
rib_pattern = (
    base
    .union(
        rib.translate((spacer_width/2 - rib_width/2, 0, spacer_thickness/2 + rib_height/2))
    )
    .union(
        rib.translate((-spacer_width/2 + rib_width/2, 0, spacer_thickness/2 + rib_height/2))
    )
)

# Counterbore on top face
counterbore = (
    rib_pattern
    .faces(">Z")
    .workplane()
    .hole(through_hole_diam)
    .hole(counterbore_diam, depth=counterbore_depth)
)

# Peripheral key slot (cut into side face)
slot = (
    counterbore
    .faces("<X")
    .workplane(offset=spacer_thickness/2)
    .rect(key_slot_width, key_slot_depth)
    .cutBlind(-spacer_thickness)
)

# Chamfer edges
result = (
    slot
    .edges("|Z")
    .chamfer(chamfer_size)
)
