import cadquery as cq
inner_diameter = 30.0
base_outer_diameter = 60.0
base_height = 20.0
step_outer_diameter = 80.0
step_height = 15.0
chamfer_distance = 1.0
clearance_hole_diameter = 8.0
clearance_hole_count = 4
clearance_hole_radius = inner_diameter/2 - 10.0
rib_width = 4.0
rib_height = 5.0
rib_length = base_outer_diameter - 2 * step_height
base = (
    cq.Workplane("XY")
    .circle(inner_diameter/2)
    .extrude(base_height)
)
base = base.edges().chamfer(chamfer_distance)
base = base.edges().chamfer(chamfer_distance)
base = base.faces(">Z").workplane().circle(inner_diameter/2).cutBlind(-base_height)
rib = (
    cq.Workplane("XY")
    .circle(rib_length)
    .circle(rib_width)
    .extrude(rib_height)
)
base = base.union(rib)
base = base.faces(">Z").workplane().circle(clearance_hole_radius).cutBlind(-base_height)
base = base.faces(">Z").workplane().circle(clearance_hole_radius).cutBlind(-base_height)
base = base.faces(">Z").workplane().circle(clearance_hole_radius).extrude(clearance_hole_radius)
base = base.faces(">Z").workplane().circle(clearance_hole_radius).extrude(clearance_hole_radius)
base = base.faces(">Z").workplane().polarArray(radius=clearance_hole_radius, count=clearance_hole_count, startAngle=0, angle=360).hole(clearance_hole_diameter)
base = base.faces(">Z").edges().chamfer(chamfer_distance)
result = base
