import cadquery as cq

outer_diameter = 80.0
inner_diameter = 40.0
flange_thickness = 10.0
rib_height = 5.0
rib_width = 8.0
hole_diameter = 4.0
hole_count = 6

outer_radius = outer_diameter / 2.0
inner_radius = inner_diameter / 2.0
hole_radius = (inner_radius + outer_radius) / 2.0

base = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(flange_thickness)
    .faces(">Z")
    .workplane()
    .circle(inner_radius)
    .cutThruAll()
)

rib_profile = (
    cq.Workplane("XZ")
    .moveTo(outer_radius, 0)
    .lineTo(outer_radius, rib_height)
    .threePointArc((outer_radius + rib_width / 2.0, rib_height + rib_width / 2.0), (outer_radius + rib_width, rib_height))
    .lineTo(outer_radius + rib_width, 0)
    .close()
    .revolve(360, (0, 0, 0), (0, 0, 1))
)

flange_with_rib = base.union(rib_profile)

result = (
    flange_with_rib
    .faces(">Z")
    .workplane()
    .polarArray(radius=hole_radius, startAngle=0, count=hole_count, angle=360)
    .hole(hole_diameter)
)
