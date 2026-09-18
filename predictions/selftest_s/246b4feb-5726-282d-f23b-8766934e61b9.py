import cadquery as cq

plate_length = 80.0
plate_width = 60.0
plate_thickness = 5.0
rib_height = 4.0
rib_width = 12.0
rib_margin = 8.0
corner_hole_diameter = 6.0
corner_counter_diameter = 10.0
central_hole_diameter = 8.0
central_counter_diameter = 12.0
edge_chamfer = 0.8
rib_fillet = 1.0
pocket_depth = 3.0
pocket_spacing = 15.0
pocket_margin = 10.0

base = (
    cq.Workplane("XY")
    .rect(plate_length, plate_width)
    .extrude(plate_thickness)
    .edges()
    .chamfer(edge_chamfer)
)

rib_length = plate_length - 2 * rib_margin
rib = (
    cq.Workplane("XY")
    .center(0, 0)
    .rect(rib_length, rib_width)
    .extrude(rib_height)
    .union(
        cq.Workplane("XY")
        .center(rib_length/2 - rib_width/2, 0)
        .circle(rib_width/2)
        .extrude(rib_height)
    )
)

result = base.union(rib)

corner_offset_x = plate_length/2 - corner_hole_diameter
corner_offset_y = plate_width/2 - corner_hole_diameter

result = (
    result
    .faces(">Z")
    .workplane()
    .pushPoints([
        ( corner_offset_x,  corner_offset_y),
        (-corner_offset_x,  corner_offset_y),
        (-corner_offset_x, -corner_offset_y),
        ( corner_offset_x, -corner_offset_y)
    ])
    .cskHole(corner_hole_diameter, corner_counter_diameter, plate_thickness+1)
)

result = (
    result
    .faces(">Z")
    .workplane()
    .center(0,0)
    .cskHole(central_hole_diameter, central_counter_diameter, plate_thickness+1)
)

pocket_origin_x = -plate_length/2 + pocket_margin
pocket_origin_y = -plate_width/2 + pocket_margin

num_x = int((plate_length - 2 * pocket_margin) // pocket_spacing) + 1
num_y = int((plate_width - 2 * pocket_margin) // pocket_spacing) + 1

points = []
for i in range(num_x):
    for j in range(num_y):
        x = pocket_origin_x + i * pocket_spacing
        y = pocket_origin_y + j * pocket_spacing
        # avoid cutting under rib and central hole
        if abs(x) < rib_length/2 + rib_width and abs(y) < rib_width/2:
            continue
        if (x**2 + y**2)**0.5 < central_hole_diameter:
            continue
        points.append((x, y))

result = (
    result
    .faces("<Z")
    .workplane()
    .pushPoints(points)
    .hole(pocket_spacing/3, depth=pocket_depth)
)
