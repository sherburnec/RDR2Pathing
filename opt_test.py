import mlrose
import numpy as np
import matplotlib.pyplot as plt

def get_contents(file_name):
	key_pair = []
	with open(file_name) as f:
		for l in f:
			key_pair.append(l.strip('\n'))
	key = split_key(key_pair)
	return key

def split_key(key_coords):
	items = [key.split(':')[0] for key in key_coords]
	coords = [tuple(key.split(':')[1].replace(" ", "").split(",")) for key in key_coords]
	coords = [(int(coord[0]), int(coord[1])) for coord in coords ]
	key = dict((items[i], coords[i]) for i in range(0, len(key_coords)))
	return key

key = get_contents("tarot_swords.txt")

problem_no_fit = mlrose.TSPOpt(length = len(key), coords = list(key.values()), maximize=False)
best_state, best_fitness = mlrose.genetic_alg(problem_no_fit, pop_size=450, mutation_prob=0.14, max_attempts=900)

path = [ list(key)[i] for i in best_state]
path_coords =  [key[i] for i in path]
np_path = np.array(path_coords)
x,y = np_path.T

plt.ylim([0,5400])
plt.xlim([0,7200])
plt.scatter(x, y, c=(0,0,0))

for i in range(0, len(key)):
				plt.annotate(path[i],
				path_coords[i],
				textcoords="offset points",
				xytext=(0,10),
				ha='center')

print(path)
print(best_fitness)

plt.show()

