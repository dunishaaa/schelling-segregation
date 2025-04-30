import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import math
import random

#np.random.seed(2)
plt.rcParams["legend.loc"] = 'upper right'
plt.style.use('dark_background')

class Agent:

    num_of_agents = 0

    def __init__(self,race,x,y,ID):
        self.race = race
        self.x = x
        self.y = y
        self.ID = ID

    def set_x(self,x):
        self.x = x

    def set_y(self,y):
        self.y = y

        Agent.num_of_agents += 1 



def distance(x,y):
    return math.sqrt(x.item()**2+y.item()**2)

##################### Create agents
       # RELEVANT CONSTANTS
population = 20
proportion = 0.3
k = 8  # Neighbors
Coeff = 0.5     # Minority intolerance
min_dist = 0.02
step = 0.01


agents = list()
for i in range(population):

    if i < population*proportion: 
        agents.append(Agent('white',np.random.rand(1),np.random.rand(1),i))
    else:
        agents.append(Agent('black',np.random.rand(1),np.random.rand(1),i))


X_w = [agent.x for agent in agents if agent.race == 'white']
Y_w = [agent.y for agent in agents if agent.race == 'white']

num_whites = len([agent.race for agent in agents if agent.race == 'white'])
num_blacks = len([agent.race for agent in agents if agent.race == 'black'])

X_b = [agent.x for agent in agents if agent.race == 'black']
Y_b = [agent.y for agent in agents if agent.race == 'black']

##################### Plotting

fig, (ax1,ax2) = plt.subplots(
    ncols=2,
    figsize = (12,10)
)
fig.suptitle('Schelling Segregation Agent Based Model', fontsize=15)
sc1 = ax1.scatter(X_w,Y_w,c='r',marker='.',label=num_whites)
sc2 = ax1.scatter(X_b,Y_b,c='cyan',marker='.', label=num_blacks)
ax1.legend()

labels = ['Avg_Prob_Red_Neighbor_As_Red','Avg_Prob_Blue_Neighbor_As_Blue']

bar = ax2.bar(labels,[proportion,1-proportion],width = 0.3, color=['tab:red','tab:cyan'])
ax2.set_title('Segregation Measure')
ax2.set_yticks(np.arange(0,1.1,0.1))



############################# Animation's Function

def update(frame):

    ##################### Determine the distances between agents

    X = [agent.x for agent in agents]
    Y = [agent.y for agent in agents]

    R = np.zeros((population,population))


    ag_av_segregation_w = []     # Average segregation per agent
    ag_av_segregation_b = []

    for i in range(population):
        for j in range(population):

            R[i,j] = distance(X[i]-X[j],Y[i]-Y[j])




    for i in range(population):

        ind = np.argpartition(R[i,:],k)
        reference_race = [agent.race for agent in agents if agent.ID == ind[0]]
        reference_x = [agent.x for agent in agents if agent.ID == ind[0]]
        reference_y = [agent.y for agent in agents if agent.ID == ind[0]]


        alike_count = 0

        white_alike = 0
        white_unlike = 0
        black_alike = 0
        black_unlike = 0


        ind_alike = []
        
        for j in range(1,k):  # (1,k) To avoid double counting the reference

            actual_race = [agent.race for agent in agents if agent.ID == ind[j]]

            if actual_race != reference_race :
                if actual_race == ['white']:
                    white_unlike += 1
                else:
                    black_unlike +=1
                
            else:
                alike_count +=1
                ind_alike.append(ind[j])

                if actual_race == ['white']:
                    white_alike += 1
                else:
                    black_alike +=1
        
        if white_unlike != 0:      # Counting average neighbor
            ag_av_segregation_w.append(white_alike/white_unlike)
            #ag_av_segregation_b.append(1 - ag_av_segregation_w[i])
        else:
            ag_av_segregation_w.append(1)
             

        if black_unlike != 0:
            ag_av_segregation_b.append(black_alike/black_unlike)
        else:
            ag_av_segregation_b.append(1)

        

        if alike_count / k < Coeff:
            #print('move')

            if ind_alike:
                alike_x = [agent.x for agent in agents if agent.ID == ind_alike[0]]
                alike_y = [agent.y for agent in agents if agent.ID == ind_alike[0]]
                pointer_x = alike_x[0]-reference_x[0]
                pointer_y = alike_y[0]-reference_y[0]
                pointer_ux = pointer_x/distance(pointer_x,pointer_y)
                pointer_uy = pointer_y/distance(pointer_x,pointer_y)

                if distance(pointer_x,pointer_y) > min_dist:
                    [agents[n].set_x((reference_x[0]+pointer_ux*step)) for n in range(population) if agents[n].ID == ind[0]]
                    [agents[n].set_y((reference_y[0]+pointer_uy*step)) for n in range(population) if agents[n].ID == ind[0]]
                
                   
            else:
                alike_x = [agent.x for agent in agents if agent.ID != ind[0] and [agent.race] == reference_race]
                alike_y = [agent.y for agent in agents if agent.ID != ind[0] and [agent.race] == reference_race]
                print(alike_x)

                pointer_x = alike_x[0]-reference_x[0]
                pointer_y = alike_y[0]-reference_y[0]
                pointer_ux = pointer_x/distance(pointer_x,pointer_y)
                pointer_uy = pointer_y/distance(pointer_x,pointer_y)

                if distance(pointer_x,pointer_y) > min_dist:
                    [agents[n].set_x((reference_x[0]+pointer_ux*step)) for n in range(population) if agents[n].ID == ind[0]]
                    [agents[n].set_y((reference_y[0]+pointer_uy*step)) for n in range(population) if agents[n].ID == ind[0]]
                
    # updating data values
        # Scatter
    new_X_w = [agent.x for agent in agents if agent.race == 'white']
    new_Y_w = [agent.y for agent in agents if agent.race == 'white']

    new_X_b = [agent.x for agent in agents if agent.race == 'black']
    new_Y_b = [agent.y for agent in agents if agent.race == 'black']    

    sc1.set_offsets(np.c_[new_X_w,new_Y_w])
    sc2.set_offsets(np.c_[new_X_b,new_Y_b])

    ax1.set_title(f"Affinity_Demand: {Coeff}, Neighbors: {k}, \nFrame: {frame}")

        # Bar
    av_prob_white_neigh = sum(ag_av_segregation_w)/len(ag_av_segregation_w)
    av_prob_black_neigh = sum(ag_av_segregation_b)/len(ag_av_segregation_b)

    y = [av_prob_white_neigh,av_prob_black_neigh]

    for s in range(2):
        
        bar[s].set_height(y[s])

    return sc1, sc2


animation = FuncAnimation(fig, update, frames=350, interval=50, blit=False)
#animation.save(filename="/home/beto/Documents/Python_projects/Schelling_Segregation6.mp4")
print('DONE DONE DONE')
plt.show()






