import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-5))
r=w0.sketch().segment((-100,-25),(81,-25)).segment((81,-24)).arc((100,0),(81,24)).segment((81,25)).segment((-100,25)).close().assemble().rect(186,40,mode='s').finalize().extrude(10)