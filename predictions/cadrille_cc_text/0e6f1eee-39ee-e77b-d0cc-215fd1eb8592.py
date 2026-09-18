import cadquery as cq
plate_length = 80.0
plate_width = 60.0
plate_thickness = 12.0
groove_width = 20.0
groove_depth = 4.0
mount_hole_dia = 6.0
mount_hole_offset = 8.0
edge_chamfer = 1.0
base = cq.Workplane('XY').box(plate_length, plate_width, plate_thickness)
groove = (
    cq.Workplane('XY')
    .center(0, 0)
    .box(groove_width, groove_depth, groove_depth)
)
base = base.cut(groove)
base = base.edges('|Z').chamfer(edge_chamfer)
base = base.faces('>Z').workplane().hole(mount_hole_dia)
mount_points = [
    (mount_hole_offset, 0),
    (-mount_hole_offset, 0),
    (0, mount_hole_offset),
    (0, -mount_hole_offset),
]
base = (
    base.faces('>Z')
    .workplane()
    .pushPoints(mount_points)
    .hole(mount_hole_dia)
)
base = base.edges('>Z').chamfer(edge_chamfer)
result = base
