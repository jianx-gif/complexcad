import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-50,-36))
r=w0.sketch().segment((26,-58),(31,-58)).segment((31,-47)).arc((92,0),(31,47)).segment((31,58)).segment((26,58)).segment((26,47)).arc((-25,0),(26,-47)).close().assemble().finalize().extrude(-30).union(w0.sketch().segment((96,-8),(100,-8)).segment((100,-4)).arc((98,-6),(96,-8)).assemble().finalize().extrude(116))