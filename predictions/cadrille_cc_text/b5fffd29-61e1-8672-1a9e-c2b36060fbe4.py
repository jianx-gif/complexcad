import cadquery as cq
base_length = 80.0
base_width = 60.0
base_thickness = 10.0
fin_height = 5.0
fin_thickness = 2.0
fin_spacing = 3.0
chamfer_distance = 1.0
mount_hole_dia = 4.0
mount_hole_spacing = 30.0
base = (
    cq.Workplane("XY")
    .rect(base_length, base_width)
    .extrude(base_thickness)
)
fin = (
    cq.Workplane("XY")
    .rect(base_length - 2 * fin_spacing, base_width - 2 * fin_spacing)
    .extrude(fin_height)
    .translate((0, 0, base_thickness))
)
fin = fin.cut(fin)
fin = fin.edges("|Z").chamfer(chamfer_distance)
result = (
    cq.Workplane("XY")
    .center(0, 0)
    .circle(fin_thickness)
    .extrude(fin_height)
)
result = result.cut(fin)
result = (
    result
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .hole(mount_hole_dia)
)
mount_points = [
    (-mount_hole_spacing/2, 0),
    (mount_hole_spacing/2, 0)
]
result = (
    result
    .faces(">Z")
    .workplane()
    .pushPoints(mount_points)
    .hole(mount_hole_dia)
)
result = (
    result
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(fin_thickness, fin_height)
    .extrude(fin_thickness)
)
