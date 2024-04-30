class Private:
    # Fix class to do what I need it to do. Needs to be a helper class

    with open("secret_sauce.csv") as secretFile:
        next(secretFile)
        for line in secretFile:
            line.strip()
            columns = line.split(",")

            token = columns[0]
            ip = columns[1]
