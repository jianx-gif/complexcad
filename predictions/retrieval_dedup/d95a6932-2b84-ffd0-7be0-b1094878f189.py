import cadquery as cq

outer_diameter = 80.0
part_length = 100.0
wall_thickness = 4.0
inner_radius = outer_diameter/2 - wall_thickness
channel_depth = 6.0
channel_half_width = 12.0
fillet_radius = 2.0
hole_diameter = 5.0
hole_spacing = 30.0
boss_width = 20.0
boss_height = 15.0
boss_thickness = 3.0

outer_cyl = cq.Workplane('XY').cylinder(part_length, outer_diameter/2)
inner_cyl = cq.Workplane('XY').cylinder(part_length, inner_radius)

v_profile = (
    cq.Workplane('XZ', origin=(outer_diameter/2, 0, 0))
    .polyline([
        (0, 0),
        (-channel_depth, channel_half_width),
        (-channel_depth, -channel_half_width),
    ])
    .close()
    .extrude(part_length)
)

base = outer_cyl.cut(inner_cyl).cut(v_profile)

boss = (
    cq.Workplane('XY')
    .rect(boss_width, boss_height)
    .extrude(boss_thickness)
    .translate((outer_diameter/2 + boss_thickness/2, 0, 0))
)

assembled = base.union(boss)

assembled = assembled.edges('>X and |Z').fillet(fillet_radius)

hole_tool = (
    cq.Workplane('YZ', origin=(outer_diameter/2 + boss_thickness/2, 0, 0))
    .rarray(hole_spacing, 0, 2, 1)
    .circle(hole_diameter/2)
    .extrude(part_length)
)

result = assembled.cut(hole_tool)
