import cadquery as cq

outer_radius = 40.0
inner_radius = 20.0
height = 60.0
rim_fillet = 5.0
rib_radial_thickness = 4.0
rib_height = 15.0
through_hole_radius = 10.0
base_chamfer = 1.0
mount_hole_radius = 3.0
mount_offset = 15.0

profile = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius, height)
    .lineTo(inner_radius, height)
    .close()
)

housing = profile.revolve()

housing = housing.faces("<Z").workplane().hole(through_hole_radius * 2)

rib_outer = inner_radius + rib_radial_thickness
rib_inner = inner_radius
rib = (
    cq.Workplane("XY")
    .circle(rib_outer)
    .circle(rib_inner)
    .extrude(rib_height)
    .translate((0, 0, height/2 - rib_height/2))
)

housing = housing.union(rib)

housing = housing.faces(">Z").edges().fillet(rim_fillet)

housing = housing.faces("<Z").edges().chamfer(base_chamfer)

housing = (
    housing.faces(">Z").workplane()
    .pushPoints([(-mount_offset, 0), (mount_offset, 0)])
    .hole(mount_hole_radius * 2)
)

result = housing