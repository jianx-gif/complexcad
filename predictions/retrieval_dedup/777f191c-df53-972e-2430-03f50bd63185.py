import cadquery as cq

outer_diameter = 80.0
thickness = 3.0
vent_pat_width = 8.0
vent_pat_height = 2.0
vent_pat_count = 12
vent_radius = outer_diameter / 2 - 15.0
tab_width = 4.0
tab_length = 10.0
tab_overlap = 1.0
tab_thickness = thickness + 0.2
chamfer_size = 0.5
boss_radius = 10.0
boss_height = 2.0
hole_diameter = 4.0
rib_width = 6.0
rib_length = 30.0
rib_thickness = 1.0

base = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2)
    .extrude(thickness)
)

boss = (
    cq.Workplane("XY")
    .circle(boss_radius)
    .extrude(boss_height)
)

boss = boss.faces(">Z").workplane().hole(hole_diameter)

result = base.union(boss)

tab_center = outer_diameter / 2 + tab_length / 2 - tab_overlap

tab = (
    cq.Workplane("XY")
    .center(tab_center, 0)
    .rect(tab_length, tab_width)
    .extrude(tab_thickness)
)

tabs = tab.union(
    tab.rotate((0, 0, 0), (0, 0, 1), 90)
    .union(tab.rotate((0, 0, 0), (0, 0, 1), 180))
    .union(tab.rotate((0, 0, 0), (0, 0, 1), 270))
)

result = result.union(tabs)

vent = (
    cq.Workplane("XY")
    .rect(vent_pat_width, vent_pat_height)
    .polarArray(count=vent_pat_count, radius=vent_radius, startAngle=0, angle=360)
    .extrude(thickness + 0.1)
)

result = result.cut(vent)

rib = (
    result.faces("<Z").workplane()
    .rect(rib_length, rib_width)
    .extrude(-rib_thickness)
)

result = result.union(rib)

result = result.edges("|Z").chamfer(chamfer_size)
