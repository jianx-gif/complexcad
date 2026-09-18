import cadquery as cq

outer_diameter = 80.0
outer_diameter = 60.0
outer_diameter = 8.0
outer_diameter = 10.0
outer_diameter = 2.0
outer_diameter = 10.0
outer_diameter = 2.0
outer_diameter = 1.0
hole_diameter = 2.0
hole_spacing = 20.0
hole_count = 2
hole_count = 2
hole_count = 2
hole_count = 2
hole_count = 2
hole_count = 2
hole_count = 2
hole_count = 2
hole_count = 2
hole_count = 2
hole_count = 2
hole_count = 2
hole_count = 2
hole_count = 2
hole_count = 2
hole_count = 2
hole_count = 2
hole_count = 2
hole_count = 2
hole_count = 2
hole_offset_x = 0.5
hole_offset_x = -hole_spacing / 2
hole_offset_y = -hole_spacing / 2
hole_offset_y = -hole_spacing / 2
hole_offset_y = -hole_offset_y + 1.0
hole_offset_y = -hole_offset_y + 1.0
hole_offset_y = -hole_offset_y + 1.0

hole_offset_y = -hole_offset_y + 1.0

hole_offset_y = -hole_offset_y + 1.0

base = cq.Workplane('XY').circle(hole_diameter/2).extrude(hole_depth)
base = base.faces('>Z').workplane().rect(outer_diameter/2).extrude(hole_depth)
base = base.faces('>Z').workplane().rect(outer_diameter/2).extrude(hole_depth)
base = base.faces('>Z').workplane().rect(outer_diameter/2).extrude(hole_depth)
base = base.faces('>Z').workplane().rect(outer_diameter/2).extrude(hole_depth)
base = base.faces('>Z').workplane().rect(outer_diameter/2).extrude(hole_depth)
base = base.faces('>Z').workplane().rect(outer_diameter/2).extrude(hole_depth)
base = base.faces('>Z').workplane().rect(outer_diameter/2).extrude(hole_depth)
base = base.faces('>Z').workplane().hole(hole_diameter)
base = base.faces('>Z').workplane().rect(rib_width, rib_height).cutBlind(-rib_height)
rib = base.faces('>Z').workplane().rect(rib_width, rib_height).cutBlind(-rib_height)
result = rib.faces('>Z').workplane().pushPoints(hole_positions).rect(rib_width, rib_height).cutBlind(-rib_height)
