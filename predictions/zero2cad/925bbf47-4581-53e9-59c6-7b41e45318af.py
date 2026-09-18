import cadquery as cq

plate_length = 80.0
plate_width = 60.0
plate_thickness = 5.0
boss_diameter = 40.0
boss_height = 8.0
hole_diameter = 6.0
hole_offset_x = 25.0
hole_offset_y = 15.0
chamfer_size = 0.8
rib_thickness = 2.0
rib_height = 4.0
rib_spacing = 15.0
fillet_radius = 0.5

base = (
    cq.Workplane("XY")
    .rect(plate_length, plate_width)
    .extrude(plate_thickness)
)

boss = (
    cq.Workplane("XY")
    .center(0, 0)
    .circle(boss_diameter / 2)
    .extrude(boss_height)
)

result = base.union(boss)

result = result.edges("|Z").chamfer(chamfer_size)

hole_positions = [
    (hole_offset_x, hole_offset_y),
    (-hole_offset_x, hole_offset_y),
    (hole_offset_x, -hole_offset_y),
    (-hole_offset_x, -hole_offset_y),
]

result = (
    result.faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)

rib_count = int((plate_width - rib_spacing) // rib_spacing) + 1
rib_positions = [(-plate_width/2 + rib_spacing/2 + i * rib_spacing) for i in range(rib_count)]

for y in rib_positions:
    rib = (
        cq.Workplane("XY")
        .center(0, y)
        .rect(rib_thickness, plate_length)
        .extrude(rib_height)
        .translate((0, 0, -rib_height))
    )
    result = result.union(rib)

result = result.edges(">Z").fillet(fillet_radius)
