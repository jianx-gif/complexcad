import cadquery as cq

# Parameters
bracket_length = 80.0
rect_width = 50.0
rect_height = 30.0
rect_hole_diameter = 12.0
circle_diameter = 40.0
circle_hole_diameter = 8.0
fillet_radius = 2.0
pad_diameter = 30.0
pad_depth = 4.0
mount_hole_diameter = 5.0
mount_hole_spacing = 20.0

# Sketches for loft
rect_sketch = (
    cq.Sketch()
    .rect(rect_width, rect_height)
    .circle(rect_hole_diameter / 2.0, mode="s")
)

circle_sketch = (
    cq.Sketch()
    .circle(circle_diameter / 2.0)
    .circle(circle_hole_diameter / 2.0, mode="s")
)

# Loft between rectangular and circular profiles
result = (
    cq.Workplane("XY")
    .placeSketch(rect_sketch, circle_sketch.moved(z=bracket_length))
    .loft()
    .edges()
    .fillet(fillet_radius)
)

# Recessed mounting pad on rectangular end (bottom face)
result = (
    result
    .faces("<Z")
    .workplane()
    .circle(pad_diameter / 2.0)
    .cutBlind(pad_depth)
)

# Add mounting holes within the recessed pad
result = (
    result
    .faces("<Z")
    .workplane()
    .rarray(mount_hole_spacing, 0, 2, 1)
    .hole(mount_hole_diameter, depth=pad_depth + 1.0)
)
