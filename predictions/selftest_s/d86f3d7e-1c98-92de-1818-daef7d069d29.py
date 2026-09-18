import cadquery as cq

outer_radius = 30
inner_radius = 25
height = 60
shell_thickness = outer_radius - inner_radius
chamfer_dist = 3
ridge_radial_thickness = 2
ridge_height = 6
hole_diameter = 6
hole_offset_radius = (inner_radius + outer_radius) / 2

base = cq.Workplane("XY").circle(outer_radius).extrude(height)
shell = base.shell(-shell_thickness)
shell = shell.faces(">Z").edges().chamfer(chamfer_dist)
ridge_profile = (
    cq.Workplane("XZ")
    .moveTo(outer_radius, height - chamfer_dist - ridge_height)
    .lineTo(outer_radius + ridge_radial_thickness, height - chamfer_dist - ridge_height)
    .lineTo(outer_radius + ridge_radial_thickness, height - chamfer_dist)
    .lineTo(outer_radius, height - chamfer_dist)
    .close()
)
ridge = ridge_profile.revolve()
rib_profile = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, height * 0.2)
    .lineTo(inner_radius + 2, height * 0.2)
    .lineTo(inner_radius + 2, height * 0.8)
    .lineTo(inner_radius, height * 0.8)
    .close()
)
rib = rib_profile.revolve()
shell = (
    shell.faces(">Z").workplane()
    .polarArray(radius=hole_offset_radius, count=4, startAngle=0, angle=360)
    .hole(hole_diameter)
)
result = shell.union(ridge).union(rib)
