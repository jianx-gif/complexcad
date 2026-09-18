import cadquery as cq
outer_radius = 45.0
wall_thickness = 5.0
inner_radius = outer_radius - wall_thickness
rib_width = 20.0
rib_height = 10.0
rib_thickness = 4.0
rib_spacing = 12.0
hole_diameter = 5.0
hole_spacing = 30.0
hole_offset = 10.0
chamfer_size = 0.5
base = cq.Workplane('XY').circle(outer_radius).extrude(wall_thickness)
rib = (cq.Workplane('XY')
        .rect(rib_width, rib_height)
        .extrude(wall_thickness))
rib = (base.faces('>Z')
        .workplane()
        .hole(inner_radius * 2)
        .rect(rib_width, rib_height)
        .extrude(wall_thickness))
combined = base.union(rib)
hole_positions = [
    (hole_offset, 0),
    (hole_offset, 0),
    (0, hole_offset),
    (0, -hole_offset),
]
result = combined
for i in range(1, hole_spacing):
    angle = i * 360.0 / hole_spacing
    x = hole_spacing * math.cos(angle)
    y = hole_spacing * math.sin(angle)
    result = result.cut(hole_positions)
