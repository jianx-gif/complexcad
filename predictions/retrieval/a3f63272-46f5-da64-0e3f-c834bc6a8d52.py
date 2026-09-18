import cadquery as cq

outer_diameter = 80.0
plate_thickness = 5.0
central_hole_diameter = 12.0
perimeter_fillet_radius = 1.0
edge_chamfer = 0.5
mount_hole_diameter = 5.0
mount_hole_offset = 20.0
slot_width = 4.0
slot_length = 20.0
slot_offset = (outer_diameter / 2) - (slot_length / 2) - 5.0
rib_thickness = 2.0
rib_height = 2.0
rib_spacing = 20.0

base = (
    cq.Workplane('XY')
    .circle(outer_diameter / 2)
    .extrude(plate_thickness)
)
result = (
    base
    .faces('>Z')
    .workplane()
    .hole(central_hole_diameter)
)
for angle in (0, 90):
    result = (
        result
        .faces('>Z')
        .workplane()
        .center(slot_offset, 0)
        .rotate((0, 0, 0), (0, 0, 1), angle)
        .rect(slot_length, slot_width)
        .cutBlind(-plate_thickness)
    )
mount_points = [
    (mount_hole_offset, 0),
    (-mount_hole_offset, 0),
    (0, mount_hole_offset),
    (0, -mount_hole_offset),
]
result = (
    result
    .faces('>Z')
    .workplane()
    .pushPoints(mount_points)
    .hole(mount_hole_diameter)
)
num_ribs_x = int((outer_diameter - rib_spacing) // rib_spacing)
num_ribs_y = int((outer_diameter - rib_spacing) // rib_spacing)
for i in range(-num_ribs_x // 2, num_ribs_x // 2 + 1):
    for j in range(-num_ribs_y // 2, num_ribs_y // 2 + 1):
        x = i * rib_spacing
        y = j * rib_spacing
        if (x**2 + y**2) < ((central_hole_diameter/2 + rib_thickness)**2):
            continue
        result = (
            result
            .faces('<Z')
            .workplane()
            .center(x, y)
            .rect(rib_thickness, rib_height)
            .cutBlind(-rib_thickness)
        )
result = result.faces('>Z').edges().fillet(perimeter_fillet_radius)
result = result.faces('<Z').edges().chamfer(edge_chamfer)
