import cadquery as cq
bracket_width = 60.0
bracket_height = 30.0
bracket_thickness = 8.0
notch_width = 12.0
notch_height = 15.0
notch_depth = 4.0
hole_diameter = 5.0
countersink_diameter = 8.0
countersink_angle = 90.0
fillet_radius = 0.8
chamfer_dist = 0.5
base = (
    cq.Workplane("XY")
    .rect(bracket_width, bracket_height)
    .extrude(bracket_thickness)
)
base = (
    base.faces(">Z").workplane()
    .rect(notch_width, notch_height)
    .cutBlind(bracket_thickness)
)
base = (
    base.faces(">Z").workplane()
    .rect(notch_width, notch_height)
    .cutBlind(bracket_thickness)
)
base = (
    base.faces(">Z").workplane()
    .rect(notch_width, notch_height)
    .cutBlind(bracket_thickness)
)
base = (
    base.faces(">Z").workplane()
    .polarArray(radius=hole_diameter/2, count=4, startAngle=0, angle=360)
    .cskHole(hole_diameter, countersink_diameter, countersink_angle, depth=bracket_thickness)
)
base = (
    base.faces(">Z").workplane()
    .pushPoints([(-bracket_width/2 + hole_diameter/2, 0), (bracket_width/2 - hole_diameter/2, 0)])
    .cskHole(hole_diameter, countersink_diameter, countersink_angle, depth=bracket_thickness)
)
result = base
