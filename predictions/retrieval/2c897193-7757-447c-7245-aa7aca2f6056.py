import cadquery as cq

# Parameters
main_pipe_length = 80.0
branch_pipe_length = 50.0
main_outer_dia = 30.0
pipe_wall_thickness = 3.0
rib_width = 8.0
rib_height = 4.0
rib_length = 40.0
pin_hole_dia = 5.0
pin_recess_depth = 6.0
pin_counterbore_dia = 9.0
pin_counterbore_depth = 2.0
chamfer_size = 1.0

# Derived dimensions
main_outer_radius = main_outer_dia / 2.0
hole_center_x = branch_pipe_length / 2.0 - 10.0

# Base tee geometry (union of two cylinders) and shell to create wall thickness
main_cyl = cq.Workplane('XY').circle(main_outer_radius).extrude(main_pipe_length)
branch_cyl = cq.Workplane('YZ').circle(main_outer_radius).extrude(branch_pipe_length)
tee_union = main_cyl.union(branch_cyl)
tee = tee_union.shell(-pipe_wall_thickness)

# External rib on positive X side of main pipe
rib = (cq.Workplane('YZ')
       .center(main_outer_radius + rib_height/2.0, 0)
       .rect(rib_width, rib_length)
       .extrude(rib_height))
tee = tee.union(rib)

# Recessed datum pin hole on branch side
pin_hole = (cq.Workplane('YZ')
            .center(0, 0)
            .circle(pin_hole_dia/2.0)
            .extrude(-pin_recess_depth)
            .translate((hole_center_x, 0, 0)))
counterbore = (cq.Workplane('YZ')
                .center(0, 0)
                .circle(pin_counterbore_dia/2.0)
                .extrude(-pin_counterbore_depth)
                .translate((hole_center_x, 0, 0)))
tee = tee.cut(pin_hole).cut(counterbore)

# Chamfer rib side edges for safety
result = tee.edges('|X').chamfer(chamfer_size)
