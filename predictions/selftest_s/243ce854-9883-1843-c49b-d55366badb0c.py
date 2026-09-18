import cadquery as cq
hex_outer_diameter=80.0
circle_outer_diameter=60.0
total_height=80.0
base=cq.Workplane('XY').polygon(6, hex_outer_diameter)
profile=base.workplane(offset=total_height).circle(circle_outer_diameter/2)
lofted=profile.loft(combine=True)
result=lofted