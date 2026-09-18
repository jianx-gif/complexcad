import cadquery as cq

# Parameters
outer_diameter = 80.0
wall_thickness = 5.0
sleeve_length = 100.0
bevel_chamfer = 2.0
octagon_side = 5.0
helix_pitch = 12.0
helix_radius = (outer_diameter/2) - wall_thickness - 2.0

# Base sleeve
outer_cyl = cq.Workplane('XY').cylinder(sleeve_length, outer_diameter/2)
inner_cyl = cq.Workplane('XY').cylinder(sleeve_length, (outer_diameter/2) - wall_thickness)
sleeve = outer_cyl.cut(inner_cyl)
# Bevel end
sleeve = sleeve.faces('>Z').edges().chamfer(bevel_chamfer)
# Helix wire
helix_wire = cq.Wire.makeHelix(pitch=helix_pitch, height=sleeve_length, radius=helix_radius)
# Octagonal profile positioned at start radius
profile = cq.Workplane('XY').center(helix_radius, 0).polygon(8, octagon_side)
# Sweep profile along helix to create cutout solid
cut_solid = profile.sweep(helix_wire, multisection=False)
# Apply helical cutouts
result = sleeve.cut(cut_solid)
