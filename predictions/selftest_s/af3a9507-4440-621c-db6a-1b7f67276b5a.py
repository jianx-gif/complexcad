import cadquery as cq

conduit_length = 80.0
profile_top_width = 30.0
profile_bottom_width = 15.0
profile_height = 25.0
wall_thickness = 3.0
rib_thickness = 2.0  # not used for height, using rib_width
rib_width = 5.0
rib_spacing = 20.0
chamfer_depth = 1.5
fillet_radius = 1.0

outer = (
    cq.Workplane('YZ')
    .polyline([
        (0, 0),
        (profile_top_width / 2, 0),
        (profile_bottom_width / 2, profile_height),
        (-profile_bottom_width / 2, profile_height),
        (-profile_top_width / 2, 0),
        (0, 0)
    ])
    .close()
    .extrude(conduit_length)
)

hollow = outer.shell(-wall_thickness)

interior_height = profile_height - 2 * wall_thickness
cavity_y_min = -profile_top_width / 2 + wall_thickness
cavity_y_max =  profile_top_width / 2 - wall_thickness
available_width = cavity_y_max - cavity_y_min

rib_solids = []
num_ribs = int((available_width - rib_width) // rib_spacing) + 1
for i in range(num_ribs):
    y_center = cavity_y_min + rib_width / 2 + i * rib_spacing
    rib = (
        cq.Workplane('YZ')
        .center(y_center, interior_height / 2)
        .rect(rib_width, interior_height)
        .extrude(conduit_length)
    )
    rib_solids.append(rib)

if rib_solids:
    ribs_union = rib_solids[0]
    for r in rib_solids[1:]:
        ribs_union = ribs_union.union(r)
    combined = hollow.union(ribs_union)
else:
    combined = hollow

result = (
    combined
    .faces('<X')
    .edges()
    .chamfer(chamfer_depth, chamfer_depth)
)
