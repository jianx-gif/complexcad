parts = [base]
parts.append(place(fastener("washer", 'M4', 0), axis=(0, 0, 1), point=(0, 0, 68), seat=4.5, flip=False))
parts.append(place(fastener("screw", 'M4-0.7', 8, 0), axis=(0, 0, 1), point=(0, 0, 68), seat=5.4, flip=False))
parts.append(place(fastener("nut", 'M4-0.7', 'M4', 0), axis=(0, 0, 1), point=(0, 0, 68), seat=-6, flip=True))
