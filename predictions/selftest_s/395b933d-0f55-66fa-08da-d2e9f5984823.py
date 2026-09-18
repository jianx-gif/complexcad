import cadquery as cq

outer_diameter = 60.0
height = 30.0
wall_thickness = 2.5
rib_width = 8.0
rib_thickness = 3.0
central_hole_diameter = 10.0
chamfer_dist = 1.0

outer_radius = outer_diameter / 2.0
inner_radius = outer_radius - wall_thickness

# Base shell
result = (
    cq.Workplane('XY')
    .circle(outer_radius)
    .extrude(height)
    .faces('<Z')
    .workplane()
    .circle(inner_radius)
    .cutBlind(-height)
)

# Rib block intersecting shell
rib = (
    cq.Workplane('XY')
    .box(rib_thickness, height, rib_width)
    .translate((outer_radius - rib_thickness/2.0, height/2.0, 0))
)
rib_rotated = rib.rotate((0, 0, 0), (0, 0, 1), 180)
result = result.union(rib).union(rib_rotated)

# Central through hole
result = (
    result.faces('>Z')
    .workplane()
    .circle(central_hole_diameter/2.0)
    .cutThruAll()
)

# Chamfer top outer edge
result = result.edges('>Z').chamfer(chamfer_dist)
