import cadquery as cq

base_width = 60
base_thickness = 8
arm_length = 70
arm_start_width = 30
arm_end_width = 12
arm_height = 12
taper_angle = 10
fillet_radius = 2
chamfer_dist = 1
mount_hole_dia = 5
mount_hole_spacing = 40
rib_thickness = 4
rib_width = 8
rib_height = 6
slot_width = 4
slot_length = 30
groove_width = 20
groove_depth = 4

base = (cq.Workplane("XY")
    .rect(base_width, base_width)
    .extrude(base_thickness)
    .faces(">Z").workplane()
    .pushPoints([(-mount_hole_spacing/2, 0), (mount_hole_spacing/2, 0)])
    .hole(mount_hole_dia)
    .edges("|Z").fillet(fillet_radius)
)

arm = (cq.Workplane("XY")
    .rect(arm_start_width, arm_height)
    .extrude(arm_length, taper=taper_angle)
    .translate((0, 0, base_thickness))
)

combined = base.union(arm)

combined = combined.faces(">Z").edges().chamfer(chamfer_dist)

rib = (cq.Workplane("YZ")
    .center(0, arm_height/2 - rib_height/2)
    .rect(rib_thickness, rib_height)
    .extrude(arm_length)
    .translate((arm_start_width/2 + rib_thickness/2, 0, base_thickness))
)

combined = combined.union(rib)

groove = (cq.Workplane("XY")
    .center(0, 0)
    .rect(groove_width, groove_depth)
    .extrude(groove_depth)
    .translate((0, 0, base_thickness + arm_length - groove_depth))
)

result = combined.cut(groove)
