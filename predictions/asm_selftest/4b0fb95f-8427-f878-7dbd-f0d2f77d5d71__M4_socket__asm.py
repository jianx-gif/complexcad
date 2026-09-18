parts = [base]
parts.append(place(fastener("washer", 'M6', 0), axis=(0, 0, 1), point=(0, 0, 12), seat=5, flip=False))
parts.append(place(fastener("screw", 'M6-1', 10, 0), axis=(0, 0, 1), point=(0, 0, 12), seat=6.8, flip=False))
parts.append(place(fastener("washer", 'M4', 1), axis=(0, 0, 1), point=(-30, 0, 2.25), seat=2.55, flip=False))
parts.append(place(fastener("screw", 'M4-0.7', 12, 1), axis=(0, 0, 1), point=(-30, 0, 2.25), seat=3.45, flip=False))
parts.append(place(fastener("nut", 'M4-0.7', 'M4', 1), axis=(0, 0, 1), point=(-30, 0, 2.25), seat=-2.75, flip=True))
parts.append(place(fastener("washer", 'M4', 2), axis=(0, 0, 1), point=(30, 0, 2.5), seat=2.5, flip=False))
parts.append(place(fastener("screw", 'M4-0.7', 12, 2), axis=(0, 0, 1), point=(30, 0, 2.5), seat=3.4, flip=False))
parts.append(place(fastener("nut", 'M4-0.7', 'M4', 2), axis=(0, 0, 1), point=(30, 0, 2.5), seat=-2.5, flip=True))
