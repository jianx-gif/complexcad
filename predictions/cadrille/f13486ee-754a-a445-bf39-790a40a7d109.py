import cadquery as cq
w0=cq.Workplane('YZ',origin=(49,0,0))
w1=cq.Workplane('XY',origin=(0,0,-3))
r=w0.sketch().segment((-41,-6),(-27,-31)).segment((-1,-16)).segment((-1,38)).close().assemble().finalize().extrude(-149).union(w0.sketch().segment((-88,-54),(3,-88)).segment((21,-48)).arc((68,-23),(88,26)).segment((46,26)).segment((46,-22)).segment((37,-22)).arc((-19,-45),(-75,-44)).close().assemble().finalize().extrude(-107)).union(w1.sketch().arc((-77,15),(-11,45),(58,26)).arc((75,10),(79,-13)).arc((88,-28),(93,-45)).arc((37,62),(-77,15)).assemble().finalize().extrude(60))