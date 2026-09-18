import cadquery as cq
outer_diameter = 70.0
wall_thickness = 8.0
wall_height = 30.0
wall_thickness = 4.0
rib_width = 12.0
rib_height = 10.0
rib_thickness = 4.0
rib_spacing = 20.0
chamfer_size = 1.0
hole_diameter = 5.0
hole_spacing = 30.0
hole_offset = 10.0
base = cq.Workplane('XY').circle(outer_diameter/2).extrude(wall_thickness)
rib = (
    cq.Workplane('XY')
    .center(0, 0)
    .rect(rib_width, rib_height)
    .extrude(wall_thickness)
)
rib = rib.translate((0, 0, wall_thickness))
rib = rib.translate((0, 0, wall_thickness))
rib = rib.translate((0, 0, wall_thickness))
rib = rib.translate((0, 0, wall_thickness))
combined = base.union(rib)
combined = combined.faces('>Z').edges().chamfer(chamfer_size)
hole_positions = [
    (hole_offset, hole_offset),
    (-hole_offset, hole_offset),
    (hole_offset, -hole_offset),
    (-hole_offset, hole_offset),
    (hole_offset, hole_offset),
]
result = (
    combined.faces('>Z').workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
