import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-26))
r=w0.sketch().segment((-100,-45),(-41,-44)).arc((0,-3),(41,-44)).segment((100,-44)).arc((78,-2),(46,34)).segment((54,40)).segment((46,45)).segment((38,39)).arc((-46,44),(-100,-45)).assemble().push([(-33,14)]).circle(7,mode='s').push([(33,14)]).circle(7,mode='s').finalize().extrude(52)