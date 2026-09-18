import cadquery as cq

arm_length = 80.0
outer_radius = 25.0
shell_thickness = 2.0
pivot_hole_diameter = 6.0
mount_hole_diameter = 4.0
rib_width = 5.0
rib_height = 4.0
chamfer_dist = 0.5

profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius, arm_length * 0.6)
    .threePointArc((outer_radius + 5, arm_length * 0.8), (outer_radius * 0.8, arm_length))
    .threePointArc((outer_radius * 0.5, arm_length + 3), (0, arm_length + 5))
    .close()
)
solid = profile.revolve()

shelled = solid.shell(-shell_thickness)
chamfered = shelled.edges().chamfer(chamfer_dist)

with_pivot = chamfered.faces("<Z").workplane().hole(pivot_hole_diameter)

mount_z_positions = [arm_length * 0.3, arm_length * 0.6, arm_length * 0.9]
mount_holes = (
    cq.Workplane("YZ")
    .transformed(offset=cq.Vector(outer_radius - shell_thickness / 2, 0, 0))
    .pushPoints([(0, z) for z in mount_z_positions])
    .circle(mount_hole_diameter / 2)
    .extrude(shell_thickness * 2 + 5)
)
with_mounts = with_pivot.cut(mount_holes)

rib = (
    cq.Workplane("YZ")
    .transformed(offset=cq.Vector(outer_radius, 0, 0))
    .rect(rib_width, rib_height)
    .extrude(rib_width / 2)
)
result = with_mounts.union(rib)
