import cadquery as cq

plate_length = 80.0
plate_width = 60.0
plate_thickness = 8.0
boss_radius = 15.0
through_hole_diameter = 8.0
rib_width = 4.0
rib_length = 20.0
rib_count = 6
mount_hole_diameter = 6.0
mount_hole_offset = 10.0
edge_chamfer = 0.5
fillet_radius = 0.2

base_plate = (
    cq.Workplane("XY")
    .rect(plate_length, plate_width)
    .extrude(plate_thickness)
)

boss = (
    cq.Workplane("XY")
    .circle(boss_radius)
    .extrude(plate_thickness)
)

through_hole = (
    cq.Workplane("XY")
    .circle(through_hole_diameter / 2)
    .extrude(plate_thickness + 1)
)

mount_points = [
    ( plate_length/2 - mount_hole_offset,  plate_width/2 - mount_hole_offset),
    (-plate_length/2 + mount_hole_offset,  plate_width/2 - mount_hole_offset),
    ( plate_length/2 - mount_hole_offset, -plate_width/2 + mount_hole_offset),
    (-plate_length/2 + mount_hole_offset, -plate_width/2 + mount_hole_offset)
]

plate_with_holes = (
    base_plate
    .cut(boss)
    .cut(through_hole)
    .faces(">Z")
    .workplane()
    .pushPoints(mount_points)
    .hole(mount_hole_diameter)
)

ribs = cq.Workplane("XY")
for i in range(rib_count):
    angle = i * 360.0 / rib_count
    rib = (
        cq.Workplane("XY")
        .center(boss_radius + rib_width/2, 0)
        .rect(rib_width, rib_length)
        .extrude(plate_thickness)
        .rotate((0,0,0), (0,0,1), angle)
    )
    ribs = ribs.union(rib)

result = (
    plate_with_holes
    .union(ribs)
    .edges("|Z")
    .chamfer(edge_chamfer)
    .edges("not |Z")
    .fillet(fillet_radius)
)
