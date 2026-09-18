import cadquery as cq

# Parameters
base_width = 80.0
base_depth = 40.0
base_thickness = 4.0
base_corner_radius = 5.0
rear_bevel = 1.0
clip_thickness = 2.5
clip_height = 30.0
clip_extension = base_depth / 2.0
cradle_radius = 12.0
cradle_depth = clip_thickness / 2.0
mount_hole_diameter = 5.0
mount_hole_spacing = 30.0
mount_hole_row_spacing = 20.0

# Base plate: extrude, fillet vertical edges, rear bevel, tag top face
base = (
    cq.Workplane("XY")
    .rect(base_width, base_depth)
    .extrude(base_thickness)
    .edges("|Z")
    .fillet(base_corner_radius)
    .faces("<Y")
    .edges()
    .chamfer(rear_bevel)
    .tag("top_face")
)

# Add clip extrusion on front face
clip_body = (
    base
    .faces(">Y")
    .workplane()
    .rect(clip_thickness, clip_height)
    .extrude(clip_extension)
)

# Cut rounded cradle and add mounting holes
result = (
    clip_body
    .faces(">Z")
    .workplane()
    .center(0, clip_height / 2.0)
    .circle(cradle_radius)
    .cutBlind(-cradle_depth)
    .workplaneFromTagged("top_face")
    .pushPoints([
        (-mount_hole_spacing/2, -mount_hole_row_spacing/2),
        ( mount_hole_spacing/2, -mount_hole_row_spacing/2),
        (-mount_hole_spacing/2,  mount_hole_row_spacing/2),
        ( mount_hole_spacing/2,  mount_hole_row_spacing/2)
    ])
    .circle(mount_hole_diameter / 2.0)
    .cutThruAll()
)
