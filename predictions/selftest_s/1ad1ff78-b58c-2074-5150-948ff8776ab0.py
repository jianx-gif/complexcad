import cadquery as cq

outer_length = 80.0
outer_width = 50.0
outer_height = 20.0
wall_thickness = 2.0
rib_height = 3.0
rib_width = 4.0
rib_spacing = 10.0
fillet_radius = 2.0
chamfer_distance = 0.5
hole_diameter = 3.0
hole_offset_y = 12.0
hole_offset_x = 30.0

result = (
    cq.Workplane('XY')
    .box(outer_length, outer_width, outer_height, centered=(True, True, False))
    .shell(-wall_thickness)
    .faces('<Z')
    .workplane()
    .rarray(rib_spacing, 0, int((outer_width - 2*wall_thickness) / rib_spacing) + 1, 1, center=True)
    .rect(rib_width, outer_length - 2*wall_thickness)
    .extrude(rib_height)
    .edges('(<Z and >Y and |X)')
    .fillet(fillet_radius)
    .faces('>Y')
    .workplane(centerOption='CenterOfMass')
    .pushPoints([(-hole_offset_x/2, outer_height/2 - hole_offset_y), (hole_offset_x/2, outer_height/2 - hole_offset_y)])
    .hole(hole_diameter)
    .edges('>Z')
    .chamfer(chamfer_distance)
)
