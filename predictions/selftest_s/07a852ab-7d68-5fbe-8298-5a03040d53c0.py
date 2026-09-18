import cadquery as cq

cover_radius = 40.0
wall_thickness = 5.0
cover_height = 20.0
lip_height = 3.0
lip_thickness = 2.0
vent_radius = 8.0
vent_depth = 4.0
clearance_hole_radius = 2.0
num_clearance_holes = 6
hole_offset_radius = cover_radius - wall_thickness/2
chamfer_distance = 1.0

inner_radius = cover_radius - wall_thickness
lip_outer_radius = inner_radius + lip_thickness

profile = (
    cq.Workplane("XZ")
    .moveTo(cover_radius, 0)
    .lineTo(cover_radius, cover_height - lip_height)
    .lineTo(lip_outer_radius, cover_height - lip_height)
    .lineTo(lip_outer_radius, cover_height)
    .lineTo(inner_radius, cover_height)
    .lineTo(inner_radius, 0)
    .close()
)

solid = profile.revolve()

vent = (
    cq.Workplane("XY")
    .circle(vent_radius)
    .extrude(-vent_depth)
)

solid = solid.cut(vent.translate((0, 0, cover_height / 2)))

cutter = cq.Workplane("XY").box(cover_radius, 200, cover_height).translate((-cover_radius/2, 0, 0))

half1 = solid.intersect(cutter)
half2 = solid.cut(cutter)

half1 = half1.edges("|Z").chamfer(chamfer_distance)
half2 = half2.edges("|Z").chamfer(chamfer_distance)

def add_clearance_holes(part):
    return (
        part.workplane(offset=cover_height / 2)
        .polarArray(radius=hole_offset_radius, startAngle=0, angle=360, count=num_clearance_holes)
        .circle(clearance_hole_radius)
        .cutThruAll()
    )

half1 = add_clearance_holes(half1)
half2 = add_clearance_holes(half2)

result = half1.union(half2)
