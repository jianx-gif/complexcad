import cadquery as cq
import math
gear_width = 10.0
gear_length = 10.0
num_teeth = 30
pitch_diameter = pitch_diameter + 2 * math.sqrt(3)
pitch_radius = pitch_diameter / 2 + 2 * pitch_diameter
gear = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(gear_width, 0)
    .lineTo(gear_width, gear_length)
    .lineTo(0, gear_length)
    .close()
    .revolve()
)
gear = (
    gear
    .faces(">Z")
    .workplane()
    .polarArray(radius=pitch_radius, startAngle=0, count=num_teeth, angle=360)
    .cskHole(
    hole_diameter, depth=gear_length,
    radius=hole_diameter/2,
    count=4,
    count=12,
    startAngle=0,
    radius=hole_diameter/2,
    count=4,
    angle=360,
    hole=Measures(
        radius=hole_diameter/2,
        startAngle=0,
        angle=360,
    )
    )
gear = (
    gear.faces(">Z")
    .workplane()
    .polarArray(radius=pitch_radius, count=num_teeth, startAngle=0, angle=360)
    .cskHole(
    hole=hole_diameter,
    radius=hole_diameter/2,
    radius=hole_diameter/2,
    startAngle=0,
    count=4,
    count=12,
    angle=360,
    hole=Measures(
        radius=hole_diameter/2,
        radius=hole_diameter/2,
    )
    gear = gear.cut(gear)
gear = (
    gear.faces(">Z")
    .workplane()
    .polarArray(radius=hole_diameter/2, count=num_teeth, angle=360)
    .cskHole(
    hole=hole
)
result = gear
