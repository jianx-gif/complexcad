import cadquery as cq

inner_diameter = 30.0
base_outer_diameter = 60.0
step_outer_diameter = 80.0
base_height = 20.0
step_height = 15.0
total_height = base_height + step_height
clearance_hole_diameter = 8.0
chamfer_distance = 1.0
rib_width = 4.0
rib_height = 5.0
rib_count = 4
mounting_hole_diameter = 4.0
mounting_hole_depth = total_height / 2.0

outer_body = (
    cq.Workplane("XY")
    .circle(base_outer_diameter / 2)
    .workplane(offset=base_height)
    .circle(step_outer_diameter / 2)
    .workplane(offset=total_height - base_height)
    .circle(step_outer_diameter / 2)
    .loft()
)

inner_cylinder = cq.Workplane("XY").circle(inner_diameter / 2).extrude(total_height)
result = outer_body.cut(inner_cylinder)

clearance_hole = cq.Workplane("XY").circle(clearance_hole_diameter / 2).extrude(total_height + 2)
result = result.cut(clearance_hole)

result = result.faces(">Z").edges().chamfer(chamfer_distance)

rib_depth = (step_outer_diameter - inner_diameter) / 2 - rib_width / 2
rib = (
    cq.Workplane("XY")
    .workplane(offset=total_height)
    .center(inner_diameter / 2 + rib_width / 2, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_depth, both=False)
)

for i in range(rib_count):
    angle = i * 360.0 / rib_count
    rotated = rib.rotate((0, 0, 0), (0, 0, 1), angle)
    result = result.union(rotated)

mount_holes = (
    cq.Workplane("XY")
    .workplane(offset=total_height / 2)
    .polarArray(count=6, radius=step_outer_diameter / 2 - mounting_hole_diameter, startAngle=0, angle=360)
    .circle(mounting_hole_diameter / 2)
    .extrude(mounting_hole_depth)
)
result = result.cut(mount_holes)
