import random
from visualization import COLOR_VISITED_POINT_IDS, Matrix,COLOR_VISITED_POINT,COLOR_FINISHED_POINT
from environment import BLOCKED,VISITED,np



class SearchAlgorithm:
    
    def __init__(self,graph,visual) -> None:
        self.moveset = [self.right,self.down,self.left,self.up]
        random.shuffle(self.moveset)
        self.visited = np.copy(graph)
        self.original_graph = graph
        self.frontier = []
        self.visual = Matrix(visual.leftmost_pos)
        self.visual.size = visual.size
        self.allpaths = {}

    #Breath First Search
    def find_BFS(self,start_point : tuple,goal_point : tuple):
        '''
        Breath First Search
        '''

        start = (start_point[1],start_point[0])
        goal = (goal_point[1],goal_point[0])

        if not (self.isvalid_move(start) and self.isvalid_move(goal)):  
            raise Exception("Invalid start or goal point")
        
        if (start == goal):
            return [start]

        self.visited[start] = VISITED
        self.frontier = []
        self.frontier.append((start,(-1,-1)))           
        expanded_cost = 0

        while self.frontier:
            current_move = self.frontier.pop(0)
            self.allpaths[current_move[0]] = current_move[1]
            expanded_cost += 1
            if current_move[0] != start:
                self.visual.draw_square((current_move[0][1],current_move[0][0]),COLOR_VISITED_POINT)
            if current_move[0] == goal:
                self.visual.draw_square((current_move[0][1],current_move[0][0]),COLOR_FINISHED_POINT)
                break

            for movefrom in self.moveset:
                posible_move = movefrom(current_move)
                if self.isvalid_move(posible_move[0]):
                    self.visited[posible_move[0]] = VISITED
                    self.frontier.append(posible_move)
            random.shuffle(self.moveset)
                    
        path = goal
        result = []
        result.append(path)
        cost = -1
        while self.allpaths:
            path = self.allpaths[path]
            cost += 1
            if path[0] == -1:
                break
            result.append(path)
            
        return result,cost,expanded_cost

    #Uniform Cost Search
    def find_UCS(self,start_point : tuple,goal_point : tuple):
        '''
        Uniform Cost Search
        '''

        start = (start_point[1],start_point[0])
        goal = (goal_point[1],goal_point[0])
        if not (self.isvalid_move(start) and self.isvalid_move(goal)):  
            raise Exception("Invalid start or goal point")

        if (start == goal):
            return [start]

        self.visited[start] = VISITED
        self.frontier = {}
        self.frontier[start] = (0,(-1,-1))
        expanded_cost = 0

        while self.frontier:
            
            current_move = min(self.frontier, key=self.frontier.get)
            self.visited[current_move] = VISITED
            expanded_cost += 1
            if current_move != start:
                self.visual.draw_square((current_move[1],current_move[0]),COLOR_VISITED_POINT)
            self.allpaths[current_move] = self.frontier[current_move]
            
            if current_move == goal:
                self.visual.draw_square((current_move[1],current_move[0]),COLOR_FINISHED_POINT)
                break

            for movefrom in self.moveset:
                cost = 1    
                posible_move_newmove,posible_move_oldmove = movefrom((current_move,self.frontier[current_move][1]))  
                posible_move = (self.frontier[current_move][0] + cost,posible_move_newmove,posible_move_oldmove)  
                if self.isvalid_move(posible_move[1]):
                    if not posible_move[1] in self.frontier:
                        self.frontier[posible_move[1]] = (posible_move[0],posible_move[2])
                    elif posible_move[0] < self.frontier[posible_move[1]][0]:
                        self.frontier[posible_move[1]] = (posible_move[0],posible_move[2])
            self.frontier.pop(current_move)
            random.shuffle(self.moveset)

        path = goal
        result = []
        result.append(path)
        path_cost = self.allpaths[path][0]
        while self.allpaths:
            path = self.allpaths[path][1]
            if path[0] == -1:
                break
            result.append(path)

        return result,path_cost,expanded_cost
    
    def find_IDS(self,start_point,goal_point,visualize = True):
        '''
        Iterative Deepening Search
        '''
        self.list_color = [COLOR_VISITED_POINT,COLOR_VISITED_POINT_IDS]
        self.INDEX = False


        start = (start_point[1],start_point[0])
        goal = (goal_point[1],goal_point[0])
        if not (self.isvalid_move(start) and self.isvalid_move(goal)):  
            raise Exception("Invalid start or goal point")

        if (start == goal):
            return [start]

        expanded_cost = 0
        depth = 1
        MAX_DEPTH = self.visited.shape[0]*self.visited.shape[1]
        self.frontier = []

        while depth <= MAX_DEPTH:
            finish,expanded_cost = self.DLS(start,goal,depth,visualize)
            if finish: break
            self.visited = np.copy(self.original_graph)
            self.allpaths.clear()
            self.frontier.clear()
            depth *= 2
            self.visual.pen.clear()
            expanded_cost = 0

        path = goal
        result = []
        cost = -1
        result.append(path)
        while self.allpaths:
            path = self.allpaths[path]
            cost += 1
            if path[0] == -1:
                break
            result.append(path)
            
        return result,cost,expanded_cost
        

    def DLS(self,start,goal,limit_depth,visualize):
        
        self.frontier.append((start,(-1,-1)))           

        depth = -1
        reached = False
        success = False
        expanded_cost = 0
        previous_point = [self.frontier[0][1],(-2,-2)]

        while self.frontier:
            current_move = self.frontier.pop()
            if current_move[1] == previous_point[0]:
                depth += 1
                previous_point[0] = current_move[0]
                previous_point[1] = current_move[1]
            elif current_move[1] == previous_point[1]:
                pass
            else:
                depth -= 1
                previous_point[0] = current_move[0]
                previous_point[1] = current_move[1]

            self.allpaths[current_move[0]] = current_move[1]
            self.visited[current_move[0]] = VISITED
            expanded_cost += 1
            if current_move[0] == goal:
                self.visual.draw_square((current_move[0][1],current_move[0][0]),COLOR_FINISHED_POINT)
                success = True
                break
            if visualize and current_move[0] != start:
                self.visual.draw_square((current_move[0][1],current_move[0][0]),self.list_color[self.INDEX])
            
            for movefrom in self.moveset:
                posible_move = movefrom(current_move)
                if self.isvalid_move(posible_move[0]) and depth < limit_depth:
                    self.frontier.append(posible_move)
        
        return success,expanded_cost

    def find_GBFS(self,start_point,goal_point):
        '''
        Greedy Best First Search
        '''
        start = (start_point[1],start_point[0])
        goal = (goal_point[1],goal_point[0])
        reached = False
        if not (self.isvalid_move(start) and self.isvalid_move(goal)):  
            raise Exception("Invalid start or goal point")
        
        if (start == goal):
            return [start]


        self.visited[start] = VISITED
        self.frontier = []
        self.frontier.append((start,(-1,-1))) 
        expanded_cost = 0
        reached = False

        while self.frontier:
            self.frontier.sort(key= lambda move: self.heuristic(move[0],goal))
            current_move = self.frontier.pop(0)
            
            self.allpaths[current_move[0]] = current_move[1]
            if current_move[0] == goal:
                self.visual.draw_square((current_move[0][1],current_move[0][0]),COLOR_FINISHED_POINT)
                break
            self.visited[current_move[0]] = VISITED
            expanded_cost += 1
            if current_move[0] != start:
                self.visual.draw_square((current_move[0][1],current_move[0][0]),COLOR_VISITED_POINT)


            #self.frontier.clear()
            for movefrom in self.moveset:
                posible_move = movefrom(current_move)
                if self.isvalid_move(posible_move[0]):
                    self.frontier.append(posible_move)
            
            random.shuffle(self.moveset)
        path = goal
        result = []
        cost = -1
        result.append(path)
        while self.allpaths:
            path = self.allpaths[path]
            cost += 1
            if path[0] == -1:
                break
            result.append(path)
            
        return result,cost,expanded_cost

    #A* Search
    def find_ASS(self,start_point,goal_point):
        '''
        A* Search
        '''

        start = (start_point[1],start_point[0])
        goal = (goal_point[1],goal_point[0])
        reached = False
        if not (self.isvalid_move(start) and self.isvalid_move(goal)):  
            raise Exception("Invalid start or goal point")
        
        if (start == goal):
            return [start]

        self.visited[start] = VISITED
        self.frontier = {}
        self.frontier[start] = (0,(-1,-1))
        expanded_cost = 0

        while self.frontier:
            current_move = self.bestway(goal)
            self.allpaths[current_move[0]] = current_move[1]
            self.visited[current_move[0]] = VISITED
            expanded_cost += 1
            if current_move[0] != start:
                self.visual.draw_square((current_move[0][1],current_move[0][0]),COLOR_VISITED_POINT)
            
            if current_move[0] == goal:
                self.visual.draw_square((current_move[0][1],current_move[0][0]),COLOR_FINISHED_POINT)
                break
            
            for movefrom in self.moveset:
                cost = 1   
                posible_move_newmove,posible_move_oldmove = movefrom((current_move[0],current_move[1][1]))  
                posible_move = (current_move[1][0] + cost,posible_move_newmove,posible_move_oldmove)
                if self.isvalid_move(posible_move[1]):
                    if not posible_move[1] in self.frontier:
                        self.frontier[posible_move[1]] = (posible_move[0],posible_move[2])
                    else:
                        move_in_frontier = self.frontier[posible_move[1]]
                        f_cost_current = self.f((posible_move[0],posible_move[1]),goal)
                        f_cost_old = self.f((move_in_frontier[0],posible_move[1]),goal)
                        if f_cost_current < f_cost_old:
                            self.frontier[posible_move[1]] = (posible_move[0],posible_move[2])
    
            self.frontier.pop(current_move[0])
            random.shuffle(self.moveset)
                    
        path = goal
        result = []
        result.append(path)
        path_cost = self.allpaths[path][0]
        while self.allpaths:
            path = self.allpaths[path][1]
            if path[0] == -1:
                break
            result.append(path)

        return result,path_cost,expanded_cost

    def heuristic(self,point,goal):     
        return abs(point[0] - goal[0]) + abs(point[1] - goal[1])


    def f(self,move : tuple,goal):    
        g = move[0]
        h = self.heuristic(move[1],goal)
        print(g+h)
        return g + h

    def bestway(self,goal):
        result = 0  
        minValue = self.visited.shape[0]*self.visited.shape[1] + 1
        for move in self.frontier:
            f_cost = self.f((self.frontier[move][0],move),goal)
            if f_cost < minValue:
                minValue = f_cost
                result = move
            elif f_cost == minValue:
                if self.heuristic(move,goal) < self.heuristic(result,goal):
                    result = move

        return (result, self.frontier[result])
        


    def right(self,move):
        newpoint = list(move[0])
        newpoint[1] += 1
        newpoint = tuple(newpoint)
        result = (newpoint,move[0])
        return result
        
    def left(self,move):
        newpoint = list(move[0])
        newpoint[1] -= 1
        newpoint = tuple(newpoint)
        result = (newpoint,move[0])
        return result

    def up(self,move):
        newpoint = list(move[0])
        newpoint[0] += 1
        newpoint = tuple(newpoint)
        result = (newpoint,move[0])
        return result

    def down(self,move):
        newpoint = list(move[0])
        newpoint[0] -= 1
        newpoint = tuple(newpoint)
        result = (newpoint,move[0])
        return result

    def isvalid_move(self,point):
        return (0 <= point[0] < self.visited.shape[0]  
            and 0 <= point[1] < self.visited.shape[1]
            and not self.visited[point])              

    def clear(self):
        self.visual.pen.clear()
        self.visited = np.copy(self.original_graph)
        self.frontier.clear()
        self.allpaths.clear()