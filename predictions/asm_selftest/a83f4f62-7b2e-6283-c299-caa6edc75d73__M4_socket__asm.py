parts = [base]
parts.append(place(fastener("screw", 'M4-0.7', 40, 0), axis=(0, -1, 0), point=(-15, -18.5, 25), seat=-31.5, flip=True))
parts.append(place(fastener("nut", 'M4-0.7', 'M4', 0), axis=(0, -1, 0), point=(-15, -18.5, 25), seat=1.5, flip=False))
parts.append(place(fastener("screw", 'M4-0.7', 40, 1), axis=(0, -1, 0), point=(-5, -18.5, 25), seat=-31.5, flip=True))
parts.append(place(fastener("nut", 'M4-0.7', 'M4', 1), axis=(0, -1, 0), point=(-5, -18.5, 25), seat=1.5, flip=False))
parts.append(place(fastener("screw", 'M4-0.7', 40, 2), axis=(0, -1, 0), point=(5, -18.5, 25), seat=-31.5, flip=True))
parts.append(place(fastener("nut", 'M4-0.7', 'M4', 2), axis=(0, -1, 0), point=(5, -18.5, 25), seat=1.5, flip=False))
parts.append(place(fastener("screw", 'M4-0.7', 40, 3), axis=(0, -1, 0), point=(15, -18.5, 25), seat=-31.5, flip=True))
parts.append(place(fastener("nut", 'M4-0.7', 'M4', 3), axis=(0, -1, 0), point=(15, -18.5, 25), seat=1.5, flip=False))
