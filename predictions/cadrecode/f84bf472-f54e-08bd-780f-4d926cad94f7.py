import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-17))
r=w0.sketch().circle(100).push([(73,1)]).circle(11,mode='s').finalize().extrude(9).union(w0.sketch().segment((-63,64),(-57,64)).segment((-57,50)).segment((-26,50)).arc((21,56),(60,24)).segment((55,24)).segment((55,18)).segment((62,18)).arc((60,10),(58,2)).segment((90,0)).arc((34,83),(-63,64)).assemble().finalize().extrude(35))