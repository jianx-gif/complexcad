import cadquery as cq
outer_radius = 30.0
wall_thickness = 2.0
inner_radius = outer_radius - wall_thickness
rib_width = 12.0
rib_height = 6.0
rib_thickness = 2.0
rib_spacing = 12.0
rib_count = 4
chamfer_size = 0.5
base = cq.Workplane('XY').circle(outer_radius).extrude(outer_radius)
rib = (cq.Workplane('XY')
        .circle(outer_radius - rib_thickness)
        .extrude(rib_height)
        .translate((0, 0, wall_thickness))
    )
    base = base.union(rib)
rib = (cq.Workplane('XY')
        .circle(inner_radius - rib_thickness)
        .extrude(rib_height)
        .translate((0, 0, wall_thickness))
    )
    rib = rib.translate((inner_radius - rib_thickness/2, 0, wall_thickness))
    rib = rib.translate((inner_radius - rib_thickness/2, 0, wall_thickness))
    rib = rib.translate((inner_radius - rib_thickness/2, 0, wall_thickness))
    rib = rib.translate((inner_radius - rib_thickness/2, 0, wall_thickness))
    rib = rib.translate((inner_radius - rib_thickness/2, 0, wall_thickness))
    rib = rib.translate((inner_radius - rib_thickness/2, 0, wall_thickness))
    rib = rib.translate((inner_radius - rib_thickness/2, 0, wall_thickness))
    rib = rib.translate((inner_radius - rib_thickness/2, 0, wall_thickness))
    rib = rib.translate((inner_radius - rib_thickness/2, 0, wall_thickness))
    rib = rib.translate((inner_radius - rib_thickness/2, 0, wall_thickness))
    rib = rib.translate((inner_radius - rib_thickness/2, 0, wall_thickness))
    rib = rib.translate((inner_radius - rib_thickness/2, 0, 0))
    rib = rib.translate((inner_radius - rib_thickness/2, 0, 0))
    rib = rib.translate((inner_radius - rib_thickness/2, 0, 0))
)
result = base.union(rib)
