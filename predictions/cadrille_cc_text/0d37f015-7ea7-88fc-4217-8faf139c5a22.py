import cadquery as cq
body_diameter = 40.0
body_height = 70.0
flange_diameter = 60.0
flange_thickness = 10.0
flange_pocket_diameter = 30.0
flange_pocket_depth = 6.0
mount_hole_diameter = 4.0
mount_hole_radius = 20.0
mount_hole_count = 6
mount_hole_radius = mount_hole_radius + flange_pocket_depth
thread_width = 3.0
thread_depth = 4.0
edge_chamfer = 0.7
body = (
    cq.Workplane("XY")
    .circle(body_diameter / 2)
    .extrude(body_height)
)
flange = (
    cq.Workplane("XY")
    .circle(flange_diameter / 2)
    .extrude(flange_thickness)
)
body = body.union(flange)
body = body.faces(">Z").workplane().hole(1)
body = body.faces(">Z").workplane().hole(mount_hole_diameter)
body = body.faces(">Z").workplane().circle(mount_hole_radius).extrude(mount_hole_radius)
body = body.faces(">Z").workplane().polarArray(radius=mount_hole_radius, count=mount_hole_count, startAngle=0, angle=360).hole(mount_hole_diameter)
body = body.faces(">Z").workplane().polarArray(radius=mount_hole_radius, count=mount_hole_count, startAngle=0, angle=360).hole(mount_hole_diameter)
body = body.faces(">Z").workplane().polarArray(radius=mount_hole_radius, count=mount_hole_count, startAngle=0, angle=360).circle(mount_hole_radius).extrude(mount_hole_radius)
body = body.faces(">Z").workplane().polarArray(radius=mount_hole_radius, count=mount_hole_count, angle=360).hole(mount_hole_diameter)
body = body.faces(">Z").workplane().polarArray(radius=mount_hole_radius, count=mount_hole_count, angle=360).circle(mount_hole_radius).extrude(mount_hole_radius)
body = body.faces("<Z").workplane().polarArray(radius=mount_hole_radius, count=mount_hole_count, angle=360).circle(mount_hole_radius).extrude(mount_hole_radius)
body = body.faces("<Z").workplane().polarArray(radius=mount_hole_radius, count=mount_hole_count, angle=360).hole(mount_hole_diameter)
result = body
