import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().segment((-80,-56),(-78,-58)).segment((-78,-60)).segment((76,-60)).segment((76,-56)).segment((80,-56)).segment((80,56)).segment((76,56)).segment((76,60)).segment((-78,60)).segment((-78,56)).segment((-80,56)).close().assemble().rect(150,100,mode='s').finalize().extrude(-200)