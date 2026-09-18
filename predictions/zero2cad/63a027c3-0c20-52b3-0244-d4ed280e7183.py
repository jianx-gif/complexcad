import cadquery as cq

outer_diameter = 80.0
inner_diameter = 40.0
ring_thickness = 12.0
boss_height = 5.0
boss_diameter = inner_diameter
hole_diameter = 4.5
hole_count = 8
hole_radius = (outer_diameter/2 + inner_diameter/2) / 2
chamfer_size = 0.7
rib_width = 6.0
rib_height = 4.0
rib_count = 4
rib_offset = 2.0

base = (
    cq.Workplane("XY")
    .circle(outer_diameter/2)
    .extrude(ring_thickness)
)

boss = (
    cq.Workplane("XY")
    .circle(boss_diameter/2)
    .extrude(boss_height)
    .translate((0, 0, ring_thickness))
)

result = base.union(boss)

result = (
    result
    .faces(">Z")
    .workplane()
    .polarArray(radius=hole_radius, count=hole_count, startAngle=0, angle=360)
    .hole(hole_diameter)
)

result = result.faces(">Z").edges().chamfer(chamfer_size)

rib = (
    cq.Workplane("XY")
    .rect(rib_width, rib_height)
    .extrude(ring_thickness)
    .translate((inner_diameter/2 + rib_offset + rib_width/2, 0, 0))
)

ribs = rib
for i in range(1, rib_count):
    angle = 360.0 / rib_count * i
    ribs = ribs.union(rib.rotate((0, 0, 0), (0, 0, 1), angle))

result = result.union(ribs)
