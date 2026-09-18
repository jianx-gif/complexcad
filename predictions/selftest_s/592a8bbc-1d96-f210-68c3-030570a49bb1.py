import cadquery as cq

outer_diameter = 80
outer_radius = outer_diameter/2
hub_diameter = 30
hub_radius = hub_diameter/2
hub_width = 12
wall_thickness = 4
shaft_diameter = 12
keyway_width = 6
keyway_depth = 5
keyway_length = hub_width*0.8
belt_groove_width = 8
belt_groove_depth = 4
chamfer_size = 1

base_cylinder = cq.Workplane("XY").circle(outer_radius).extrude(hub_width)
shelled = base_cylinder.shell(-wall_thickness)
hub_solid = cq.Workplane("XY").circle(hub_radius + wall_thickness).extrude(hub_width)
part = hub_solid.union(shelled)
part = part.hole(shaft_diameter)
keyway_cut = (
    cq.Workplane()
    .box(keyway_depth, keyway_length, hub_width)
    .translate((shaft_diameter/2 + keyway_depth/2, 0, 0))
)
part = part.cut(keyway_cut)

groove_profile = (
    cq.Workplane("XY")
    .moveTo(outer_radius - belt_groove_depth, -belt_groove_width/2)
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius - belt_groove_depth, belt_groove_width/2)
    .close()
    .revolve()
)
part = part.cut(groove_profile)
part = part.edges("|Z").chamfer(chamfer_size)
result = part
