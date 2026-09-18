import cadquery as cq

outer_radius = 80.0
outer_radius = 40.0
wall_thickness = 10.0
wall_thickness = 2.0
rib_width = 30.0
rib_height = 12.0
rib_spacing = 20.0
rib_spacing = 20.0
rib_spacing = 12.0
rib_spacing = 2.0
rib_spacing = 2.0
rib_spacing = 12.0
rib_spacing = 20.0
rib_spacing = 12.0
rib_spacing = 2.0

# Base plate
rib_spacing = 0.5
rib_spacing = 12.0
rib_spacing = 2.0

# Base plate
rib_spacing = 0.5
rib_spacing = 0.5

# Base plate
rib_count = 0.5
rib_count = 0.5
rib_count = 0.5
rib_count = 0.5

# Base plate
rib_count = 0.5
rib_count = 0.5
rib_count = 0.5

# Base = (rib_height - rib_height)
# Base
rib = (
    cq.Workplane('XY')
    .box(rib_depth, rib_height, rib_height)
    .translate((0, 0, rib_height + rib_height + rib_height + rib_height, rib_height + rib_height + rib_height + rib_height, rib_height + rib_height)
    .rect(rib_height, rib_height)
    .extrude(rib_height)
)

rib = (
    rib.faces(">Z")
    .workplane()
    .rect(rib_width, rib_height)
    .extrude(rib_height)
    .translate((0, 0, rib_height + rib_height + rib_height + rib_height + rib_height + rib_height + rib_height + rib_height + rib_height + rib_height + rib_height + rib_height + rib_height + rib_height + rib_height + rib_height + rib_height + rib_height + rib_height + rib_height + rib_height + rib_height + rib_height + rib_height + rib_height + rib_height + rib_height + rib_height + rib_height + rib_height + rib_height + rib_height + rib_height + rib_height + rib_height + rib_height)
    .workplane()
    .rect(rib_depth, rib_height)
    .extrude(rib_height)
)

# rib = (
    rib.faces(">Z")
    .workplane()
    .rect(rib_width, rib_height)
    .extrude(rib_height)
)
)

# rib
result = base.edges().fillet(rib_count)
