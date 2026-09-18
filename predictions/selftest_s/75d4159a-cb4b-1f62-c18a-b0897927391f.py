import cadquery as cq

# Parameters
body_width = 80.0  # X dimension
body_height = 40.0  # Z dimension
body_thickness = 12.0  # extrusion along Y
wall_thickness = 2.0
vent_hole_dia = 4.0
vent_rows = 3
vent_cols = 5
vent_spacing_x = 12.0
vent_spacing_y = 12.0
protrusion_radius = 6.0
protrusion_height = 5.0
chamfer_dist = 1.0
# Attachment tab parameters
tab_width = 20.0
tab_height = 6.0
tab_length = 10.0

# Helper to get the solid
def firstSolid(self):
    return self.newObject([self.findSolid()])

cq.Workplane.firstSolid = firstSolid

# Base body
result = (
    cq.Workplane("XZ")
    .rect(body_width, body_height)
    .extrude(body_thickness)
    .faces(">Y")
    .workplane()
    .tag("top_face")
    # Chamfer outer edges for safety
    .firstSolid()
    .edges()
    .chamfer(chamfer_dist)
    # Central protrusion on top
    .workplaneFromTagged("top_face")
    .center(0, 0)
    .circle(protrusion_radius)
    .extrude(protrusion_height)
    # Vent holes pattern on top
    .workplaneFromTagged("top_face")
    .rarray(
        vent_spacing_x,
        vent_spacing_y,
        vent_cols,
        vent_rows,
        center=True,
    )
    .circle(vent_hole_dia / 2)
    .cutBlind(-body_thickness)
    # Attachment tab on back face
    .faces("<Y")
    .workplane()
    .rect(tab_width, tab_length)
    .extrude(tab_height)
)
