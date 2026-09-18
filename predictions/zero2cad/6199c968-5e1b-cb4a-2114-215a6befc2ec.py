import cadquery as cq

# Parameters
outer_radius = 30.0
wall_thickness = 4.0
inner_radius = outer_radius - wall_thickness
height = 50.0
draft_angle = 2.0
flange_extra = 10.0
flange_thickness = 8.0
rib_width = 6.0
rib_height = 12.0
rib_thickness = 2.0
rib_offset = 5.0
chamfer_size = 1.0

# Outer shell with draft
outer = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(height, taper=-draft_angle)
)

# Inner cavity with chamfer on top edge
inner = (
    cq.Workplane("XY")
    .circle(inner_radius)
    .extrude(height, taper=-draft_angle)
    .faces("<Z")
    .edges()
    .chamfer(chamfer_size)
)

# Hollow body
body = outer.cut(inner)

# Flange on top
flange = (
    cq.Workplane("XY")
    .circle(outer_radius + flange_extra)
    .extrude(flange_thickness)
    .translate((0, 0, height))
)

# Internal rib (rectangular block attached to inner wall)
rib = (
    cq.Workplane("XY")
    .box(rib_thickness, rib_width, rib_height)
    .translate((inner_radius - rib_thickness/2, 0, rib_offset + rib_height/2))
)

# Assemble final part
result = body.union(flange).union(rib)
