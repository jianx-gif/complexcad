import cadquery as cq

corner_radius = 30
pipe_radius = 10
major_radius = corner_radius + pipe_radius
box_size = 200
hole_diameter = 6
hole_spacing = 30
hole_rows = 2
hole_cols = 2
boss_radius = 8
boss_height = 20
boss_fillet = 4

# Create full torus (pipe corner) by revolving an offset circle
torus = (
    cq.Workplane("XY")
    .circle(pipe_radius)
    .center(major_radius, 0)
    .revolve(360)
)

# Box to keep quarter (positive X, Y)
box = (
    cq.Workplane("XY")
    .box(box_size, box_size, box_size)
    .translate((box_size/2, box_size/2, 0))
)
quarter = torus.intersect(box)

# Cylindrical boss at the inner corner with a small fillet on its top edge
boss = (
    cq.Workplane("XY")
    .circle(boss_radius)
    .extrude(boss_height)
    .edges()
    .fillet(boss_fillet)
)
quarter = quarter.union(boss)

# Drill a 2x2 array of through holes on the X-negative face
points = []
for i in range(hole_cols):
    for j in range(hole_rows):
        x = (i - (hole_cols - 1) / 2) * hole_spacing
        y = (j - (hole_rows - 1) / 2) * hole_spacing
        points.append((x, y))
quarter = (
    quarter.faces("<X")
    .workplane(centerOption="CenterOfMass")
    .pushPoints(points)
    .hole(hole_diameter)
)

result = quarter