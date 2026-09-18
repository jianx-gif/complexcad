import cadquery as cq
import math
beaming_outer_radius = 20.0
beaming_inner_radius = 10.0
beaming_height = 30.0
flange_radius = 25.0
flange_height = 5.0
base_thickness = 2.0
central_hole_diameter = 8.0
set_screw_diameter = 4.0
set_screw_countersink_diameter = 8.0
set_screw_depth = 4.0
set_screw_offset = 15.0
pocket_depth = 2.0
pocket_margin = 5.0
pocket_margin = 5.0
profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(0, beaming_height)
    .lineTo(0, beaming_height)
    .lineTo(flange_radius, beaming_height)
    .lineTo(flange_radius, beaming_height + flange_height)
    .lineTo(0, beaming_height + flange_height)
    .close()
)
solid = profile.revolve()
solid = solid.edges().fillet(fillet_radius)
solid = solid.faces(">Z").workplane().hole(central_hole_diameter)
solid = solid.faces(">Z").workplane().polarArray(radius=flange_radius - set_screw_offset, count=set_screw_count, startAngle=0, angle=360)
solid = solid.faces(">Z").workplane().pushPoints([(-set_screw_diameter/2, 0), (set_screw_diameter/2, 0)])
solid = solid.faces(">Z").workplane().pushPoints([(-set_screw_diameter/2, 0), (set_screw_diameter/2, 0)])
solid = solid.faces(">Z").workplane().pushPoints([(-set_screw_diameter/2, 0), (set_screw_diameter/2, 0)])
solid = solid.faces(">Z").workplane().pushPoints([(-set_screw_diameter/2, 0), (set_screw_diameter/2, 0)])
solid = solid.faces(">Z").workplane().pushPoints([(-set_screw_diameter/2, 0), (set_screw_diameter/2, 0)])
solid = solid.faces("<Z").workplane().pushPoints([(-set_screw_diameter/2, 0), (set_screw_diameter/2, 0)])
solid = solid.faces(">Z").workplane().pushPoints([(-set_screw_diameter/2, 0), (set_screw_diameter/2, 0)])
solid = solid.faces("<Z").workplane().pushPoints([(-set_screw_diameter/2, 0), (set_screw_diameter/2, 0)])
solid = solid.faces("<Z").workplane().pushPoints([(-set_screw_diameter/2, 0), (set_screw_diameter/2, 0)])
solid = solid.faces("<Z").workplane().pushPoints([(-set_screw_diameter/2, 0), (set_screw_diameter/2, 0)])
solid = solid.faces("<Z").workplane().pushPoints([(-set_screw_diameter/2, 0), (set_screw_diameter/2, 0)])
solid = solid.faces("<Z").workplane().pushPoints([(-set_screw_diameter/2, 0), (set_screw_diameter/2, 0)])
solid = solid.faces("<Z").workplane().pushPoints([(-set_screw_diameter/2, 0), (set_screw_diameter/2, 0)])
solid = solid.faces("<Z").workplane().pushPoints([(-set_screw_diameter/2, 0), (set_screw_diameter/2, 0)])
solid = solid.faces("<Z").workplane().pushPoints([(-set_screw_diameter/2, 0), (set_screw_diameter/2, 0)])
solid = solid.faces("<Z").workplane().pushPoints([(-set_screw_diameter/2, 0), (set