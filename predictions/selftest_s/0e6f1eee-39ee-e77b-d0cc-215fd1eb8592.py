import cadquery as cq
# Parameters
plate_length = 80.0  # overall length, max 100
plate_width = 60.0   # overall width
plate_thickness = 12.0
groove_width = 20.0
groove_depth = 4.0
groove_length = 60.0
mount_hole_dia = 6.0
mount_hole_offset = 8.0
edge_chamfer = 1.0
# Base plate solid
base_plate = cq.Workplane('XY').box(plate_length, plate_width, plate_thickness, centered=(True, True, False))
# Oil groove profile on top face
groove_profile = (
    cq.Workplane('XY', origin=(0, 0, plate_thickness))
    .moveTo(-groove_length/2, -groove_width/2)
    .line(groove_length, 0)
    .line(0, groove_width)
    .line(-groove_length, 0)
    .close()
)
# Cut groove recessed into plate
plate_with_groove = base_plate.cut(
    groove_profile.extrude(-groove_depth)
)
# Chamfer outer edges
plate_chamfered = plate_with_groove.edges(">Z and (<<X or >>X or <<Y or >>Y)").chamfer(edge_chamfer)
# Mounting holes near corners (offset from edges)
px = plate_length/2 - mount_hole_offset - mount_hole_dia/2
py = plate_width/2 - mount_hole_offset - mount_hole_dia/2
result = (
    plate_chamfered
    .faces("<Z")
    .workplane()
    .pushPoints([
        (px, py),
        (-px, py),
        (-px, -py),
        (px, -py)
    ])
    .hole(mount_hole_dia)
)
