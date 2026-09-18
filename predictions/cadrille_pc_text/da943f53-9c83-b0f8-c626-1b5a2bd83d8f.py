import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,37))
w1=cq.Workplane('XY',origin=(0,0,51))
r=w0.sketch().segment((-97,-28),(-89,-28)).arc((0,-99),(89,-28)).segment((97,-28)).segment((97,-11)).arc((100,0),(97,11)).segment((97,28)).segment((89,28)).arc((0,99),(-89,28)).segment((-97,28)).segment((-97,11)).arc((-100,0),(-97,-11)).close().assemble().finalize().extrude(-10).union(w1.sketch().circle(49).push([(36,-1)]).circle(3,mode='s').finalize().extrude(-102))