import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,0))
r=w0.sketch().push([(-15.5,0)]).rect(169,86).push([(-72,15)]).rect(20,22,mode='s').push([(0,0)]).circle(30,mode='s').finalize().extrude(-22).union(w0.sketch().segment((43,-15),(100,-15)).segment((100,13)).segment((43,13)).arc((44,0),(43,-15)).assemble().finalize().extrude(22))