import cadquery as cq
outer_diameter = 80.0
inner_diameter = 30.0
thickness = 40.0
rib_height = 12.0
rib_width = 6.0
rib_thickness = 4.0
rib_spacing = 12.0
hole_diameter = 8.0
hole_depth = thickness / 2.0
chamfer_size = 1.0
rib_count = int(36 / rib_spacing)
base = cq.Workplane('XY').circle(outer_diameter / 2).extrude(thickness)
rib = (
    cq.Workplane('XY')
    .center(outer_diameter / 2 - rib_width / 2, 0)
    .rect(rib_width, rib_thickness)
    .extrude(thickness)
)
rib = rib.edges('|Z').chamfer(chamfer_size)
rib = (
    rib.faces('>Z')
    .workplane()
    .rect(rib_width, rib_thickness)
    .extrude(rib_height)
)
rib = rib.union(rib)
hole_positions = [
    (inner_diameter / 2 - rib_spacing / 2, inner_diameter / 2 - rib_spacing / 2),
    (inner_diameter / 2 - rib_spacing / 2, inner_diameter / 2 + rib_spacing / 2),
    (inner_diameter / 2 - rib_spacing / 2, inner_diameter / 2 + rib_spacing / 2),
]
result = (
    rib.faces('>Z')
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
