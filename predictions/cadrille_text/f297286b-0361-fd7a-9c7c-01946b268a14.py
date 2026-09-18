import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-20,-96))
r=w0.sketch().segment((92,-17),(100,-17)).segment((100,-17)).segment((100,17)).segment((92,17)).close().assemble().finalize().extrude(192)