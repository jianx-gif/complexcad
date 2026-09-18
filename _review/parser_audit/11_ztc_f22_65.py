import cadquery as cq

outer_radius = 45
cover_height = 20
shell_thickness = 2
boss_radius = 10
boss_height = 12
clearance_hole_diameter = 4
hole_count = 6
hole_center_radius = (outer_radius - shell_thickness) / 2
chamfer_distance = 1
inner_pocket_width = 30
inner_pocket_depth = 2

solid_disc = cq.Workplane('XY').circle(outer_radius).extrude(cover_height)

hollow_cover = solid_disc.shell(shell_thickness)

boss = cq.Workplane('XY').circle(boss_radius).extrude(boss_height)

result = hollow_cover.union(boss)

holes = (
    cq.Workplane('XY')
    .polarArray(hole_center_radius, 0, 360, hole_count)
    .circle(clearance_hole_diameter / 2)
    .extrude(cover_height + 2)
)

result = result.cut(holes)

result = (
    result.faces('>Z')
    .workplane()
    .center(0, 0)
    .rect(inner_pocket_width, inner_pocket_width)
    .cutBlind(-inner_pocket_depth)
)

result = result.edges("|Z").chamfer(chamfer_distance)
