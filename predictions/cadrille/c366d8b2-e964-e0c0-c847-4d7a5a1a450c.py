import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-18))
r=w0.sketch().segment((-100,-11),(-59,-22)).arc((17,-2),(96,-34)).arc((98,-32),(100,-31)).segment((100,6)).arc((35,32),(-33,28)).segment((-37,28)).segment((-37,26)).arc((-40,26),(-42,25)).segment((-43,26)).segment((-44,24)).arc((-46,23),(-48,23)).segment((-84,5)).close().assemble().finalize().extrude(36)