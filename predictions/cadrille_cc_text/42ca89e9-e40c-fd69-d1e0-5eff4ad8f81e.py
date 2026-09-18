import cadquery as cq
import math
gear_thickness = 20.0
gear_thickness = gear_thickness - gear_thickness
gear_base = gear_thickness / 2.0
gear_base = gear_base.edges().chamfer(gear_base)
gear_with_gear = gear_base
gear_with_hole = gear_with_gear.faces(">Z").workplane().hole(keyway_width)
gear_with_hole = gear_with_hole.faces(">Z").workplane().circle(gear_with_hole).cutBlind(gear_thickness)
gear_with_hole = gear_with_hole.faces(">Z").workplane().circle(gear_with_hole).cutBlind(gear_thickness)
gear_with_cavity = gear_with_hole.faces(">Z").workplane().polarArray(radius=gear_with_hole, count=5, startAngle=0, angle=360).hole(gear_with_hole)
gear_with_cavity = gear_with_hole.faces(">Z").workplane().polarArray(radius=gear_with_hole, count=5, startAngle=0, angle=360).circle(gear_with_hole).cutBlind(gear_thickness)
gear_with_gear = gear_with_cavity.cut(gear_with_cavity)
gear_with_gear = gear_with_gear.faces(">Z").edges().chamfer(gear_base)
gear_with_gear = gear_with_gear.faces(">Z").edges().chamfer(gear_base)
result = gear_with_gear
