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
counterbore_diameter = 12.0
counterbore_depth = 2.0
hole_offset_x = 25.0
hole_offset_y = 15.0
edge_chamfer = 0.8
rib_chamfer = 0.5
side_rib_thickness = 4.0
side_rib_height = 2.5

result = (
    cq.Workplane("XY")
    .rect(plate_length, plate_width)
    .extrude(plate_thickness)
)
result = (
    result.faces(">Z")
    .workplane()
    .circle(rib_outer_radius)
    .extrude(rib_height)
)
result = (
    result.faces(">Z")
    .workplane()
    .circle(rib_inner_radius)
    .cutBlind(rib_height)
)
result = (
    result.faces(">Z")
    .workplane()
    .center(0, 0)
    .circle(pocket_radius)
    .cutBlind(pocket_depth)
)
hole_positions = [
    (hole_offset_x, hole_offset_y),
    (-hole_offset_x, hole_offset_y),
    (-hole_offset_x, -hole_offset_y),
    (hole_offset_x, -hole_offset_y),
]
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .cboreHole(
        diameter=hole_diameter,
        cboreDiameter=counterbore_diameter,
        cboreDepth=counterbore_depth,
        depth=plate_thickness + rib_height,
    )
)
result = result.edges("|Z").chamfer(edge_chamfer)
result = result.faces(">Z").edges("<<Z").chamfer(rib_chamfer)
# Side stiffening ribs created independently
x_offset = plate_length / 2 - side_rib_thickness / 2
side_rib = (
    cq.Workplane("YZ")
    .center(x_offset, 0)
    .rect(plate_width - 2 * edge_chamfer, side_rib_thickness)
    .extrude(side_rib_height)
)
result = result.union(side_rib)
side_rib_mirror = (
    cq.Workplane("YZ")
    .center(-x_offset, 0)
    .rect(plate_width - 2 * edge_chamfer, side_rib_thickness)
    .extrude(side_rib_height)
)
result = result.union(side_rib_mirror)
