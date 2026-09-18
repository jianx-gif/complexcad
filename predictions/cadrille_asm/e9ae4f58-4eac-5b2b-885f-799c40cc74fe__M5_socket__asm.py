parts = [base]
parts.append(place(fastener("washer", 'M4', 0), axis=(0, 0, 1), point=(15, 0, 20), seat=2.8, flip=False))
parts.append(place(fastener("screw", 'M4-0.7', 6, 0), axis=(0, 0, 1), point=(15, 0, 20), seat=3.7, flip=False))
parts.append(place(fastener("nut", 'M4-0.7', 'M4', 0), axis=(0, 0, 1), point=(15, 0, 20), seat=-20, flip=True))
