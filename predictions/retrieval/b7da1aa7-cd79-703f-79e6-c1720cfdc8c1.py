import cadquery as cq
result = (cq.Workplane('XY')
    .rect(40,40)
    .workplane(offset=10)
    .ellipse(30,20)
    .loft(combine=True))
