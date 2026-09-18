import cadquery as cq
outer_diameter = 80.0
hub_height = 60.0
shoulder_diameter = 50.0
shoulder_height = 15.0
shoulder_thickness = 10.0
insert_diameter = 10.0
insert_length = 30.0
outer_chamfer = 2.0
mount_hole_diameter = 6.0
mount_hole_offset = 30.0
base_thickness = 10.0
outer_radius = outer_diameter / 2.0
inner_radius = outer_radius - shoulder_diameter
base = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(hub_height)
)
shoulder = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(hub_height)
)
shoulder = (
    cq.Workplane("XY")
    .circle(outer_radius - shoulder_diameter)
    .extrude(hub_height)
)
shoulder = (
    cq.Workplane("XY")
    .circle(outer_radius - shoulder_diameter)
    .extrude(hub_height)
)
shoulder = (
    shoulder
    .cut(shoulder)
)
result = (
    shoulder
    .cut(shoulder)
    .cut(shoulder)
    .cut(shoulder)
)
result = (
    result
    .cut(shoulder)
    .cut(shoulder)
)
result = (
    result
    .faces(">Z")
    .workplane()
    .polarArray(radius=mount_hole_offset, startAngle=0, angle=360, count=mount_hole_offset)
    .hole(mount_hole_diameter)
)
