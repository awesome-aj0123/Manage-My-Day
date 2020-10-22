import numpy as np
import random
import math
import matplotlib.pyplot as plt

class ScheduleGenerator():

    def __init__(self, 
                 event_list,
                 time_slots):

        self.event_list = event_list
        self.time_slots = time_slots        

    def randomly_generate_schedules(self, population):

        random_population = []

        for schedule in range(population):

            random_events = []

            for i in range(self.time_slots): # adding 10 random activities to the event list (needs to be changed based on what is filled so far)
                random_event = random.choice(list(self.event_list.items()))[0]
                random_events.append(random_event)

            random_population.append(random_events)

        return random_population

    def fitness_function(self, schedule):

        # scoring based on the following factors:
        # 1. Putting high priority tasks first - DONE
        # 2. Putting breaks after long periods of doing stuff - DONE
        # 3. Consistency in tasks - DONE
        # 4. Doing high priority tasks for longer periods of time, but not too long - DONE

        priority_score    = self.calculate_priority_score(schedule)
        break_score       = self.calculate_break_score(schedule)
        consistency_score = round(self.calculate_consistency_score(schedule), 3)
        time_period_score = self.calculate_time_period_score(schedule)

        fin_score = 0.8*priority_score + 1*break_score + 0.5*consistency_score + 0.8*time_period_score

        # FOR TESTING PURPOSES
        # if(fin_score > 20):
        #     print('-----------------')
        #     print(schedule)
        #     print(f'Priority Score => {priority_score}')
        #     print(f'Break Score => {break_score}')
        #     print(f'Consistency Score => {consistency_score}')
        #     print(f'Time Period Score => {time_period_score}')
        #     print('-----------------')


        return max(0, round(fin_score, 3))

    def calculate_priority_score(self, schedule):

        score = 0

        for i in range(len(schedule) - 1):

            curr_priority = self.event_list[schedule[i]]
            next_priority = self.event_list[schedule[i+1]]

            # checks if the current task is of greater priority than the next one
            if curr_priority >= next_priority:
                score+=2
            else:
                score-=2;

        return score

    def calculate_break_score(self, schedule):

        score = 0

        # map the score using the following function: -(x-3)^2 + 4 
        # where x = difference between the previous break and the current one

        previous_break_index = 0

        for i in range(len(schedule)):

            current_event = schedule[i]

            if current_event == 'break':
                diff = i - previous_break_index
                score += -(0.5*diff - 1.5)**2 + 4
                previous_break_index = i

        return score

    def calculate_consistency_score(self, schedule):

        score = 0

        for i in range(len(schedule) - 1):

            if schedule[i] == schedule[i+1] and schedule[i] != 'break':
                score += 2

            elif schedule[i] == schedule[i+1] and schedule[i] == 'break':
                score -= 1

            else:
                score -= 0.3

        return score

    def calculate_time_period_score(self, schedule):

        # does tasks that are of higher priority for longer periods of time
        # uses the following formula to calculate the score:
        #
        # a = floor(priority_level_of_task / total_priorities * 2 * time_slots)/2
        # score += -2(x-a)^2 + 4
        
        # first gets the amount of time for each of the tasks
        dict_events = {}

        for event in self.event_list.keys():
            dict_events[event] = 0 

        for event in schedule:
            dict_events[event] += 0.5

        total_priorities = 0.0
        for i in self.event_list.values():
            total_priorities += i

        score = 0
        for i in dict_events:
            a = math.floor((self.event_list[i]/total_priorities) * 2 * self.time_slots) / 2
            event_score = -2*(dict_events[i] - a)**2 + 4
            score += event_score

        return score

def discard_bad_schedules(original_population, average):
    return [x for x in original_population if(x[1] > average)]

def crossover(population, time_slots):

    total_score   = np.sum([x[1] for x in population])
    probabilities = [x[1]/total_score for x in population]

    new_population = []

    for i in range(len(population)):
        rand_index_1 = np.random.choice(np.arange(0, len(population)), p=probabilities)
        rand_index_2 = np.random.choice(np.arange(0, len(population)), p=probabilities)

        new_schedule = []
        # cross over bewteen two different schedules
        for j in range(time_slots):
            if random.randint(1, 2) == 1:
                new_schedule.append(population[rand_index_1][0][j])
            else:
                new_schedule.append(population[rand_index_2][0][j])

        new_population.append(new_schedule)

    return new_population


if __name__ == '__main__':

    # putting the events and priorities into a dictionary
    # the event ('break', 1) will automatically be added to the dictionary
    event_list = {'work': 5, 
                  'running': 2,  
                  'tennis': 3, 
                  'volunteer': 3,
                  'break': 1}

    time_slots = 20
    env = ScheduleGenerator(event_list, time_slots)

    num_generations = 100
    num_population  = 300

    avg_score = 0

    original_population = env.randomly_generate_schedules(num_population)

    generation_averages = []
    
    for gen in range(num_generations):

        original_population_with_scores = []

        # randomly generates population of schedules for the very beginning

        for schedule in original_population:
            
            # calculate the fitness for each of the schedules
            score = env.fitness_function(schedule)
            avg_score += score

            original_population_with_scores.append((schedule, score))

        avg_score /= len(original_population)
        avg_score = round(avg_score, 3)
        generation_averages.append(avg_score)

        print(original_population[0])
        print(f'Average Score => {avg_score}')

        good_schedules = discard_bad_schedules(original_population_with_scores, avg_score)

        original_population = crossover(original_population_with_scores, time_slots)

    plt.plot(generation_averages)
    plt.show()
