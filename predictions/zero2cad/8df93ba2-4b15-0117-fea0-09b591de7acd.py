import cadquery as cq

outer_diameter = 80.0
inner_diameter = 30.0
thickness = 15.0
wall_thickness = 3.0
keyway_width = 8.0
keyway_depth = 3.0
fillet_radius = 2.0

outer_radius = outer_diameter / 2.0
inner_radius = inner_diameter / 2.0

base = cq.Workplane('XY').circle(outer_radius).extrude(thickness)
ring = base.shell(wall_thickness)
ring = ring.edges().fillet(fillet_radius)
keyway = (
    cq.Workplane('XY')
    .box(keyway_width, keyway_depth, thickness)
    .translate((inner_radius - keyway_depth / 2.0, 0, 0))
)
result = ring.cut(keyway)
