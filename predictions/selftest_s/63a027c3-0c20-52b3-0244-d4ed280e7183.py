import cadquery as cq

outer_radius = 45.0
inner_radius = 20.0
total_height = 20.0
frame_thickness = 6.0
hex_flat_distance = 5.5
hex_depth = 2.5
hole_diameter = 5.5
hole_count = 8
hole_circle_radius = outer_radius - frame_thickness/2
chamfer_dist = 0.8
pocket_width = 6.0
pocket_depth = 4.0
pocket_cut_depth = 3.0
pocket_count = 6
pocket_radius = (inner_radius + outer_radius) / 2
reinforcement_radius = inner_radius + 1.0

profile = (
    cq.Workplane('XZ')
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, total_height - frame_thickness)
    .lineTo(outer_radius, total_height - frame_thickness)
    .lineTo(outer_radius, 0)
    .close()
)

frame = profile.revolve()

reinforcement = (
    cq.Workplane('XY')
    .circle(reinforcement_radius)
    .extrude(total_height)
)

frame = frame.union(reinforcement)

hex_cut = (
    cq.Workplane('XY')
    .polygon(6, hex_flat_distance * 2)
    .extrude(-hex_depth)
    .translate((0, 0, total_height - hex_depth))
)

frame = frame.cut(hex_cut)

pocket_wp = frame.faces('>Z').workplane()

frame = (
    pocket_wp.polarArray(pocket_radius, 0, 360, pocket_count)
    .rect(pocket_width, pocket_depth)
    .cutBlind(-pocket_cut_depth)
)

frame = frame.edges('>Z').chamfer(chamfer_dist)

hole_wp = frame.faces('>Z').workplane()

frame = (
    hole_wp.polarArray(hole_circle_radius, 0, 360, hole_count)
    .hole(hole_diameter)
)

result = frame
