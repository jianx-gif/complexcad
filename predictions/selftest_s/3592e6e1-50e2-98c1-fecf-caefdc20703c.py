import cadquery as cq

# Parameters
rail_length = 100.0
rail_width = 30.0
base_thickness = 8.0
rib_height = 3.0
rib_width = 12.0
hole_diameter = 2.0
hole_count = 5
hole_spacing = 18.0
edge_chamfer = 0.8
tab_length = 12.0
boss_dia = 8.0
boss_height = 6.0
pocket_width = rail_width / 2.0
pocket_depth = base_thickness / 2.0

# Base plate
base = cq.Workplane('XY').box(rail_length, rail_width, base_thickness)

# Central rib (adds height on top of base)
rib = (cq.Workplane('XY')
       .box(rail_length, rib_width, rib_height)
       .translate((0, 0, base_thickness/2 + rib_height/2)))

# Mounting tab at +X end
tab = (cq.Workplane('XY')
       .box(tab_length, rail_width, base_thickness)
       .translate((rail_length/2 - tab_length/2, 0, 0)))

# Cylindrical boss at -X end (on top of base)
boss = (cq.Workplane('XY')
        .center(-rail_length/2 + boss_dia, 0)
        .circle(boss_dia/2)
        .extrude(boss_height)
        .translate((0, 0, base_thickness/2 + boss_height/2)))

# Assemble main body
part = base.union(rib).union(tab).union(boss)

# Cable pocket cut into the tab (centered in Y)
# pocket cut goes half through thickness
pocket = (cq.Workplane('XY')
          .center(rail_length/2 - tab_length/2, 0)
          .rect(tab_length, pocket_width)
          .extrude(pocket_depth)
          .translate((0, 0, base_thickness/2 - pocket_depth/2)))
part = part.cut(pocket)

# Chamfer top perimeter edges for safety
part = part.faces('>Z').edges().chamfer(edge_chamfer)

# Compute hole positions (symmetric layout)
margin = (rail_length - (hole_count - 1) * hole_spacing) / 2.0
hole_positions = [(-rail_length/2 + margin + i * hole_spacing, 0) for i in range(hole_count)]

# Drill through-holes across full thickness (including rib and boss)
result = (part.faces('>Z')
            .workplane()
            .pushPoints(hole_positions)
            .hole(hole_diameter))