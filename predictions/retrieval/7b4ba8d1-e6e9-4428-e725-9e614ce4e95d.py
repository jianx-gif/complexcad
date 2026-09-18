import cadquery as cq

case_length = 80.0
case_width = 50.0
case_height = 20.0
wall_thickness = 2.0
inner_length = case_length - 2 * wall_thickness
inner_width = case_width - 2 * wall_thickness
shelf_thickness = 3.0
chamfer_distance = 1.0
hole_diameter = 3.0
hole_spacing_x = 60.0
open_length = inner_length - 4.0
open_width = inner_width - 4.0

result = (
    cq.Workplane("XY")
    .box(case_length, case_width, case_height, centered=(True, True, False))
    .shell(-wall_thickness)
    .faces(">Z")
    .workplane()
    .rect(open_length, open_width)
    .cutBlind(-wall_thickness)
    .faces(">Y")
    .edges("|Z and >Y")
    .chamfer(chamfer_distance)
    .faces("<Z")
    .workplane()
    .rect(inner_length, inner_width)
    .extrude(shelf_thickness)
    .faces(">Y")
    .workplane(offset=case_height/2 - wall_thickness/2)
    .pushPoints([(-hole_spacing_x/2, 0), (hole_spacing_x/2, 0)])
    .hole(hole_diameter)
    .faces("<Y")
    .workplane(offset=case_height/2 - wall_thickness/2)
    .pushPoints([(-hole_spacing_x/2, 0), (hole_spacing_x/2, 0)])
    .hole(hole_diameter)
)
