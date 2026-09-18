import cadquery as cq
base_length = 70.0
base_width = 45.0
base_thickness = 10.0
gusset_height = 25.0
hole_diameter = 6.0
hole_offset_x = 20.0
hole_offset_y = 12.0
rib_width = 8.0
rib_height = 6.0
rib_spacing = 12.0
gusset_depth = 15.0
base = cq.Workplane('XY').box(base_length, base_width, base_thickness, centered=True)
gusset = (
    cq.Workplane('XY')
    .box(gusset_depth, base_width, base_thickness, centered=True)
    .translate((0, base_width/2 + gusset_height/2, base_thickness/2))
)
base = base.union(gusset)
base = base.faces('>Z').workplane().hole(hole_diameter)
rib = (
    cq.Workplane('XY')
    .box(rib_width, base_width, rib_height, centered=True)
    .translate((0, base_width/2 + gusset_depth/2, base_thickness/2))
)
base = base.union(rib)
base = base.faces('>Z').workplane().hole(hole_diameter)
base = base.faces('>Z').workplane().center(0, 0).hole(hole_diameter)
base = base.faces('>Z').workplane().center(0, 0).hole(hole_diameter)
base = base.faces('>Z').workplane().center(0, 0).hole(hole_diameter)
base = base.faces('>Z').workplane().center(0, 0).hole(hole_diameter)
rib = rib.translate((0, base_width/2 - gusset_depth/2, base_thickness/2))
result = base.union(rib)
