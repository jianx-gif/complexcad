import cadquery as cq

# Parameters
length = 80.0
width = 50.0
height = 20.0
boss_diameter = 30.0
rib_thickness = 5.0
rib_height = 12.0
rib_length = 60.0
aperture_diameter = 15.0
mount_hole_dia = 4.0
mount_offset_x = 30.0
mount_offset_y = 18.0
chamfer_size = 1.0
slot_width = 8.0
slot_length = 60.0
slot_depth = 5.0

# Base block with central boss (composite sketch)
profile = (
    cq.Workplane("XY")
    .sketch()
    .rect(length, width)
    .circle(boss_diameter / 2)
    .finalize()
)
result = cq.Workplane("XY").add(profile).extrude(height)

# Central vertical through aperture
result = result.faces(">Z").workplane().hole(aperture_diameter)

# Mounting holes at four corners on top surface
result = (
    result
    .faces(">Z")
    .workplane()
    .pushPoints([
        (mount_offset_x, mount_offset_y),
        (-mount_offset_x, mount_offset_y),
        (-mount_offset_x, -mount_offset_y),
        (mount_offset_x, -mount_offset_y),
    ])
    .hole(mount_hole_dia)
)

# Top surface slot for cable management
result = (
    result
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(slot_length, slot_width)
    .cutBlind(-slot_depth)
)

# Side ribs on +Y face
rib_pos = (
    result
    .faces(">Y")
    .workplane(centerOption="CenterOfMass")
    .rect(rib_thickness, rib_height)
    .extrude(rib_length)
)
# Side ribs on -Y face
rib_neg = (
    result
    .faces("<Y")
    .workplane(centerOption="CenterOfMass")
    .rect(rib_thickness, rib_height)
    .extrude(rib_length)
)
result = result.union(rib_pos).union(rib_neg)

# Chamfer vertical edges for safety
result = result.edges("|Z").chamfer(chamfer_size)

# Final result stored in variable 'result'
