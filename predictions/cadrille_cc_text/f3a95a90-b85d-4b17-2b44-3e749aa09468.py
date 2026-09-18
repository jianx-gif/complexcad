import cadquery as cq
plate_width = 80.0
plate_depth = 30.0
plate_thickness = 6.0
boss_width = 30.0
boss_depth = 15.0
boss_height = 5.0
fillet_radius = 2.0
chamfer_distance = 0.8
pocket_width = 40.0
pocket_depth = 20.0
pocket_thickness = 3.0
pocket_margin = 10.0
result = (
    cq.Workplane("XY")
    .rect(plate_width, plate_depth)
    .extrude(plate_thickness)
    .edges("|Z")
    .fillet(fillet_radius)
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(pocket_width, pocket_depth)
    .cutBlind(-pocket_thickness)
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(pocket_width, pocket_depth)
    .cutBlind(-pocket_thickness)
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(pocket_width, pocket_depth)
    .cutBlind(-pocket_thickness)
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(pocket_width, pocket_depth)
    .cutBlind(-pocket_thickness)
    .faces(">Z")
    .workplane()
    .pushPoints([
        (0, 0),
        (0, -plate_thickness),
        (-0.5, -plate_thickness),
        (0.5, -plate_thickness),
        (0.5, 0)
    ])
    .cskHole(pocket_width, pocket_depth, 360)
)
