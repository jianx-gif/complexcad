import cadquery as cq

# Parameters
outer_diameter = 40.0
inner_diameter = 20.0
sleeve_length = 70.0
wall_thickness = (outer_diameter - inner_diameter) / 2.0
shoulder_length = 15.0
shoulder_diameter = 30.0
blind_hole_diameter = 6.0
blind_hole_depth = 8.0
blind_hole_rows = 2
blind_hole_cols = 4
blind_hole_spacing = 8.0
chamfer_size = 1.0
tab_thickness = 5.0
tab_width = 20.0
tab_height = 10.0

# Base hollow sleeve via revolve of composite profile
half_profile = (
    cq.Workplane('XZ')
    .moveTo(inner_diameter/2.0, -sleeve_length/2.0)
    .lineTo(inner_diameter/2.0, sleeve_length/2.0)
    .lineTo(outer_diameter/2.0, sleeve_length/2.0)
    .lineTo(outer_diameter/2.0, -sleeve_length/2.0)
    .close()
)

sleeve = half_profile.revolve()

# Chamfer top and bottom edges
sleeve = sleeve.edges("<Z").chamfer(chamfer_size)

# Milled shoulder: cut a reduced‑diameter section at the bottom
shoulder_cut = (
    cq.Workplane('XY')
    .workplane(offset=-sleeve_length/2.0 + shoulder_length/2.0)
    .circle(shoulder_diameter/2.0)
    .extrude(shoulder_length)
)

sleeve = sleeve.cut(shoulder_cut)

# Blind hole pattern on top face (axial, not through)
points = []
for i in range(blind_hole_rows):
    for j in range(blind_hole_cols):
        x = -(blind_hole_cols-1)/2.0*blind_hole_spacing + j*blind_hole_spacing
        y = -(blind_hole_rows-1)/2.0*blind_hole_spacing + i*blind_hole_spacing
        points.append((x, y))

sleeve = (
    sleeve
    .faces(">Z")
    .workplane()
    .pushPoints(points)
    .hole(blind_hole_diameter, depth=blind_hole_depth)
)

# Add an external tab for handling
tab = (
    cq.Workplane('YZ')
    .box(tab_thickness, tab_width, tab_height)
    .translate((outer_diameter/2.0 + tab_thickness/2.0, 0, 0))
)

result = sleeve.union(tab)
