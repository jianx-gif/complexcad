import cadquery as cq
outer_radius = 30.0
inner_radius = 25.0
base_thickness = 5.0
body_height = 40.0
flange_radius = 35.0
flange_thickness = 8.0
counter_sink_diameter = 6.0
counter_sink_angle = 90.0
base_fillet_radius = 2.0
base = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(base_thickness)
    .edges()
    .chamfer(base_fillet_radius)
)
base = (
    cq.Workplane("XY")
    .circle(inner_radius)
    .extrude(base_thickness)
    .translate((0, 0, base_thickness))
)
base = base.cut(base)
flange = (
    cq.Workplane("XY")
    .circle(flange_radius)
    .extrude(flange_thickness)
    .translate((0, 0, base_thickness))
)
base = base.union(flange)
base = base.edges().chamfer(base_fillet_radius)
base = (
    base.faces(">Z")
    .workplane()
    .circle(counterbore_diameter/2)
    .cutBlind(counterbore_diameter/2)
)
base = base.cut(flange)
base = base.edges().chamfer(base_fillet_radius)
base = base.faces(">Z").edges().chamfer(base_fillet_radius)
result = base
