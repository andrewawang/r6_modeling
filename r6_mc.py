"""
Rainbow six alpha pack monte carlo simulation

Season pass is broken

Need to streamline simulations
"""

import random
#from decimal import Decimal

class R6_Mc:
    def __init__(self, n_iter = 100, wl = 1, ssn_pass = False, casual = True, seed = None, verbose = False):
        if ssn_pass:
            self.p_weight = 1.003
        else:
            self.p_weight = 1.0
        
        if casual:
            self.win_bonus = 0.02
            self.loss_bonus = 0.015
        else:
            self.win_bonus = 0.035
            self.loss_bonus = 0.025

        self.win_p = wl / (wl + 1.0)
        self.max_iter = n_iter
        random.seed(a = seed)
        self.verbose = verbose

        self.curr_iter = 0
        self.curr_p = 0
        self.n_packs = 0
        self.wins = 0
        self.losses = 0
        self.avg_games = 0
        self.curr_games = 0

    def curr_state(self):
        print()
        print("Current probability: " + str(self.curr_p))
        print("Number of Alpha Packs won: " + str(self.n_packs))
        print("Average number of games til AP: " + str(self.avg_games))
        #print("Games played to AP ratio: " + str(self.curr_iter/ self.n_packs))
        print("Number of simulations: " + str(self.curr_iter) + "/" + str(self.max_iter))
        if (self.losses == 0):
            print("Win/Loss ratio: " + str(self.wins))
        else:
            print("Win/Loss ratio: " + str(self.wins / self.losses))
        print()

        
    def __iter__(self):
        return self

    def __next__(self):
        if self.curr_iter > self.max_iter:
            raise StopIteration
        else:
            #self.curr_p = float(round(Decimal(self.curr_p), 5))
            
            return self.play()

    def play(self):
        self.curr_iter += 1
        self.curr_games += 1
        if random.random() > self.win_p:
            self.curr_p += self.loss_bonus * self.p_weight
            self.losses += 1
            return "Lost match, current probability: " + str(self.curr_p)

        else:
            self.wins += 1
            if self.roll():
                if (self.verbose):
                    print("Alpha pack won at " + str(self.curr_p * 100) + "%")
                self.curr_p = self.win_bonus * self.p_weight
                self.avg_games = (self.n_packs * self.avg_games + self.curr_games) / (self.n_packs + 1)
                self.curr_games = 0
                self.n_packs += 1
                return "Won match, new current number of alpha packs: " + str(self.n_packs)
            else:
                self.curr_p += self.win_bonus * self.p_weight
                return "Won match, no alpha pack, current probability: " + str(self.curr_p)

    def roll(self):
        return random.random() < self.curr_p



simulation = R6_Mc(verbose = True, casual = True, seed = None, ssn_pass = True, n_iter = 1000)
for i in simulation:
    None
simulation.curr_state()



class Single_Mc:
    def __init__(self, start_p = None, wl = 1, ssn_pass = False, casual = True, seed = None, verbose = False):
        if ssn_pass:
            self.p_weight = 1.003
        else:
            self.p_weight = 1.0
        
        if casual:
            self.win_bonus = 0.02
            self.loss_bonus = 0.015
        else:
            self.win_bonus = 0.035
            self.loss_bonus = 0.025

        if start_p == None:
            self.curr_p = self.win_bonus * self.p_weight
        else:
            self.curr_p = start_p
        self.win_p = wl / (wl + 1.0)
        random.seed(a = seed)
        self.verbose = verbose

        self.games_played = 0
    
    def play(self):
        return random.random() < self.win_p

    def roll(self):
        return random.random() < self.curr_p
        
    def run(self):
        while (True):
            self.games_played += 1
            if self.curr_p >= 1.0:
                if self.play():
                    self.curr_p = self.win_bonus * self.p_weight
                else:
                    self.curr_p = self.loss_bonus * self.p_weight
                return self.games_played, 1.0

            else:
                if self.play():
                    if self.roll():
                        temp = self.curr_p
                        self.curr_p = self.win_bonus * self.p_weight
                        return self.games_played, temp
                    else:
                        self.curr_p += self.win_bonus * self.p_weight
                else:
                    self.curr_p += self.loss_bonus * self.p_weight



single_sim = Single_Mc()
print(single_sim.run())
