import cadquery as cq

outer_radius = 40.0
wall_thickness = 3.0
cover_height = 10.0
dome_radius = 3.0
fillet_radius = 1.5
mount_hole_dia = 4.0
mount_hole_count = 6
mount_hole_pattern_radius = outer_radius - wall_thickness - 5.0
rib_width = 4.0
rib_length = 20.0
rib_height = 2.0
rib_offset_radius = outer_radius - wall_thickness - 8.0

base = cq.Workplane('XY').circle(outer_radius).extrude(cover_height)
shell = base.shell(-wall_thickness)
inner_radius = outer_radius - wall_thickness

dome_profile = (
    cq.Workplane('XZ')
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, dome_radius)
    .threePointArc((inner_radius + dome_radius, dome_radius), (inner_radius + dome_radius, 0))
    .close()
    .revolve()
)

result = shell.union(dome_profile)
result = result.edges().fillet(fillet_radius)
result = (
    result.faces('>Z')
    .workplane()
    .polarArray(radius=mount_hole_pattern_radius, startAngle=0, angle=360, count=mount_hole_count)
    .hole(mount_hole_dia)
)

rib = (
    cq.Workplane('XY')
    .rect(rib_width, rib_length)
    .extrude(rib_height)
)
result = result.union(
    rib.translate((rib_offset_radius, 0, wall_thickness))
    .union(
        rib.translate((-rib_offset_radius, 0, wall_thickness))
    )
    .union(
        rib.translate((0, rib_offset_radius, wall_thickness))
        .rotate((0,0,0), (0,0,1), 90)
    )
    .union(
        rib.translate((0, -rib_offset_radius, wall_thickness))
        .rotate((0,0,0), (0,0,1), 90)
    )
)
