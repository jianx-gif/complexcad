import cadquery as cq
hex_diameter = 60.0
circle_diameter = 40.0
height = 60.0
result = (cq.Workplane('XY')
          .polygon(6, hex_diameter)
          .workplane(offset=height)
          .circle(circle_diameter/2)
          .loft(combine=True))
