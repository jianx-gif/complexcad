import cadquery as cq

clip_length = 80.0
clip_width = 30.0
clip_thickness = 5.0
rib_height = 3.0
rib_width = 6.0
hole_diameter = 4.0
hole_spacing_x = 20.0
hole_spacing_y = 12.0
chamfer_size = 0.8
corner_fillet_radius = 2.0


def hole_grid_points():
    start_x = -clip_length/2 + hole_spacing_x
    start_y = -clip_width/2 + hole_spacing_y
    pts = []
    for i in range(3):
        for j in range(2):
            pts.append((start_x + i*hole_spacing_x, start_y + j*hole_spacing_y))
    return pts

result = (
    cq.Workplane("XY")
    .rect(clip_length, clip_width)
    .extrude(clip_thickness)
    .edges("|Z")
    .fillet(corner_fillet_radius)
    .faces(">Z")
    .workplane()
    .center(0, clip_width/2 - rib_width/2)
    .rect(rib_width, clip_length)
    .extrude(rib_height)
    .faces(">Z")
    .workplane()
    .center(0, -(clip_width/2 - rib_width/2))
    .rect(rib_width, clip_length)
    .extrude(rib_height)
    .faces(">Z")
    .workplane()
    .pushPoints(hole_grid_points())
    .circle(hole_diameter/2)
    .cutBlind(clip_thickness + 0.1)
    .edges("|Z")
    .chamfer(chamfer_size)
)
