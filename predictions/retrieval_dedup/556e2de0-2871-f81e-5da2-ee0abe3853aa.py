import cadquery as cq

pipe_outer_dia = 30.0
wall_thickness = 3.0
elbow_radius = 40.0
rib_length = 15.0
rib_radial = 4.0
chamfer_size = 2.0

outer_radius = pipe_outer_dia / 2.0

path = (
    cq.Workplane("XZ")
    .moveTo(elbow_radius, 0)
    .threePointArc((elbow_radius, elbow_radius), (0, elbow_radius))
)

outer_profile = cq.Workplane("XY").circle(outer_radius)

elbow_solid = outer_profile.sweep(path).shell(-wall_thickness)

rib_profile = cq.Workplane("XY").rect(rib_length, rib_radial)

rib = rib_profile.translate((outer_radius + rib_radial/2.0, 0, 0)).sweep(path)

result = (
    elbow_solid
    .union(rib)
    .faces("<X")
    .edges()
    .chamfer(chamfer_size)
)
