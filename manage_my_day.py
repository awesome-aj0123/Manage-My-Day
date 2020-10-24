import numpy as np
import random
import math
import matplotlib.pyplot as plt

class ScheduleGenerator():

    def __init__(self,
                 event_tuples,
                 event_list,
                 time_slots):

        self.event_tuples = event_tuples
        self.event_list   = event_list
        self.time_slots   = time_slots        

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
        variance_score    = self.calculate_variance_score(schedule)

        fin_score = 0.8*priority_score + 0.5*break_score + 0.8*consistency_score + 0.8*time_period_score + 1*variance_score

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

        diff = i - previous_break_index
        score += -(0.5*diff - 1.5)**2 + 4

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
            #a = math.floor((self.event_list[i]/total_priorities) * 2 * self.time_slots) / 2
            time_event = ()
            for j in self.event_tuples:
                if j[0] == i:
                    time_event = j
                    break

            event_score = -2*(dict_events[i] - time_event[5])**2 + 4
            score += event_score

        return score

    def calculate_variance_score(self, schedule):

        event_names = set()

        for event in schedule:
            if event not in event_names:
                event_names.add(event)

        return len(event_names)

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


class DayManager():

    def genetic_algo(self, event_tuples, start_time, end_time):

        dynamic_events_list = self.gather_dynamic_events(event_tuples)

        # # putting the events and priorities into a dictionary
        # # the event ('break', 1) will automatically be added to the dictionary
        # event_list = {'work': 3, 
        #               'running': 1,  
        #               'tennis': 2, 
        #               'volunteer': 2,
        #               'break': 1}

        total_time_slots = self.calculate_slots(event_tuples, start_time, end_time)
        time_slots       = self.substract_fixed(event_tuples, total_time_slots)

        env = ScheduleGenerator(event_tuples, dynamic_events_list, time_slots)

        num_generations = 100
        num_population  = 300

        avg_score = 0

        original_population = env.randomly_generate_schedules(num_population)

        best_schedule = []
        best_score = 0
        
        for gen in range(num_generations):

            original_population_with_scores = []

            # randomly generates population of schedules for the very beginning

            for schedule in original_population:
                
                # calculate the fitness for each of the schedules
                score = env.fitness_function(schedule)
                avg_score += score

                original_population_with_scores.append((schedule, score))

                if score > best_score:
                    best_schedule = schedule
                    best_score    = score 

            avg_score /= len(original_population)
            avg_score = round(avg_score, 3)

            good_schedules = discard_bad_schedules(original_population_with_scores, avg_score)

            original_population = crossover(original_population_with_scores, time_slots)

        #print(f'Best schedule: {best_schedule}')
        #print(f'Best score: {best_score}')
    
        final_schedule = self.generate_final_schedule(total_time_slots, time_slots, event_tuples, best_schedule, start_time, end_time)

        return final_schedule
        

    def generate_final_schedule(self, total_time_slots, time_slots, event_tuples, best_schedule, start_time, end_time):
        # start_time and end_time are strings

        # get_slot_number

        final_schedule = ['' for i in range(48)]

        for event in event_tuples:
            if event[4] == True: # fixed event
                starting_slot = self.get_slot_number(event[1])
                ending_slot   = self.get_slot_number(event[2])
                for i in range(starting_slot, ending_slot + 1):
                    final_schedule[i] = event[0]

        start_slot_dynamic_events = self.get_slot_number(start_time)
        
        i = 0
        index = start_slot_dynamic_events
        while i < len(best_schedule):
            event = best_schedule[i]

            if final_schedule[index] == '':
                final_schedule[index] = (event, index)
                i+=1
            index+=1

        final_schedule = [x for x in final_schedule if x != '']

        final_schedule_with_times = [(x[0], self.get_time_from_slot(x[1])) for x in final_schedule if type(x) != str]

        final = []

        curr_event = final_schedule_with_times[0][0]
        start_time = final_schedule_with_times[0][1]
        curr_time  = final_schedule_with_times[0][1]

        for i in range(1, len(final_schedule_with_times)):

            event = final_schedule_with_times[i]

            if event[0] != curr_event or self.get_slot_number(curr_time)+1!=self.get_slot_number(event[1]):

                final.append((curr_event, self.get_time_from_slot(self.get_slot_number(start_time)+1), self.get_time_from_slot(self.get_slot_number(curr_time)+2)))
                start_time = event[1]

            curr_time  = event[1]
            curr_event = event[0]

        final.append((curr_event, self.get_time_from_slot(self.get_slot_number(start_time)+1), self.get_time_from_slot(self.get_slot_number(curr_time)+2)))

        return final

    def calculate_slots(self, event_tuples, start_time, end_time):
        # calcualates the number of slots taken given start and end times

        self.event_times = []

        curr_time = self.round_up_time(start_time)

        # first, turn the times into numbers
        hour1    = int(start_time[:2])
        minutes1 = int(start_time[3:])
        hour2    = int(end_time[:2])
        minutes2 = int(end_time[3:]) 
        
        slot_min1 = 0
        if minutes1 > 0 and minutes1 <= 30:
            slot_min1+=1
        elif minutes1 > 30:
            slot_min1+=2

        slot_min2 = 0
        if minutes2 >= 30:
            slot_min2+=1

        slot_start = 2*hour1 + slot_min1
        slot_end   = 2*hour2 + slot_min2

        total = (slot_end - slot_start)

        return total

    def substract_fixed(self, event_tuples, total):
        # substract the times from the fixed events
        for event in event_tuples:
            if event[4] == True:
                # subtract the slots
                total -= self.calculate_event_slots(event[1], event[2])

        # then calculate and return the difference between the numbers
        return total

    def round_up_time(self, start_time):
        hour    = int(start_time[:2])
        minutes = int(start_time[3:])
        if minutes > 30:
            hour += 1
            minutes = 0

        return "{0:0=2d}".format(hour) + ':' + "{0:0=2d}".format(minutes)
 
    def calculate_event_slots(self, start_time, end_time):
        hour1    = int(start_time[:2])
        minutes1 = int(start_time[3:])
        hour2    = int(end_time[:2])
        minutes2 = int(end_time[3:]) 

        slot_min1 = 0
        if minutes1 >= 30:
            slot_min1+=1

        slot_min2 = 0
        if minutes2 > 0 and minutes2 <= 30:
            slot_min2+=1
        elif minutes2 > 30:
            slot_min2+=2

        slot_start = 2*hour1 + slot_min1
        slot_end   = 2*hour2 + slot_min2

        return slot_end - slot_start


    def gather_dynamic_events(self, event_tuples):

        dynamic_events = {}

        for event_des in event_tuples:
            
            if not event_des[len(event_des) - 2]:
                dynamic_events[event_des[0]] = event_des[3]

        dynamic_events['break'] = 1

        return dynamic_events

    def get_slot_number(self, time):
        hour    = int(time[:2])
        minutes = int(time[3:])

        slot_min = 0
        if minutes > 0 and minutes <= 30:
            slot_min+=1
        elif minutes > 30:
            slot_min+=2

        #print(hour*2 + slot_min)
        return hour*2 + slot_min - 1

    def get_time_from_slot(self, slot_number):
        hour   = math.floor(slot_number / 2)
        minute = 30

        if slot_number % 2 == 0:
            minute = 0

        #print("{0:0=2d}".format(hour) + ':' + "{0:0=2d}".format(minute))
        return "{0:0=2d}".format(hour) + ':' + "{0:0=2d}".format(minute)


def get_schedule(event_tuples = [('math class', '10:00', '11:00', 4, True, 0),
                                 ('english class', '15:00', '16:25', 4, True, 0),
                                 ('physics class', '12:00', '13:00', 4, True, 0),
                                 ('play valorant', '', '', 1, False, 0.5),
                                 ('go run', '', '', 3, False, 1),
                                 ('study for midterm', '', '', 3, False, 6)],
                start_time    = '08:00',
                end_time      = '21:00'):

    manager = DayManager()

    event_tuples.append(('break', '', ':', 1, False, 1))

    final_schedule = manager.genetic_algo(event_tuples, start_time, end_time)

    for event in event_tuples:
        if event[4] == True:
            final_schedule.append((event[0], event[1], event[2]))

    return final_schedule

if __name__ == '__main__':

    final_schedule = get_schedule()
    
    for i in final_schedule:
        print(i)
