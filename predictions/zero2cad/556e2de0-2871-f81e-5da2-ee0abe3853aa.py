import cadquery as cq

# Parameters
elbow_center_radius = 30.0
pipe_outer_diameter = 20.0
pipe_wall_thickness = 2.0
chamfer_distance = 1.0
hole_diameter = 4.0
hole_depth = 5.0
hole_spacing = 12.0
boss_width = 12.0
boss_height = 6.0
boss_depth = 8.0

# Derived dimensions
pipe_outer_radius = pipe_outer_diameter / 2.0
pipe_inner_radius = pipe_outer_radius - pipe_wall_thickness

# Path for elbow (quarter circle in XZ plane)
path = (
    cq.Workplane("XZ")
    .moveTo(elbow_center_radius, 0)
    .threePointArc((elbow_center_radius, elbow_center_radius), (0, elbow_center_radius))
    .wire()
)

# Sweep outer profile (circle) along path
outer_profile = cq.Workplane("XY").circle(pipe_outer_radius)
outer_solid = outer_profile.sweep(path, multisection=False)

# Shell to create pipe wall thickness
pipe_elbow = outer_solid.shell(-pipe_wall_thickness)

# Chamfer inlet and outlet edges
pipe_elbow = pipe_elbow.faces("<X").edges().chamfer(chamfer_distance)
pipe_elbow = pipe_elbow.faces(">Z").edges().chamfer(chamfer_distance)

# Add mounting boss on inlet face
pipe_elbow = (
    pipe_elbow.faces("<X")
    .workplane()
    .rect(boss_width, boss_height)
    .extrude(boss_depth)
)

# Add blind holes on inlet face
pipe_elbow = (
    pipe_elbow.faces("<X")
    .workplane()
    .pushPoints([(-hole_spacing/2, 0), (hole_spacing/2, 0)])
    .hole(hole_diameter, depth=hole_depth)
)

result = pipe_elbow