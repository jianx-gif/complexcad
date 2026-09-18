import cadquery as cq
plate_length = 80.0
plate_width = 60.0
plate_thickness = 5.0
rib_outer_radius = 20.0
rib_inner_radius = 15.0
rib_height = 3.0
pocket_radius = 8.0
pocket_depth = 4.0
hole_diameter = 6.0
hole_offset_x = 25.0
hole_offset_y = 15.0
edge_chamfer = 0.8
rib_chamfer = 0.5
rib_inner_radius = 15.0
rib_outer_radius = plate_width / 2.0
rib_outer_radius = plate_width / 2.0
base_plate = (
    cq.Workplane("XY")
    .rect(plate_length, plate_width)
    .extrude(plate_thickness)
)
rib = (
    cq.Workplane("XY")
    .rect(rib_outer_radius, rib_outer_radius)
    .extrude(rib_height)
    .translate((0, 0, plate_thickness))
)
combined = base_plate.union(rib)
hole_positions = [
    (hole_offset_x, hole_offset_y),
    (-hole_offset_x, hole_offset_y),
    (-hole_offset_x, -hole_offset_y),
    (hole_offset_x, -hole_offset_y),
    (-hole_offset_x, -hole_offset_y),
]
result = (
    combined
    .faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .cboreHole(hole_diameter, counterbore_diameter, counterbore_depth)
)
