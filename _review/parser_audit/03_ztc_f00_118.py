import cadquery as cq
from types import SimpleNamespace as NS
import math

p = NS(
    outer_diameter = 80.0,
    central_hole_diameter = 30.0,
    block_height = 20.0,
    sweep_angle = 120.0,
    chamfer_distance = 2.0,
    mounting_hole_diameter = 4.0,
    mounting_hole_offset = 12.0,
    mounting_hole_spacing = 18.0,
    rib_width = 10.0,
    rib_length = 6.0,
    rib_thickness = 2.0
)

p.outer_radius = p.outer_diameter/2.0
p.inner_radius = p.central_hole_diameter/2.0
p.half_height = p.block_height/2.0

sector_profile = (cq.Workplane('XZ')
    .moveTo(p.inner_radius, -p.half_height)
    .lineTo(p.outer_radius, -p.half_height)
    .lineTo(p.outer_radius, p.half_height)
    .lineTo(p.inner_radius, p.half_height)
    .close())

sector = sector_profile.revolve(p.sweep_angle)
sector = sector.edges().chamfer(p.chamfer_distance)
sector = (sector.faces('>Z').workplane()
    .pushPoints([
        (p.mounting_hole_offset, p.mounting_hole_spacing/2),
        (p.mounting_hole_offset, -p.mounting_hole_spacing/2),
        (-p.mounting_hole_offset, p.mounting_hole_spacing/2),
        (-p.mounting_hole_offset, -p.mounting_hole_spacing/2)
    ])
    .hole(p.mounting_hole_diameter))
# pocket rib (cut) on top face
sector = (sector.faces('>Z').workplane()
    .center(0,0)
    .rect(p.rib_width, p.rib_length)
    .cutBlind(p.rib_thickness))

result = sector