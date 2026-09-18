import cadquery as cq

# Parameters
outer_radius = 25.0
inner_radius = 20.0
cap_height = 30.0
grip_ring_height = 8.0
knurl_count = 20
knurl_width = 2.0
knurl_height = 3.0
knurl_depth = 0.8
pilot_diameter = 5.0
pilot_depth = 12.0
chamfer_size = 0.5

# Revolve profile to create cap body
cap_body = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, cap_height - grip_ring_height)
    .lineTo(outer_radius, cap_height - grip_ring_height)
    .lineTo(outer_radius, cap_height)
    .lineTo(inner_radius, cap_height)
    .close()
    .revolve()
)

# Apply chamfer to all edges
cap_body = cap_body.edges().chamfer(chamfer_size)

# Blind pilot aperture (hole from top surface)
cap_body = (
    cap_body.faces(">Z")
    .workplane()
    .hole(pilot_diameter, depth=pilot_depth)
)

# Generate knurl ribs
knurl_ribs = []
for i in range(knurl_count):
    rib = (
        cq.Workplane("XY")
        .box(knurl_width, knurl_depth, knurl_height)
        .translate((outer_radius + knurl_depth/2, 0, cap_height - grip_ring_height/2))
        .rotate((0, 0, 0), (0, 0, 1), i * 360.0 / knurl_count)
    )
    knurl_ribs.append(rib.val())

knurl_compound = cq.Compound.makeCompound(knurl_ribs)

# Assemble final part
result = cq.Workplane("XY").add(cap_body).add(knurl_compound).combine()
