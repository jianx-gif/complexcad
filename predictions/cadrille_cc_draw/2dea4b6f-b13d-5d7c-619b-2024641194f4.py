import cadquery as cq
outer_radius = 40
inner_radius = 20
thickness = 10
rib_width = 4
rib_height = 3
rib_thickness = 2
rib_offset = 5
chamfer_size = 0.5
hole_diameter = 5
hole_spacing = 12
hole_count = 6
hole_radius = outer_radius - inner_radius - 2
base = cq.Workplane('XY').circle(outer_radius).extrude(thickness)
rib = cq.Workplane('XY').circle(inner_radius).extrude(thickness)
rib = rib.translate((0, 0, thickness))
rib = rib.translate((0, 0, thickness))
rib = rib.translate((0, 0, thickness + rib_thickness))
rib = rib.translate((0, 0, thickness + rib_thickness))
rib = rib.translate((0, 0, thickness + rib_thickness))
rib = rib.translate((0, 0, thickness + rib_thickness))
rib = rib.translate((0, 0, thickness + rib_thickness))
rib = rib.translate((0, 0, thickness + rib_thickness))
rib = rib.translate((0, 0, thickness + rib_thickness))
rib = rib.translate((0, 0, thickness + rib_thickness))
result = base.union(rib)
hole_positions = [
    (hole_count-1)*hole_count,
    (-hole_count-1)*hole_spacing),
    (hole_count-1)*hole_spacing),
    (hole_count-1)*hole_spacing,
    (-hole_count-1)*hole_spacing),
    (hole_count-1)*hole_spacing),
    (hole_count-1)*hole_spacing,
]
result = result.faces('>Z').workplane().pushPoints(hole_positions).hole(hole_diameter)
