import cadquery as cq

main_diameter = 30.0
branch_diameter = 20.0
pipe_thickness = 2.0
main_length = 80.0
branch_length = 60.0
rib_width = 20.0
rib_height = 15.0
rib_thickness = 5.0
fillet_radius = 0.3

main_outer = cq.Workplane("XY").circle(main_diameter/2).extrude(main_length)
branch_outer = (cq.Workplane("XY")
    .transformed(offset=(0,0,main_length/2), rotate=(0,90,0))
    .circle(branch_diameter/2)
    .extrude(branch_length))
outer_union = main_outer.union(branch_outer)
outer_fillet = outer_union.edges().fillet(fillet_radius)

main_inner = cq.Workplane("XY").circle((main_diameter-2*pipe_thickness)/2).extrude(main_length)
branch_inner = (cq.Workplane("XY")
    .transformed(offset=(0,0,main_length/2), rotate=(0,90,0))
    .circle((branch_diameter-2*pipe_thickness)/2)
    .extrude(branch_length))
inner_union = main_inner.union(branch_inner)

tee_hollow = outer_fillet.cut(inner_union)

rib = (cq.Workplane("XY")
    .transformed(offset=(main_diameter/2 + rib_thickness/2, 0, main_length/2))
    .rect(rib_width, rib_height)
    .extrude(rib_thickness))

result = tee_hollow.union(rib)
