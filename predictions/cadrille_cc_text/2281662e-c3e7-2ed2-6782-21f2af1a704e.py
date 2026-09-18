import cadquery as cq
inner_hole_radius = 15
plate_thickness = 8
outer_chamfer = 2
mounting_hole_diameter = 8
mounting_hole_offset = 30
mounting_hole_radius = inner_hole_radius - mounting_hole_diameter
boss_height = 3
boss_radial_thickness = 5
boss_radial_depth = 0.4
slot_width = 4
slot_length = 12
slot_offset_radius = 22
slot_depth = plate_thickness - 0.5
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_hole_radius, 0)
    .lineTo(inner_hole_radius, plate_thickness)
    .lineTo(outer_chamfer, plate_thickness)
    .lineTo(outer_chamfer, plate_thickness + boss_radial_thickness)
    .lineTo(inner_hole_radius, plate_thickness + boss_radial_thickness)
    .lineTo(inner_hole_radius, 0)
    .close()
)
result = profile.revolve()
result = result.edges().chamfer(outer_chamfer)
boss = (
    cq.Workplane("XY")
    .center(0, 0)
    .circle(boss_radial_thickness + boss_radial_thickness)
    .extrude(boss_height)
)
result = result.union(boss)
result = (
    result.faces(">Z")
    .workplane()
    .polarArray(radius=mounting_hole_offset, count=mounting_hole_diameter/2, startAngle=0, angle=360)
    .hole(mounting_hole_diameter)
)
result = (
    result.faces(">Z")
    .workplane()
    .center(0, 0)
    .circle(mounting_hole_radius)
    .cutBlind(-mounting_hole_depth)
)
result = result.edges().chamfer(outer_chamfer)
