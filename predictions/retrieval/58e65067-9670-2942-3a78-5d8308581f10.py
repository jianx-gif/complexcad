import cadquery as cq

outer_radius = 40.0
wall_thickness = 2.0
length = 80.0
outer_fillet_radius = 3.0
hole_diameter = 5.0
hole_radius = outer_radius - wall_thickness/2

result = (
    cq.Workplane('XY')
    .circle(outer_radius)
    .extrude(length)
    .faces('>Z')
    .edges()
    .fillet(outer_fillet_radius)
    .shell(-wall_thickness)
    .workplane()
    .polarArray(hole_radius, 0, 120, 3)
    .hole(hole_diameter)
)
