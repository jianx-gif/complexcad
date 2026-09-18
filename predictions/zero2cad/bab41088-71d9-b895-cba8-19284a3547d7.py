import cadquery as cq

# Parameters
base_width = 60.0
base_height = 40.0
top_radius = 20.0
loft_height = 80.0
rib_width = 10.0
rib_height = 30.0
rib_thickness = 5.0
slot_width = 8.0
slot_length = 30.0
slot_depth = 5.0
chamfer_size = 1.0

# Lofted body: trapezoidal base to circular top
loft_body = (
    cq.Workplane("XY")
    .polyline([
        (-base_width/2, 0),
        (base_width/2, 0),
        (base_width/4, base_height),
        (-base_width/4, base_height),
    ])
    .close()
    .workplane(offset=loft_height)
    .circle(top_radius)
    .loft(combine=True)
)

# Rib on the +X side
rib = (
    cq.Workplane("XY")
    .center(base_width/2 - rib_width/2, 0)
    .rect(rib_width, rib_thickness)
    .extrude(rib_height)
)

# Combine loft and rib
combined = loft_body.union(rib)

# Slot cut on the -X side
slot = (
    cq.Workplane("XY")
    .center(-base_width/2 + slot_width/2, 0)
    .rect(slot_width, slot_length)
    .extrude(slot_depth)
    .translate((0, 0, loft_height/2 - slot_depth/2))
)

# Apply slot cut
result = combined.cut(slot)

# Chamfer bottom edges for safety
result = result.faces("<Z").edges().chamfer(chamfer_size)
