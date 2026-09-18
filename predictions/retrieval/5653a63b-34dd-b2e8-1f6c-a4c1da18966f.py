import cadquery as cq

outer_radius = 40
inner_radius = 20
height = 60
wall_thickness = outer_radius - inner_radius
hole_diameter = 8
hole_radius = hole_diameter / 2
hole_spacing = 12
hole_offset_y = 10
cutout_radius = 15
cutout_center_y = height / 2
fillet_radius = 2

# base profile
base_profile = (
    cq.Workplane("XY")
    .moveTo(inner_radius, 0)
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius, height)
    .lineTo(inner_radius, height)
    .close()
)

base = base_profile.revolve()

cutout = (
    cq.Workplane("YZ")
    .center((inner_radius + outer_radius) / 2, cutout_center_y)
    .circle(cutout_radius)
    .extrude(wall_thickness)
)

base = base.cut(cutout)

hole_positions = [(hole_offset_y + i * hole_spacing, 0) for i in range(5)]

result = (
    base
    .faces(">X")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
    .edges()
    .fillet(fillet_radius)
)
