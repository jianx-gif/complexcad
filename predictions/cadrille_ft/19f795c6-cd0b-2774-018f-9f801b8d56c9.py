import cadquery as cq

outer_radius = 80.0
outer_radius = 30.0
wall_thickness = 10.0
wall_thickness = 2.0
rib_width = 20.0
rib_height = 20.0
rib_spacing = 20.0
rib_spacing = 12.0
rib_spacing = 20.0
rib_spacing = 20.0
rib_spacing = 12.0
rib_spacing = 20.0
rib_spacing = 20.0
rib_spacing = 12.0
rib_spacing = 20.0
rib_spacing = 20.0
rib_spacing = 20.0
rib_spacing = 20.0
rib_spacing = 20.0
rib_spacing = 20.0
rib_spacing = 20.0
rib_spacing = 20.0
rib_spacing = 20.0
rib_spacing = 20.0
rib_spacing = 20.0
rib_spacing = 12.0
rib_spacing = 12.0
rib_spacing = 12.0
rib_spacing = 12.0

rib_count = 2.0

rib_count = 2.0

rib_count = 2.0

rib_count = 2.0

rib_count = 2.0

rib_count = 2.0

rib_count = 2.0

rib_count = 2.0

rib = (
    cq.Workplane('XY')
    .box(rib_length, rib_height, rib_height)
    .translate((0, 0, rib_height/2 + rib_height/2 + rib_height/2 + rib_height/2, rib_height/2 + rib_height/2 + rib_height/2, rib_height/2)
    .rect(rib_width, rib_height)
    .extrude(rib_height)
)

rib = (
    cq.Workplane('XY')
    .rect(rib_width, rib_height)
    .extrude(rib_height)
    .translate((0, 0, rib_height/2 + rib_height/2 + rib_height/2 + rib_height/2 + rib_height/2 + rib_height/2 + rib_height/2 + rib_height/2 + rib_width/2 + rib_width/2 + rib_width/2 + rib_width/2 + rib_width/2 + rib_width/2 + rib_width/2 + rib_width/2 + rib_width/2 + rib_width/2 + rib_width/2 + rib_width/2 + rib_width/2 + rib_width/2 + rib_width/2 + rib_width/2 + rib_width/2 + rib_width/2 + rib_width/2 + rib_width/2 + rib_width/2 + rib_width/2 + rib_width/2 + rib_width/2 + rib_width/2 + rib_width/2 + rib_width/2 + rib_width/2 + rib_width/2 + rib_width/2 + rib_width/2 + rib_width/2 + rib_width/2 + rib_width/2 + rib_width/2 + rib_width/2 + rib_width/2 + rib_width/2 + rib_width/2 + rib_width/2 + rib_width/2 + rib_width/2 + rib_width/2 + rib_width/2 + rib_width/2 + rib_width/2 + rib_width/2 + rib_width/2 + rib_width/2 + rib_width/2 + rib_width/2 + rib_width/2 + rib_width/2 + rib_width/2 +