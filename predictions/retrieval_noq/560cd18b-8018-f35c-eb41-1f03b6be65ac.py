import cadquery as cq

base_length = 80
base_width = 60
base_thickness = 6
rib_height = 8
rib_width = 4
rib_spacing = 20
boss_diameter = 20
boss_height = 12
edge_bevel = 2
fillet_radius = 1

# Base plate with beveled outer edges
base = (cq.Workplane('XY')
        .rect(base_length, base_width)
        .extrude(base_thickness)
        .edges('|Z')
        .chamfer(edge_bevel))

# Central boss
boss = (cq.Workplane('XY')
        .circle(boss_diameter/2)
        .extrude(boss_height)
        .translate((0, 0, base_thickness)))

# Stiffening ribs (two ribs symmetrically placed)
rib_profile_length = base_length - 2 * rib_spacing
rib = (cq.Workplane('XY')
       .rect(rib_width, rib_profile_length)
       .extrude(rib_height)
       .translate((0, 0, base_thickness)))

rib1 = rib.translate((0, -rib_spacing, 0))
rib2 = rib.translate((0, rib_spacing, 0))

# Combine features
result = base.union(rib1).union(rib2).union(boss)

# Small fillet on top edges for safety
result = result.edges('>Z').fillet(fillet_radius)
