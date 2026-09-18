import cadquery as cq

outer_radius = 45
inner_radius = 20
thickness = 10
blind_hole_diameter = 8
blind_hole_depth = 7
outer_chamfer = 2
inner_chamfer = 1
mounting_hole_diameter = 5
mounting_hole_offset = 5
mounting_hole_count = 4
rib_count = 6
rib_width = 3
rib_height = 8
rib_thickness = 2

profile = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius, thickness)
    .lineTo(inner_radius, thickness)
    .close()
)

washer = profile.revolve()

washer = (
    washer
    .edges("<<Z")
    .chamfer(outer_chamfer)
    .faces(">Z")
    .edges()
    .chamfer(inner_chamfer)
)

washer = (
    washer
    .faces(">Z")
    .workplane()
    .hole(blind_hole_diameter, blind_hole_depth)
)

washer = (
    washer
    .faces(">Z")
    .workplane()
    .polarArray(outer_radius - mounting_hole_offset, 0, 360, mounting_hole_count)
    .hole(mounting_hole_diameter)
)

ribs = cq.Workplane("XY")
for i in range(rib_count):
    angle = i * 360 / rib_count
    rib = (
        cq.Workplane("XY")
        .center(inner_radius + rib_height / 2, 0)
        .rect(rib_width, rib_height)
        .extrude(rib_thickness)
        .rotate((0, 0, 0), (0, 0, 1), angle)
    )
    ribs = ribs.union(rib)

result = washer.union(ribs)
