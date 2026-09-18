import cadquery as cq

# Parameters
outer_radius = 30.0
top_radius = 20.0
base_height = 40.0
taper_height = 20.0
total_height = base_height + taper_height
wall_thickness = 3.0
inner_radius = outer_radius - wall_thickness
inner_top_radius = top_radius - wall_thickness
post_radius = 28.0
post_height = 10.0
hole_diameter = 5.0
hole_depth = 15.0
hole_grid_x = 2
hole_grid_y = 2
hole_spacing = 12.0
chamfer_distance = 2.0

# Outer solid (revolved)
outer = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius, base_height)
    .lineTo(top_radius, total_height)
    .lineTo(0, total_height)
    .close()
    .revolve()
)

# Inner hollow (revolved)
inner = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(inner_radius, 0)
    .lineTo(inner_radius, base_height)
    .lineTo(inner_top_radius, total_height)
    .lineTo(0, total_height)
    .close()
    .revolve()
)

block = outer.cut(inner)

# Top mounting post extruded into the block (negative direction) to intersect wall
block = (
    block.faces(">Z")
    .workplane()
    .center(0, 0)
    .circle(post_radius)
    .extrude(-post_height)
)

# Top blind hole pattern (grid)
block = (
    block.faces(">Z")
    .workplane()
    .rect((hole_grid_x - 1) * hole_spacing, (hole_grid_y - 1) * hole_spacing)
    .vertices()
    .circle(hole_diameter / 2)
    .cutBlind(hole_depth)
)

# Chamfer on top rim edges
block = block.faces(">Z").edges().chamfer(chamfer_distance)

result = block