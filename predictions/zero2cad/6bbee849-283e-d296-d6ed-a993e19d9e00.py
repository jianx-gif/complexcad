import cadquery as cq

# Parameters
base_radius = 30.0
top_radius = 20.0
knob_height = 45.0
offset_x = 5.0
offset_y = 0.0
central_hole_diameter = 10.0
rib_width = 6.0
rib_height = 8.0
rib_depth = 4.0
rib_count = 6
rib_fillet_radius = 1.5
edge_fillet_radius = 0.8

# Lofted knob body
knob_body = (
    cq.Workplane("XY")
    .circle(base_radius)
    .workplane(offset=knob_height)
    .center(offset_x, offset_y)
    .circle(top_radius)
    .loft()
)

# Central through hole
knob_body = knob_body.faces(">Z").workplane().hole(central_hole_diameter)

# Ribbed grip zone
rib_base = (
    cq.Workplane("XY")
    .workplane(offset=knob_height - rib_height)
    .center(top_radius - rib_depth/2, 0)
    .rect(rib_width, rib_depth)
    .extrude(rib_height)
)

ribs = rib_base
for i in range(1, rib_count):
    angle = 360.0 / rib_count * i
    ribs = ribs.union(rib_base.rotate((0, 0, 0), (0, 0, 1), angle))

# Combine ribs with knob body
result = knob_body.union(ribs)

# Fillet rib edges for safety
result = result.edges("|Z").fillet(rib_fillet_radius)

# Fillet outer top edge for comfort
result = result.edges(">Z").fillet(edge_fillet_radius)
