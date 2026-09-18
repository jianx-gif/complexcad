import cadquery as cq

# Parameters
outer_diameter = 80.0
outer_radius = outer_diameter / 2.0
base_height = 25.0
step_diameter = 50.0
step_radius = step_diameter / 2.0
step_height = 15.0
central_hole_diameter = 15.0
mount_hole_diameter = 8.0
mount_hole_count = 6
mount_hole_radius = outer_radius - 10.0
chamfer_distance = 2.0
rib_width = 6.0
rib_height = 12.0
rib_thickness = 4.0
rib_count = 4
rib_angle = 360.0 / rib_count

# Base cylinder
base = cq.Workplane("XY").circle(outer_radius).extrude(base_height)
# Step cylinder on top of base
step = cq.Workplane("XY").circle(step_radius).extrude(step_height).translate((0, 0, base_height))
# Combine base and step
result = base.union(step)
# Central through hole
result = result.faces(">Z").workplane().hole(central_hole_diameter)
# Mounting holes pattern on top face
result = (
    result.faces(">Z")
    .workplane()
    .polarArray(mount_hole_radius, 0, 360.0 / mount_hole_count, mount_hole_count)
    .hole(mount_hole_diameter)
)
# Add ribs around outer circumference
for i in range(rib_count):
    angle = i * rib_angle
    rib = (
        cq.Workplane("XY")
        .rect(rib_width, rib_height)
        .extrude(rib_thickness)
        .translate((outer_radius - rib_thickness / 2.0, 0, base_height / 2.0))
        .rotate((0, 0, 0), (0, 0, 1), angle)
    )
    result = result.union(rib)
# Chamfer bottom edge
result = result.faces("<Z").edges().chamfer(chamfer_distance)
