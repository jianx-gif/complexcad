import cadquery as cq
import math
thickness = 10.0
outer_len = 40.0
inner_fillet_radius = 2.0
m8_hole_dia = 4.0
m8_hole_offset_short = 20.0
m8_hole_offset_long = 10.0
lattice_dia = 4.0
lattice_spacing = 15.0
lattice_spacing = 15.0
lattice_offset_y = thickness / 2.0
lattice_offset_y = thickness / 2.0
result = (
    cq.Workplane("XY")
    .box(thickness, thickness, thickness)
    .edges("|Z")
    .fillet(inner_fillet_radius)
    .faces(">Z")
    .workplane()
    .hole(m8_hole_dia)
    .faces(">Z")
    .workplane()
    .hole(m8_hole_dia)
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .hole(m8_hole_dia)
    .edges("|Z")
    .fillet(m8_hole_dia)
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .hole(m8_hole_dia)
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .hole(m8_hole_dia)
    .edges("|Z")
    .fillet(m8_hole_dia)
)
