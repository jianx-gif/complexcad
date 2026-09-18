import cadquery as cq

frame_length = 80
frame_width = 50
frame_height = 15
wall_thickness = 3
base_thickness = 5
rib_height = 8
rib_thickness = 2
hole_diameter = 8
hole_depth = 10
mount_hole_diameter = 4
mount_hole_offset = 6
chamfer_size = 0.5

outer = cq.Workplane("XY").rect(frame_length, frame_width).extrude(frame_height)
inner_cut = (
    cq.Workplane("XY", origin=(0, 0, base_thickness))
    .rect(frame_length - 2 * wall_thickness, frame_width - 2 * wall_thickness)
    .extrude(frame_height - base_thickness)
)
housing = outer.cut(inner_cut)

rib1 = (
    cq.Workplane("XY", origin=(frame_length / 2 - wall_thickness - rib_thickness / 2, 0, base_thickness))
    .rect(rib_thickness, frame_width - 2 * wall_thickness)
    .extrude(rib_height)
)

rib2 = (
    cq.Workplane("XY", origin=(0, frame_width / 2 - wall_thickness - rib_thickness / 2, base_thickness))
    .rect(frame_length - 2 * wall_thickness, rib_thickness)
    .extrude(rib_height)
)

rib3 = (
    cq.Workplane("XY", origin=(frame_length / 2 - wall_thickness - rib_thickness, frame_width / 2 - wall_thickness - rib_thickness, base_thickness + rib_height))
    .rect(rib_thickness, rib_thickness)
    .extrude(rib_height)
)

housing = housing.union(rib1).union(rib2).union(rib3)

blind_hole = (
    cq.Workplane("XY", origin=(0, 0, base_thickness))
    .circle(hole_diameter / 2)
    .extrude(-hole_depth)
)
housing = housing.cut(blind_hole)

mount_hole_positions = [
    (mount_hole_offset - frame_length / 2, mount_hole_offset - frame_width / 2),
    (-mount_hole_offset + frame_length / 2, mount_hole_offset - frame_width / 2),
    (mount_hole_offset - frame_length / 2, -mount_hole_offset + frame_width / 2),
    (-mount_hole_offset + frame_length / 2, -mount_hole_offset + frame_width / 2),
]
for x, y in mount_hole_positions:
    hole = (
        cq.Workplane("XY", origin=(x, y, base_thickness))
        .circle(mount_hole_diameter / 2)
        .extrude(-(wall_thickness + 0.5))
    )
    housing = housing.cut(hole)

housing = housing.edges("|Z").chamfer(chamfer_size)

result = housing