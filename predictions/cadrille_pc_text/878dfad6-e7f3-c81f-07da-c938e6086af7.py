import cadquery as cq
w0=cq.Workplane('YZ',origin=(-100,0,0))
r=w0.sketch().segment((-50,-13),(-13,-13)).arc((-10,-7),(-7,-13)).segment((50,-13)).segment((50,12)).segment((48,12)).segment((48,13)).segment((-48,13)).segment((-48,12)).segment((-50,12)).close().assemble().push([(0,0.5)]).rect(20,25,mode='s').finalize().extrude(200)