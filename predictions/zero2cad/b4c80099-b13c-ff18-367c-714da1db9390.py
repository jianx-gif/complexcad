import cadquery as cq

outer_radius = 45.0
inner_radius = 30.0
height = 20.0
wall_thickness = 2.0
rib_height = 5.0
rib_thickness = 1.0
rib_base_z = 12.0
fillet_radius = 2.0
hole_diameter = 4.0
hole_depth = 10.0

profile = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, height)
    .lineTo(outer_radius, height)
    .lineTo(outer_radius, 0)
    .close()
)

solid = profile.revolve()

hollow = solid.shell(-wall_thickness)

rib = (
    cq.Workplane("XY")
    .circle(outer_radius + rib_thickness)
    .extrude(rib_height)
    .translate((0, 0, rib_base_z))
)

combined = hollow.union(rib)

filleted = combined.faces(">Z").edges().fillet(fillet_radius)

result = (
    filleted
    .faces(">Z")
    .workplane()
    .hole(hole_diameter, depth=hole_depth)
)
