import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-100,0))
r=w0.sketch().segment((-75,-62),(-23,-41)).arc((-18,-38),(-12,-37)).segment((75,62)).arc((47,58),(23,41)).segment((-75,-38)).close().assemble().finalize().extrude(200)