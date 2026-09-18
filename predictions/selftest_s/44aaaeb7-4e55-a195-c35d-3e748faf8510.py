import cadquery as cq

clip_width = 80.0
clip_height = 30.0
clip_thickness = 2.0
tab_width = 12.0
tab_height = 15.0
mount_hole_dia = 4.0
mount_spacing = 20.0
rib_width = 6.0
rib_offset = 4.0
pocket_width = 40.0
pocket_height = 15.0
pocket_depth = 1.5
edge_roll_radius = 1.5
corner_radius = 1.0

base = (
    cq.Workplane('XY')
    .rect(clip_width, clip_height)
    .extrude(clip_thickness)
)

tab = (
    cq.Workplane('XY')
    .center(-clip_width / 2.0, 0.0)
    .rect(tab_width, tab_height)
    .extrude(clip_thickness)
)

rib = (
    cq.Workplane('XY')
    .center(0.0, rib_offset)
    .rect(rib_width, clip_height - 2 * rib_offset)
    .extrude(clip_thickness)
)

combined = base.union(tab).union(rib)

holes = (
    combined.faces('>Z')
    .workplane()
    .center(-clip_width / 4.0, -mount_spacing / 2.0)
    .circle(mount_hole_dia / 2.0)
    .cutThruAll()
    .center(0.0, mount_spacing)
    .circle(mount_hole_dia / 2.0)
    .cutThruAll()
)

pocketed = (
    holes.faces('>Z')
    .workplane()
    .center(0.0, 0.0)
    .rect(pocket_width, pocket_height)
    .cutBlind(pocket_depth)
)

final = (
    pocketed.edges('|Z').fillet(edge_roll_radius)
    .faces('>Z').edges().fillet(corner_radius)
)

result = final