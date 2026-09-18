import cadquery as cq
import math
tube_radius = 40.0
outer_wall_thickness = 5.0
outer_wall_height = 30.0
flat_angle = math.radians(tube_angle)
flat_depth = outer_wall_thickness - 2 * outer_wall_height
rib_thickness = 3.0
rib_height = 12.0
rib_length = outer_wall_thickness - 2 * rib_thickness
mount_hole_diameter = 5.0
mount_hole_spacing = 30.0
fillet_radius = 2.0
base = cq.Workplane('XY').cylinder(tube_radius, outer_wall_thickness)
base = base.edges().fillet(fillet_radius)
base = base.faces('>Z').workplane().hole(mount_hole_diameter)
base = base.faces('>Z').workplane().hole(mount_hole_diameter)
base = base.faces('>Z').workplane().rect(rib_length, rib_thickness).extrude(rib_height)
base = base.faces('>Z').workplane().polarArray(radius=mount_hole_spacing/2, count=4, startAngle=0, angle=360).hole(mount_hole_diameter)
base = base.faces('>Z').workplane().polarArray(radius=mount_hole_spacing/2, startAngle=0, angle=360).hole(mount_hole_diameter)
base = base.faces('>Z').workplane().polarArray(radius=mount_hole_spacing/2, startAngle=0, angle=360).hole(mount_hole_diameter)
base = base.faces('>Z').edges().fillet(fillet_radius)
result = base
