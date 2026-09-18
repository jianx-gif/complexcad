import cadquery as cq

overall_width = 80
overall_height = 60
wall_thickness = 5
length = 100
slot_width = 20
slot_height = 30
hole_diameter = 6
hole_spacing = 40
pocket_width = 30
pocket_depth = 10
pocket_length = 40
chamfer_size = 2

base = cq.Workplane('XY').rect(overall_width, overall_height).extrude(length)

inner_cut = (cq.Workplane('XY')
    .rect(overall_width - wall_thickness, overall_height - 2 * wall_thickness)
    .translate((wall_thickness / 2, 0, 0))
    .extrude(length)
)
channel = base.cut(inner_cut)

slot = (cq.Workplane('XY')
    .rect(slot_width, slot_height)
    .translate(((overall_width - slot_width) / 2, 0, 0))
    .extrude(length)
)
channel = channel.cut(slot)

num_holes = int(length / hole_spacing) + 1
channel = (channel
    .faces('>Y')
    .workplane()
    .rarray(0, hole_spacing, 1, num_holes)
    .hole(hole_diameter)
)

pocket = (cq.Workplane('XY')
    .rect(pocket_width, pocket_depth)
    .translate((0, -overall_height / 2 + wall_thickness / 2, length / 4))
    .extrude(pocket_length)
)
channel = channel.cut(pocket)

channel = channel.edges('|Z').chamfer(chamfer_size)

result = channel