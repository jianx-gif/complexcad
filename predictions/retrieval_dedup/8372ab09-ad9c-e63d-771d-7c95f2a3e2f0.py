import cadquery as cq

socket_radius = 12.0
socket_length = 20.0
branch_length = 40.0
branch_end_radius = 6.0
fillet_radius = 0.5
rib_width = 30.0
rib_thickness = 5.0
rib_height = 10.0
rib_offset = 4.0

central = cq.Workplane('XY').circle(socket_radius).extrude(socket_length)
central = central.edges().fillet(fillet_radius)

cone = cq.Solid.makeCone(socket_radius, branch_end_radius, branch_length)

branch_pos_x = (
    cq.Workplane()
    .add(cone)
    .rotate((0, 0, 0), (0, 1, 0), -90)
    .translate((0, 0, socket_length / 2))
)
branch_neg_x = (
    cq.Workplane()
    .add(cone)
    .rotate((0, 0, 0), (0, 1, 0), 90)
    .translate((0, 0, socket_length / 2))
)
branch_pos_y = (
    cq.Workplane()
    .add(cone)
    .rotate((0, 0, 0), (1, 0, 0), 90)
    .translate((0, 0, socket_length / 2))
)

tee = central.union(branch_pos_x).union(branch_neg_x).union(branch_pos_y)

ribs = []
for angle in [0, 90, 180, 270]:
    rib = (
        cq.Workplane('XY')
        .box(rib_width, rib_thickness, rib_height)
        .translate((socket_radius + rib_width / 2 - 0.5, 0, socket_length / 2))
        .rotate((0, 0, 0), (0, 0, 1), angle)
    )
    ribs.append(rib)

result = tee
for rib in ribs:
    result = result.union(rib)
