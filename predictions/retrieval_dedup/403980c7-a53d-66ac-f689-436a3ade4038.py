import cadquery as cq
import math
outer_diameter = 80.0
inner_diameter = 70.0
wall_thickness = 3.0
height = 20.0
chamfer_distance = 1.0
mounting_hole_dia = 5.0
num_holes = 6
hole_pitch_radius = (inner_diameter/2) - wall_thickness - 5.0
outer_radius = outer_diameter/2
solid = (cq.Workplane('XY')
    .circle(outer_radius)
    .extrude(height)
)
shelled = solid.shell(wall_thickness)
# Add a central boss on top
boss_radius = (inner_diameter/2) * 0.4
boss_height = wall_thickness * 2
with_boss = (shelled
    .faces('>Z')
    .workplane(centerOption='CenterOfMass')
    .circle(boss_radius)
    .extrude(boss_height)
)
# Drill mounting holes in a circular pattern on top face
hole_positions = [(hole_pitch_radius*math.cos(math.radians(a)),
                   hole_pitch_radius*math.sin(math.radians(a)))
                  for a in [i*360/num_holes for i in range(num_holes)]]
with_holes = (with_boss
    .faces('>Z')
    .workplane()
    .pushPoints(hole_positions)
    .hole(mounting_hole_dia)
)
# Apply chamfer to top outer edge and boss top edge
result = (with_holes
    .faces('>Z')
    .edges()
    .chamfer(chamfer_distance)
)
