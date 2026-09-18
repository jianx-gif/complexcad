import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-37,0))
w1=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().arc((62,66),(77,52),(90,35)).arc((78,55),(62,66)).assemble().finalize().extrude(13).union(w1.sketch().arc((-56,-45),(0,-60),(56,-45)).segment((56,-23)).arc((0,-51),(-56,-23)).close().assemble().reset().face(w1.sketch().arc((-56,23),(0,51),(56,23)).segment((56,45)).arc((0,60),(-56,45)).close().assemble()).finalize().extrude(-200))