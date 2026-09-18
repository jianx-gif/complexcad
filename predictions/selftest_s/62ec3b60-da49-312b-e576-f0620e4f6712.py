import cadquery as cq
outer_diameter = 80.0
wall_thickness = 2.0
height = 30.0
recess_depth = 8.0
recess_diameter = 30.0
hole_diameter = 4.0
hole_grid_rows = 4
hole_grid_cols = 5
hole_spacing = 12.0
chamfer_size = 0.5
rib_thickness = 1.5
rib_height = 20.0
outer_radius = outer_diameter / 2.0
inner_radius = outer_radius - wall_thickness
base = (
    cq.Workplane("XY")
    .sketch()
    .circle(outer_radius)
    .circle(inner_radius)
    .finalize()
    .extrude(height)
)
recess = (
    cq.Workplane("XY")
    .center(0, 0)
    .circle(recess_diameter / 2.0)
    .extrude(-recess_depth)
)
base = base.cut(recess)
rib = (
    cq.Workplane("XZ")
    .center(inner_radius + wall_thickness/2.0, height/2.0)
    .rect(rib_thickness, rib_height)
    .extrude(wall_thickness)
)
base = base.union(rib)
origin_x = -((hole_grid_cols - 1) * hole_spacing) / 2.0
origin_y = -((hole_grid_rows - 1) * hole_spacing) / 2.0
points = [(origin_x + i * hole_spacing, origin_y + j * hole_spacing)
          for i in range(hole_grid_cols)
          for j in range(hole_grid_rows)]
base = (
    base.faces(">Z").workplane()
    .pushPoints(points)
    .hole(hole_diameter, wall_thickness + 0.2)
)
result = base.edges(">Z").chamfer(chamfer_size)
