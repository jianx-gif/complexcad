import cadquery as cq
import math
# Parameters
gear_radius = 30.0
gear_thickness = 10.0
num_teeth = 20
tooth_height = 5.0
tooth_width = 4.0
rim_width = 5.0
rib_count = 12
rib_width = 6.0
rib_thickness = 2.0
rib_height = 3.0
bolt_hole_dia = 3.0
bolt_rows = 2
bolt_cols = 3
dx_bolt = 20.0
dy_bolt = 15.0
# Base disc
base = cq.Workplane('XY').circle(gear_radius).extrude(gear_thickness)
# Rim ring (outer cylinder minus inner disc)
rim = (
    cq.Workplane('XY')
    .circle(gear_radius + rim_width)
    .circle(gear_radius)
    .extrude(gear_thickness)
)
# Combine base and rim
body = base.union(rim)
# Teeth
teeth = (
    cq.Workplane('XY')
    .center(gear_radius + tooth_height/2, 0)
    .rect(tooth_width, tooth_height)
    .polarArray(count=num_teeth, radius=gear_radius + tooth_height/2, startAngle=0, angle=360)
    .extrude(gear_thickness)
)
# Ribs on top surface
ribs = (
    body.faces('>Z')
    .workplane()
    .center(gear_radius + rim_width/2, 0)
    .rect(rib_width, rib_thickness)
    .polarArray(count=rib_count, radius=gear_radius + rim_width/2, startAngle=0, angle=360)
    .extrude(rib_height)
)
# Bolt hole pattern on top face
result = (
    body.union(teeth).union(ribs)
    .faces('>Z')
    .workplane()
    .rarray(dx_bolt, dy_bolt, bolt_cols, bolt_rows)
    .hole(bolt_hole_dia)
)
