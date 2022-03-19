class Methods:
  
    def backToFront():
        pass

    def zoneRoate():
        pass

    def reversePyramid():
        pass

    def efficientMethods():
        pass

    def optimalStrategy(num, plane, views):

        passengers = []

        # Group 1: Board all of the even rows on the left side
        # Group 2: Board all of the even rows on the right side
        # Group 3: Board all of the odd rows on the left side
        # Group 4: Board all of the odd rows on the right side

        group1 = []
        group2 = []
        group3 = []
        group4 = []


        for j in range(0,3):
            # Board all of the even rows on the left side
            for i in range(plane[0] - 2, -1, -2):
                group1.append([i,j])
                random.shuffle(group1)

        for j in range(0,3):
            # Board all of the even rows on the right side
            for i in range(plane[0] - 2, -1, -2):
                group2.append([i,6-j])
                random.shuffle(group2)


        for j in range(0,3):
            # Board all of the odd rows on the left side
            for i in range(plane[0] - 1, -1, -2):

                if (j == 0 or j == 1) and (i == 0 or i == plane[0] - 1):
                    # Skips places where there are no seats
                    pass
                else:
                    group3.append([i, j])
                    random.shuffle(group3)



        for j in range(0, 3):
            # Board all of the odd rows on the right side
            for i in range(plane[0] - 1, -1, -2):
                if j == 0 and (i == 0 or i == plane[0] - 1):

                    pass
                else:
                    group4.append([i,6 - j])
                    random.shuffle(group4)


        for i in range(len(group1)):
            x = (group1[i][0])
            y = (group1[i][1])
            passengers.append(Passenger(x, y , 'X', views[len(passengers)], len(passengers)))

        for i in range(len(group2)):
            x = (group2[i][0])
            y = (group2[i][1])
            passengers.append(Passenger(x, y , 'X', views[len(passengers)], len(passengers)))

        for i in range(len(group3)):
            x = (group3[i][0])
            y = (group3[i][1])
            passengers.append(Passenger(x, y , 'X', views[len(passengers)], len(passengers)))


        for i in range(len(group4)):
            x = (group4[i][0])
            y = (group4[i][1])
            passengers.append(Passenger(x, y , 'X', views[len(passengers)], len(passengers)))


        return(passengers)

    def randomBoarding(num, plane, views):

      # creates list of (num) passengers
      # (plane) indicates the number of rows and columns
      # for 132 seats, plane = [23, 7]
      # views corresponds to v.passengers

        seating = []

        for i in range(0, plane[0]):
            for j in range(0, plane[1]):
                if((i == 0 or i == plane[0] - 1) and (j == 0 or j == 1 or j == plane[1] - 1)):
                    pass
                elif j != middle:
                    seating.append([i, j])

        passengers = []

        for i in range(0, num):
            index = random.randint(0, len(seating) - 1)
            coord = seating[index]
            passengers.append(Passenger(coord[0], coord[1], 'X', views[i], i))
            seating.remove(coord)

        return passengers

    def steffensOptimalBoarding(num, plane, views):

        passengers = []

        for j in range(0, 3):
            # Loop works outside in
            for i in range(plane[0] - 1, -1, -2):

                # Every other seat starting in back right

                if j == 0 and (i == 0 or i == plane[0] - 1):
                    # Skips places where there are no seats
                    pass
                else:
                    passengers.append(Passenger(i, 6 - j, 'X', views[len(passengers)], len(passengers)))

            for i in range(plane[0] - 1, -1, -2):

                # Every other seat starting in back left

                if (j == 0 or j == 1) and (i == 0 or i == plane[0] - 1):
                    # Skips places where there are no seats
                    pass
                else:
                    passengers.append(Passenger(i, j, 'X', views[len(passengers)], len(passengers)))

            for i in range(plane[0] - 2, -1, -2):

                # Every other seat starting one up from back right

                passengers.append(Passenger(i, 6 - j, 'X', views[len(passengers)], len(passengers)))

            for i in range(plane[0] - 2, -1, -2):

                # Every other seat starting one up from back left

                passengers.append(Passenger(i, j, 'X', views[len(passengers)], len(passengers)))

        return passengers

    def outsideInBoarding(num, plane, views):
        passengers = []

        g = [[], [], []]

        for i in range(0, 3):
            # Creates three groups of seats: rows 0 and 6, rows 1 and 5, and rows 2 and 4
            for j in range(0, plane[0]):

                if (i == 0 or i == 1) and (j == 0 or j == plane[0] - 1):
                    # Does not list places with no seats
                    pass
                else:
                    g[i].append([i, j])

                if i == 0 and (j == 0 or j == plane[0] - 1):
                    # Does not list places with no seats
                    pass
                else:
                    g[i].append([plane[1] - 1 - i, j])

        p = 0

        for i in range(0, 3):
            # Randomly assigns passengers to seats in each group, starting from outside group, working in
            for j in range(0, len(g[i])):
                index = random.randint(0, len(g[i]) - 1)
                coord = g[i][index]
                passengers.append(Passenger(coord[1], coord[0], 'X', views[p], p))
                g[i].remove(coord)
                p += 1

        return passengers
