import cadquery as cq

# Parameters
main_length = 80.0
main_od = 30.0
main_wall_thk = 3.0
branch_length = 50.0
branch_od = 25.0
lip_thk = 0.8
lip_length = 5.0
bolt_hole_dia = 6.0
bolt_hole_offset = 8.0
chamfer_dist = 0.5

# Outer main pipe
outer_main = (
    cq.Workplane("XY")
    .center(0, 0)
    .circle(main_od / 2)
    .extrude(main_length)
)
# Inner cavity of main pipe
inner_main = (
    cq.Workplane("XY")
    .center(0, 0)
    .circle((main_od / 2) - main_wall_thk)
    .extrude(main_length)
)
main_pipe = outer_main.cut(inner_main)
# Outer branch pipe
outer_branch = (
    cq.Workplane("YZ")
    .center(0, 0)
    .circle(branch_od / 2)
    .extrude(branch_length)
)
# Inner cavity of branch pipe
inner_branch = (
    cq.Workplane("YZ")
    .center(0, 0)
    .circle((branch_od / 2) - main_wall_thk)
    .extrude(branch_length)
)
branch_pipe = outer_branch.cut(inner_branch)
# Combine to form tee
tee = main_pipe.union(branch_pipe)
# Compute inner radius of main pipe after wall thickness
inner_radius = (main_od / 2) - main_wall_thk
# Create a solid cylinder slightly larger to allow shell operation
cylinder_solid = (
    cq.Workplane("XY")
    .circle(inner_radius + 2 * lip_thk)
    .extrude(lip_length)
)
# Shell inward to produce thin-walled lip of thickness lip_thk
lip_sleeve = cylinder_solid.shell(-lip_thk)
# Position lip at the far end of the main pipe (+Z direction)
lip_sleeve = lip_sleeve.translate((0, 0, main_length))
# Add lip to tee
tee_with_lip = tee.union(lip_sleeve)
# Add bolt holes on the positive X end face of the branch pipe
result = (
    tee_with_lip.faces(">X")
    .workplane()
    .pushPoints([(bolt_hole_offset, 0), (-bolt_hole_offset, 0)])
    .hole(bolt_hole_dia)
)
