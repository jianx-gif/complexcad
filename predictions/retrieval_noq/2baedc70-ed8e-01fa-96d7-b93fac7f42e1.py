import cadquery as cq
import math
hub_radius = 20
hub_height = 10
central_shaft_diameter = 8
mount_hole_diameter = 3
mount_hole_count = 4
mount_hole_radius = hub_radius - 4
blade_count = 10
blade_outer_radius = 45
blade_radial_length = blade_outer_radius - hub_radius
blade_axial_thickness = 5
blade_z_thickness = hub_height
fillet_radius = 1
overlap = 1
hub = (cq.Workplane('XY')
    .circle(hub_radius)
    .extrude(hub_height)
    .faces('>Z')
    .workplane()
    .hole(central_shaft_diameter)
    .faces('<Z')
    .workplane()
    .rect(30, 10)
    .cutBlind(-2)
)
mount_points = [(mount_hole_radius * math.cos(math.radians(i * 360 / mount_hole_count)),
                 mount_hole_radius * math.sin(math.radians(i * 360 / mount_hole_count)))
                for i in range(mount_hole_count)]
hub = hub.faces('>Z').workplane().pushPoints(mount_points).hole(mount_hole_diameter)
blade = (cq.Workplane('XY')
    .center(hub_radius - overlap/2 + blade_radial_length/2, 0)
    .rect(blade_radial_length, blade_axial_thickness)
    .extrude(blade_z_thickness)
    .edges('|Z')
    .fillet(fillet_radius)
)
assembly = hub
angle_increment = 360 / blade_count
for i in range(blade_count):
    rotation = i * angle_increment
    assembly = assembly.union(blade.rotate((0, 0, 0), (0, 0, 1), rotation))
result = assembly