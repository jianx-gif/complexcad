import cadquery as cq
arm_length = 80.0
max_radius = 10.0
grip_length = 30.0
grip_radius = 12.0
cable_hole_diameter = 5.0
cable_hole_offset = 8.0
fillet_radius = 2.0
mount_hole_diameter = 4.0
mount_flange_radius = 20.0
mount_flange_thickness = 5.0
knurl_bump_height = 2.0
knurl_bump_depth = 0.8
knurl_pitch = 2.0
knurl_bump_height = 2.0
knurl_bump = cq.Workplane('XY').circle(max_radius).extrude(arm_length)
base = arm_length/2.0
base = base.faces('>Z').workplane().circle(grip_radius).extrude(grip_length)
base = base.faces('>Z').workplane().circle(cable_hole_diameter/2).extrude(cable_hole_offset)
base = base.faces('>Z').workplane().circle(cable_hole_diameter/2).extrude(cable_hole_offset)
base = base.faces('>Z').workplane().circle(cable_hole_diameter/2).extrude(cable_hole_offset)
base = base.faces('>Z').edges().fillet(fillet_radius)
base = base.faces('>Z').workplane().polarArray(radius=mount_hole_offset, count=arm_hole_spacing, startAngle=0, angle=360).hole(mount_hole_diameter)
base = base.faces('>Z').workplane().circle(mount_hole_diameter/2).extrude(mount_flange_thickness)
base = base.faces('>Z').workplane().polarArray(radius=mount_hole_diameter/2, count=arm_hole_spacing, startAngle=0, angle=360).circle(mount_hole_diameter/2).extrude(mount_flange_thickness)
base = base.union(base)
base = base.faces('>Z').edges().chamfer(cable_hole_offset)
result = base
