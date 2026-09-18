import cadquery as cq

# Parameters
base_length = 80.0
base_width = 80.0
base_thickness = 10.0
hex_flat_distance = 20.0
hex_height = 8.0
hole_diameter = 5.2
hole_counterbore_diameter = 9.0
hole_counterbore_depth = 4.0
hole_spacing = 40.0
fillet_radius = 2.0
chamfer_distance = 1.0
rib_height = 4.0
rib_thickness = 5.0
rib_spacing = 20.0
slot_width = 6.0
slot_length = 30.0
slot_offset = 35.0

# Base plate
result = (
    cq.Workplane("XY")
    .sketch()
    .rect(base_length, base_width)
    .finalize()
    .extrude(base_thickness)
)

# Add four mounting slots on each side
slot_pts = [(-base_length/2 + slot_offset, 0), (base_length/2 - slot_offset, 0),
            (0, -base_width/2 + slot_offset), (0, base_width/2 - slot_offset)]
for pt in slot_pts:
    result = (
        result.faces(">Z")
        .workplane(centerOption="CenterOfMass", origin=pt)
        .rect(slot_length, slot_width)
        .cutBlind(-base_thickness)
    )

# Build ribs as separate solid and union later
ribs = cq.Workplane("XY")
rib_x = -base_length/2 + rib_spacing
while rib_x < base_length/2:
    rib_y = -base_width/2 + rib_spacing
    while rib_y < base_width/2:
        ribs = (
            ribs.union(
                cq.Workplane("XY")
                .center(rib_x, rib_y)
                .rect(rib_thickness, rib_thickness)
                .extrude(rib_height)
            )
        )
        rib_y += rib_spacing * 2
    rib_x += rib_spacing * 2
result = result.union(ribs)

# Central hex boss
hex_radius = hex_flat_distance / (2 * 0.866025403784)  # convert flat distance to circumradius
result = (
    result.faces(">Z")
    .workplane()
    .polygon(6, hex_radius * 2)
    .extrude(hex_height)
)

# Drill four M5 clearance holes with countersink for heads
hole_positions = [
    ( hole_spacing/2,  hole_spacing/2),
    (-hole_spacing/2,  hole_spacing/2),
    (-hole_spacing/2, -hole_spacing/2),
    ( hole_spacing/2, -hole_spacing/2),
]
for pos in hole_positions:
    result = (
        result.faces(">Z")
        .workplane()
        .pushPoints([pos])
        .cskHole(hole_diameter, base_thickness + hex_height, hole_counterbore_depth, hole_counterbore_diameter)
    )

# Apply chamfer on outer base edges
result = result.edges("<<Z or >>Z").chamfer(chamfer_distance)

# Apply fillet on top horizontal edges for rounded edge
result = result.edges(">Z").fillet(fillet_radius)
