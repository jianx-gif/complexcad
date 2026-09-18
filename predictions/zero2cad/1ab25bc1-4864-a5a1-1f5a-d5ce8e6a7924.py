import cadquery as cq

outer_radius = 45.0
inner_radius = 20.0
block_height = 60.0
wall_thickness = 2.0
chamfer_size = 1.0
mount_hole_dia = 5.0
mount_hole_offset = 20.0
rib_thickness = 3.0
rib_height = 15.0
rib_count = 4

profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius, block_height)
    .lineTo(inner_radius, block_height)
    .lineTo(inner_radius, block_height * 0.6)
    .threePointArc((inner_radius - 5, block_height * 0.5), (inner_radius, block_height * 0.4))
    .lineTo(inner_radius, 0)
    .close()
)

solid = profile.revolve()

hollow = solid.shell(-wall_thickness)

chamfered = hollow.faces(">Z").edges().chamfer(chamfer_size)

hole_positions = [
    (mount_hole_offset, 0),
    (-mount_hole_offset, 0),
    (0, mount_hole_offset),
    (0, -mount_hole_offset),
]

with_holes = (
    chamfered.faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(mount_hole_dia)
)

rib = (
    cq.Workplane("XY")
    .center(inner_radius + wall_thickness / 2, 0)
    .rect(rib_thickness, rib_height)
    .extrude(block_height)
)

ribs = rib
for i in range(1, rib_count):
    angle = 360.0 / rib_count * i
    ribs = ribs.union(rib.rotate((0, 0, 0), (0, 0, 1), angle))

result = with_holes.union(ribs)
