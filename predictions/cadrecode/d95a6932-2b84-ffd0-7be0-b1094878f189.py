import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-100))
r=w0.sketch().segment((76,-17),(82,-6)).segment((78,-4)).arc((-81,12),(76,-17)).assemble().push([(-2,0)]).circle(76,mode='s').finalize().extrude(200)