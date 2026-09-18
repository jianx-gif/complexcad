import cadquery as cq

# Parameters
main_pipe_diameter = 30.0
branch_pipe_diameter = 20.0
wall_thickness = 2.0
main_pipe_length = 80.0
branch_pipe_length = 60.0
fillet_radius = 0.3
hole_diameter = 5.0
hole_spacing = 15.0
hole_count = 3

# Derived dimensions
main_outer_radius = main_pipe_diameter / 2.0
main_inner_radius = main_outer_radius - wall_thickness
branch_outer_radius = branch_pipe_diameter / 2.0
branch_inner_radius = branch_outer_radius - wall_thickness

# Main pipe (hollow cylinder)
main_outer = cq.Workplane("XY").circle(main_outer_radius).extrude(main_pipe_length)
main_inner = cq.Workplane("XY").circle(main_inner_radius).extrude(main_pipe_length)
main_pipe = main_outer.cut(main_inner)

# Branch pipe (hollow cylinder) oriented along X, centered at mid of main pipe
branch_outer = (
    cq.Workplane("YZ")
    .circle(branch_outer_radius)
    .extrude(branch_pipe_length)
    .translate((0, 0, main_pipe_length / 2.0))
)
branch_inner = (
    cq.Workplane("YZ")
    .circle(branch_inner_radius)
    .extrude(branch_pipe_length)
    .translate((0, 0, main_pipe_length / 2.0))
)
branch_pipe = branch_outer.cut(branch_inner)

# Union of main and branch
tee = main_pipe.union(branch_pipe)

# Fillet on the junction edges (small radius for manufacturability)
tee = tee.edges().fillet(fillet_radius)

# Add a row of through holes on the branch pipe wall
for i in range(hole_count):
    x_pos = -branch_pipe_length / 2.0 + (i + 1) * hole_spacing
    hole = (
        cq.Workplane("YZ")
        .center(x_pos, 0)
        .circle(hole_diameter / 2.0)
        .extrude(wall_thickness * 2.0)
        .translate((0, 0, main_pipe_length / 2.0))
    )
    tee = tee.cut(hole)

result = tee