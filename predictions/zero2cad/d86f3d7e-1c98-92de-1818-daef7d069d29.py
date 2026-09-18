import cadquery as cq
import math

outer_radius = 30.0
wall_thickness = 5.0
inner_radius = outer_radius - wall_thickness
height = 60.0
rib_height = 6.0
rib_thickness = 2.0
rib_base_z = height - rib_height - 5.0
chamfer_angle_deg = 30.0
chamfer_distance = wall_thickness * math.tan(math.radians(chamfer_angle_deg))
mount_hole_diameter = 6.0
mount_hole_count = 4
mount_hole_radius = outer_radius - wall_thickness/2

profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius, rib_base_z)
    .lineTo(outer_radius + rib_thickness, rib_base_z)
    .lineTo(outer_radius + rib_thickness, rib_base_z + rib_height)
    .lineTo(outer_radius, rib_base_z + rib_height)
    .lineTo(outer_radius, height)
    .lineTo(0, height)
    .close()
)

solid = profile.revolve()

hollow = solid.shell(-wall_thickness)

chamfered = hollow.faces(">Z").edges().chamfer(chamfer_distance)

result = (
    chamfered
    .faces(">Z")
    .workplane()
    .polarArray(radius=mount_hole_radius, startAngle=0, angle=360, count=mount_hole_count)
    .hole(mount_hole_diameter)
)
