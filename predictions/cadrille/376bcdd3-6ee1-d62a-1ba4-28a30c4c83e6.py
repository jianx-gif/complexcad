import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-6,0))
r=w0.sketch().segment((-99,-28),(-95,-28)).arc((0,-100),(95,-28)).segment((99,-28)).segment((99,-11)).arc((97,12),(90,34)).segment((90,45)).segment((85,45)).arc((0,100),(-85,45)).segment((-90,45)).segment((-90,34)).arc((-95,12),(-97,-11)).segment((-99,-11)).close().assemble().circle(76,mode='s').finalize().extrude(12)