import cadquery as cq
outer_radius = 30.0
wall_thickness = 5.0
height = 40.0
rib_width = 3.0
rib_thickness = 1.0
rib_height = 30.0
chamfer_size = 1.0
latch_groove_radius = 25.0
latch_groove_depth = 2.0
outer_radius = outer_radius - wall_thickness
inner_radius = outer_radius - wall_thickness
base = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(height)
    .edges()
    .chamfer(chamfer_size)
)
rib = (
    cq.Workplane("XY")
    .box(rib_width, rib_thickness, height)
    .translate((outer_radius - rib_thickness/2, 0, 0))
)
rib = rib.translate((outer_radius - rib_thickness/2, 0, 0))
rib = rib.translate((outer_radius - rib_thickness/2, 0, 0))
result = base.union(rib)
result = result.edges("|Z").chamfer(chamfer_size)
result = result.edges("|Z").chamfer(chamfer_size)
result = (
    result.faces(">Z")
    .workplane()
    .polarArray(radius=outer_radius - wall_thickness/2, startAngle=0, count=rib_count, angle=360)
    .rect(rib_width, rib_thickness)
    .cutBlind(-rib_height)
)
result = result.edges("|Z").chamfer(chamfer_size)
