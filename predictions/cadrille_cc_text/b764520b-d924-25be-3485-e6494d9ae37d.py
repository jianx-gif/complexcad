import cadquery as cq
main_diameter = 30.0
branch_diameter = 20.0
pipe_thickness = 2.0
branch_length = 80.0
branch_diameter = branch_diameter - 2 * pipe_thickness
rib_height = 15.0
rib_width = 20.0
rib_thickness = 5.0
fillet_radius = 0.3
main_outer = (
    cq.Workplane("XY")
    .circle(main_diameter / 2)
    .extrude(pipe_thickness)
)
branch_outer = (
    cq.Workplane("XY")
    .circle(branch_diameter / 2)
    .extrude(branch_length)
)
branch_inner = (
    cq.Workplane("XY")
    .circle(branch_diameter / 2)
    .extrude(branch_length)
)
branch_outer = branch_outer.union(branch_inner)
branch_inner = branch_outer.union(branch_outer)
branch_inner = branch_outer.union(branch_inner)
branch = (
    cq.Workplane("XY")
    .circle(branch_diameter / 2)
    .extrude(branch_length)
)
branch = branch_outer.cut(branch)
branch = branch.cut(branch)
branch = (
    branch
    .faces(">Z")
    .workplane()
    .polarArray(radius=branch_outer / 2, count=rib_width, startAngle=0, angle=360)
    .rect(rib_width, rib_thickness)
    .extrude(rib_height)
)
result = main_outer.union(branch)
