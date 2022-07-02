from numpy.random import randint
from numpy.random import rand
import pickle
from datasets import DATASET
from features_extraction_1 import extract_features
from util_1 import all_vsm_similarity_i


# objective function
def objective(bits):
	br_text = ""
	for i in range(n_bits):
		if bits[i] == 1:
			br_text += br_words[i]
	br_text = [br_text]

	all_similarities_i = all_vsm_similarity_i(br_text, src_texts)

	features = extract_features(br, java_src_dict, all_similarities_i)
	features = sorted(features, key=lambda x: x[-2], reverse=True)

	rank_1 = 1
	for feature in features:
		if feature[-1] == 1:
			break
		else:
			rank_1 += 1
	return rank_1



# tournament selection
def selection(pop, scores, k=3):
    # first random selection
    selection_ix = randint(len(pop))
    for ix in randint(0, len(pop), k - 1):
        # check if better (e.g. perform a tournament)
        if scores[ix] < scores[selection_ix]:
            selection_ix = ix
    return pop[selection_ix]


# crossover two parents to create two children
def crossover(p1, p2, r_cross):
	# children are copies of parents by default
	c1, c2 = p1.copy(), p2.copy()
	# check for recombination
	if rand() < r_cross:
		# select crossover point that is not on the end of the string
		pt = randint(1, len(p1)-2)
		# perform crossover
		c1 = p1[:pt] + p2[pt:]
		c2 = p2[:pt] + p1[pt:]
	return [c1, c2]


# mutation operator
def mutation(bitstring, r_mut):
    copy_bitstring = bitstring.copy()

    while True:
        for i in range(len(bitstring)):
            # check for a mutation
            if rand() < r_mut:
                # flip the bit
                copy_bitstring[i] = 1 - copy_bitstring[i]
        if any(copy_bitstring) != 0:
            bitstring = copy_bitstring
            break


# genetic algorithm
def genetic_algorithm(objective, n_bits, n_iter, n_pop, r_cross, r_mut):
	# initial population of random bitstring
	init_gen = [1] * n_bits
	pop = [randint(0, 2, n_bits).tolist() for _ in range(n_pop - 1)]
	pop.append(init_gen)
	# keep track of best solution
	best, best_eval = pop[-1], objective(pop[-1])
	# enumerate generations
	for gen in range(n_iter):
		# evaluate all candidates in the population
		scores = [objective(c) for c in pop]
		# check for new best solution
		for i in range(n_pop):
			if scores[i] < best_eval:
				best, best_eval = pop[i], scores[i]
				print(">%d, new best f(%s) = %.3f" % (gen,  pop[i], scores[i]))
				if best_eval == 1:
					return [best, best_eval]
		# select parents
		selected = [selection(pop, scores) for _ in range(n_pop)]
		# create the next generation
		children = list()
		for i in range(0, n_pop, 2):
			# get selected parents in pairs
			p1, p2 = selected[i], selected[i+1]
			# crossover and mutation
			for c in crossover(p1, p2, r_cross):
				# mutation
				mutation(c, r_mut)
				# store for next generation
				children.append(c)
		# replace population
		pop = children
	return [best, best_eval]


if __name__ == '__main__':
	# Read bug reports
	with open(DATASET.root / 'preprocessed_reports.pickle', 'rb') as file:
		bug_reports = pickle.load(file)

	# Read all java source files
	with open(DATASET.root / 'preprocessed_src.pickle', 'rb') as file:
		java_src_dict = pickle.load(file)

	src_texts = [' '.join(src.file_name['stemmed'] + src.class_names['stemmed']
					+ src.method_names['stemmed']
					+ src.variables['stemmed']
					+ src.pos_tagged_comments['stemmed']
					+ src.attributes['stemmed'])
				for src in java_src_dict.values()]

	br = bug_reports['423257']
	br_words = br.summary['stemmed'] + br.description['stemmed']

	# define the total iterations
	n_iter = 100 # 30000
	# bits
	n_bits = len(br_words)
	# define the population size
	n_pop = 100 #500
	# crossover rate
	r_cross = 0.9
	# mutation rate
	r_mut = 1.0 / float(n_bits)
	# perform the genetic algorithm search
	best, score = genetic_algorithm(objective, n_bits, n_iter, n_pop, r_cross, r_mut)
	print('Done!')
	print('f(%s) = %f' % (best, score))
	#print(objective([1] * n_bits, br_words))