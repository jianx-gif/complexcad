import cadquery as cq

outer_length = 80.0
outer_width = 40.0
outer_height = 30.0
wall_thickness = 3.0
chamfer_size = 1.5
hole_diameter = 4.0
hole_spacing = 30.0

solid = (
    cq.Workplane("XY")
    .rect(outer_length, outer_width)
    .extrude(outer_height)
)

hollow = solid.shell(wall_thickness)

result = (
    hollow
    .edges("|X")
    .chamfer(chamfer_size)
    .faces(">Y")
    .workplane()
    .pushPoints([(-hole_spacing/2, outer_height/2), (hole_spacing/2, outer_height/2)])
    .hole(hole_diameter)
)
