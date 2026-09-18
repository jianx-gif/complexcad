import cadquery as cq

outer_diameter = 80.0
plate_thickness = 4.0
boss_diameter = 30.0
boss_height = 8.0
hole_diameter = 6.0
hole_count = 6
hole_radius = 35.0
fillet_radius = 4.0
tab_width = 10.0
tab_length = 12.0
tab_height = 5.0
rib_width = 6.0
rib_height = 2.0
rib_spacing = 20.0

base = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2)
    .extrude(plate_thickness)
)

boss = (
    cq.Workplane("XY")
    .circle(boss_diameter / 2)
    .extrude(boss_height)
    .translate((0, 0, plate_thickness))
)

result = base.union(boss)

result = (
    result.faces(">Z")
    .workplane()
    .circle(hole_diameter / 2)
    .polarArray(hole_radius, 0, 360, hole_count)
    .cutBlind(-(plate_thickness + boss_height))
)

result = result.faces(">Z").edges().fillet(fillet_radius)

for angle in [0, 90, 180, 270]:
    tab = (
        cq.Workplane("XY")
        .center(outer_diameter / 2 + tab_height / 2, 0)
        .rect(tab_width, tab_length)
        .extrude(tab_height)
        .rotate((0, 0, 0), (0, 0, 1), angle)
    )
    result = result.union(tab)

rib = (
    cq.Workplane("XY")
    .rect(rib_width, rib_spacing)
    .extrude(rib_height)
    .translate((0, 0, plate_thickness / 2))
)

rib_pattern = rib
for angle in [90, 180, 270]:
    rib_pattern = rib_pattern.union(rib.rotate((0, 0, 0), (0, 0, 1), angle))

result = result.union(rib_pattern)
