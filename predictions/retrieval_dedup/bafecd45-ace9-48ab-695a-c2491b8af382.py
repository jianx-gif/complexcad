import cadquery as cq

# Parameter definitions
length = 80.0
height = 30.0
thickness = 6.0
profile_width = 10.0
profile_height = 6.0
corner_fillet = 2.0
pocket_width = 30.0
pocket_height = 20.0
pocket_depth = thickness - 2.0
hole_dia = 6.0
hole_offset = 10.0
bend_radius = 10.0
rib_width = 4.0
rib_height = 3.0
rib_spacing = 12.0

# Create sweep path with a 90-degree bend
path = (
    cq.Workplane("XY")
    .lineTo(length - bend_radius, 0)
    .radiusArc((length, bend_radius), bend_radius)
    .lineTo(length, height)
    .wire()
)

# Sweep a rectangular profile along the path to form the bracket
bracket = (
    cq.Workplane("YZ")
    .rect(profile_width, profile_height)
    .wire()
    .sweep(path, multisection=False, makeSolid=True)
)

# Fillet interior corners created by the bend (edges roughly parallel to Z)
bracket = bracket.edges("|Z").fillet(corner_fillet)

# Create a central pocket on the top surface
bracket = (
    bracket.faces(">Z")
    .workplane()
    .center(length/2, height/2)
    .rect(pocket_width, pocket_height)
    .cutBlind(-pocket_depth)
)

# Add mounting holes on the horizontal and vertical arms
hole_positions = [
    (hole_offset, profile_width/2),
    (length - hole_offset, height - profile_width/2)
]
bracket = (
    bracket.faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_dia)
)

# Add ribs on the outer vertical face for stiffness
num_ribs = int((height - 2 * bend_radius) / rib_spacing)
for i in range(num_ribs):
    y_pos = bend_radius + rib_spacing * i + rib_spacing/2
    rib = (
        bracket.faces("<X")
        .workplane()
        .center(0, y_pos - height/2)
        .rect(rib_width, rib_height)
        .extrude(thickness)
    )
    bracket = bracket.union(rib)

# Final result
result = bracket