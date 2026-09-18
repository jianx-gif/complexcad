import cadquery as cq
outer_radius = 45.0
wall_thickness = 2.0
base_thickness = 5.0
boss_diameter = 20.0
boss_height = 6.0
chamfer = 0.5
mount_hole_diameter = 4.0
mount_hole_spacing = 30.0
base = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(base_thickness)
)
boss = (
    cq.Workplane("XY")
    .circle(boss_diameter / 2)
    .extrude(boss_height)
    .translate((0, 0, base_thickness))
)
result = base.union(boss)
result = (
    result
    .faces(">Z")
    .workplane()
    .hole(mount_hole_diameter)
)
result = (
    result
    .faces(">Z")
    .workplane()
    .hole(mount_hole_diameter)
)
result = (
    result
    .faces(">Z")
    .workplane()
    .polarArray(radius=mount_hole_spacing/2, startAngle=0, angle=360, count=mount_hole_spacing)
    .hole(mount_hole_diameter)
)
result = (
    result
    .faces(">Z")
    .workplane()
    .pushPoints([(-mount_hole_spacing/2, 0), (mount_hole_spacing/2, 0)])
    .hole(mount_hole_diameter)
)
