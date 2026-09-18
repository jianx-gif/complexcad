import cadquery as cq
base_length = 80.0
base_width = 50.0
base_thickness = 8.0
inner_cut_diameter = 30.0
boss_diameter = 20.0
boss_height = 12.0
hole_diameter = 4.0
hole_radius_pattern = 22.0
chamfer_size = 1.5
rib_width = 8.0
rib_height = 6.0
rib_spacing = 20.0
base = (
    cq.Workplane("XY")
    .rect(base_length, base_width)
    .extrude(base_thickness)
)
boss = (
    cq.Workplane("XY")
    .center(0, 0)
    .circle(boss_diameter / 2)
    .extrude(boss_height)
)
base = base.union(boss)
boss = (
    cq.Workplane("XY")
    .center(0, 0)
    .circle(boss_diameter / 2)
    .extrude(boss_height)
)
result = base.union(boss)
result = result.edges("|Z").chamfer(chamfer_size)
result = result.faces(">Z").workplane().hole(hole_diameter)
result = result.edges("|Z").chamfer(chamfer_size)
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints([(-hole_radius_pattern / 2, 0), (hole_radius_pattern / 2, 0)])
    .hole(hole_diameter)
)
