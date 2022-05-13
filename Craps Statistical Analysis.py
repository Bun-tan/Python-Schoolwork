# Deitel & Deitel fig04_02.py as starter file, plus observations from 
# AnalyzeCraps.py by Anita Wright

"""
File: CoyneSProject1.py
CSC 272 Spring 2022
Author: Steven C Coyne
Date: 2/25/2022

fig04_02.py as starter file
Program modifications to Deitel's fig04_02.py: 
    Added a loop to run many simulations
    Disabled craps outputs to prevent large output volumes during simulations
    Added lists to track simulated games and their lengths
    Added statistical analysis
    Added graphing functionality

Description: Simulates and visualizes the dice game Craps.

Problem Statement (Deitel exercise 5.33):

In this exercise, you’ll modify Chapter 4’s script that simulates the dice game 
craps by using the techniques you learned in Section 5.17.2. The script should 
receive a command-line argument indicating the number of games of craps to 
execute and use two lists to track the total numbers of games won and lost on 
the first roll, second roll, third roll, etc. Summarize the results as follows:

a) Display a horizontal bar plot indicating how many games are won and how many
are lost on the first roll, second roll, third roll, etc. Since the game could
continue indefinitely, you might track wins and losses through the first dozen
rolls (of a pair of dice), then maintain two counters that keep track of wins 
and losses after 12 rolls—no matter how long the game gets. Create separate 
bars for wins and losses.
   
"""
import random
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statistics

#Number of games from command line argument
game_count = int(sys.argv[1])

#Lists to log win/loss information, one entry per game
games_won = []
games_lost = []

def roll_dice():
    """Roll two dice and return their face values as a tuple."""
    die1 = random.randrange(1, 7)
    die2 = random.randrange(1, 7)
    return (die1, die2)  # pack die face values into a tuple

def display_dice(dice):
    """Display one roll of the two dice."""
    die1, die2 = dice  # unpack the tuple into variables die1 and die2
    print(f'Player rolled {die1} + {die2} = {sum(dice)}')

def play_game():
    """Simulates one game of craps; logs information about wins and losses."""
    die_values = roll_dice()  # first roll

    #display disabled to prevent large output volumes
    #display_dice(die_values) 

    # determine game status and point, based on first roll
    sum_of_dice = sum(die_values)
    roll_counter = 1
    
    if sum_of_dice in (7, 11):  # win
        game_status = 'WON'
        games_won.append(1)
    elif sum_of_dice in (2, 3, 12):  # lose
        game_status = 'LOST'
        games_lost.append(1)
    else:  # remember point
        game_status = 'CONTINUE'
        my_point = sum_of_dice
        #display disabled to prevent large output volumes
        #print('Point is', my_point)

    # continue rolling until player wins or loses
    while game_status == 'CONTINUE':
        roll_counter += 1
        die_values = roll_dice()
        #display disabled to prevent large output volumes
        #display_dice(die_values)
        sum_of_dice = sum(die_values)

        if sum_of_dice == my_point:  # win by making point
            game_status = 'WON'
            games_won.append(roll_counter)
        elif sum_of_dice == 7:  # lose by rolling 7
            game_status = 'LOST'
            games_lost.append(roll_counter)

    #display disabled to prevent large output volumes
    # display "wins" or "loses" message
    #if game_status == 'WON':
        #print('Player wins\n')
    #else:
        #print('Player loses\n')

#run simulations repeatedly based on command line argument
for i in range (game_count):
    play_game()

#obtain counts of each game length outcome
win_values, win_frequencies = np.unique(games_won, return_counts=True)
loss_values, loss_frequencies = np.unique(games_lost, return_counts=True)

#Enter np.unique's information into blank 13-element lists. This allows for 
#"0" entries when the number of rolls is relatively low. This cam also sum 
#rolls past 12 to collect information for a "13+" category for our charts
win_list = [0] * 13
for i in range(len(win_values)):
    value = win_values[i]
    if value <= 12:
        win_list[value-1] = win_frequencies[i]
    else:
        win_list[12] += value

loss_list = [0] * 13
for i in range(len(loss_values)):
    value = loss_values[i]
    if value <= 12:
        loss_list[value-1] = loss_frequencies[i]
    else:
        loss_list[12] += value

#concatenate win and loss records and calculate statistics over all games
games_total = games_won + games_lost
mean = statistics.mean(games_total)
median = statistics.median(games_total)
mode = statistics.mode(games_total)

#convert data to dataframe for graphing purposes
craps_df = pd.DataFrame({'Roll': list(range(1, 13)) + ['13+'],
                    'Wins': win_list, 
                    'Losses': loss_list,
                    })

#display records and statistics to the user
print(f"Displaying results from {game_count:,} simulated games of craps.\n")
print("Record of games won and on which roll:")
print()
print(craps_df.to_string(columns=['Roll','Wins'], index=False))
print()
print("Record of games lost and on which roll:")
print()
print(craps_df.to_string(columns=['Roll','Losses'], index=False))
print()
print(f"Total games won: {len(games_won)}")
print(f"Total games lost: {len(games_lost)}")
print(f"Win rate: {len(games_won) / len(games_total):.3%}")
print()
print(f"Empirical mean: {mean:.3f}")
print(f"Empirical median: {median}")
print(f"Empirical mode: {mode}")

#display data visually as a horizontal double bar plot
title = f'Craps Dice Game - Game Outcomes by Roll Count, {game_count:,} Games.'
sns.set_style('whitegrid')
axes = craps_df.set_index('Roll').plot.barh()
axes.set_title(title)
axes.invert_yaxis()
axes.set(xlabel = 'Outcome', ylabel = 'Roll Decided')

plt.show()    

##########################################################################
# (C) Copyright 2019 by Deitel & Associates, Inc. and                    #
# Pearson Education, Inc. All Rights Reserved.                           #
#                                                                        #
# DISCLAIMER: The authors and publisher of this book have used their     #
# best efforts in preparing the book. These efforts include the          #
# development, research, and testing of the theories and programs        #
# to determine their effectiveness. The authors and publisher make       #
# no warranty of any kind, expressed or implied, with regard to these    #
# programs or to the documentation contained in these books. The authors #
# and publisher shall not be liable in any event for incidental or       #
# consequential damages in connection with, or arising out of, the       #
# furnishing, performance, or use of these programs.                     #
##########################################################################

'''
Output:

Displaying results from 10,000,000 simulated games of craps.

Record of games won and on which roll:

Roll    Wins
   1 2223087
   2  771557
   3  550385
   4  392612
   5  281626
   6  200971
   7  143325
   8  102763
   9   73729
  10   53080
  11   37950
  12   27339
 13+    1013

Record of games lost and on which roll:

Roll  Losses
   1 1112325
   2 1111332
   3  797378
   4  572231
   5  411235
   6  296605
   7  213978
   8  152920
   9  111183
  10   79827
  11   58091
  12   41856
 13+    1153

Total games won: 4929649
Total games lost: 5070351
Win rate: 49.296%

Empirical mean: 3.374
Empirical median: 2.0
Empirical mode: 1
'''

'''
Answers to written questions:

b) What are the chances of winning at craps? [Note: You should discover that 
craps is one of the fairest casino games. What do you suppose this means?]

The winning odds start at 8/36, the sum of the odds for 7 and 11. 2, 3, and 
12 have combined odds of 4/36. The remaining numbers, 4, 5, 6, 8, 9, and 10,
each have different odds when taken up as the "point." The total odds of a win
depend on how each "point" respectively plays out over multiple rolls.

Since rolls other than the point and 7 result in a reroll, the most important
information is the odds of the point relative to 7, since what we need to know
is how likely we are to roll the point first. We find this by dividing 
the odds of the point by the odds of the point plus the odds of 7.

I will collapse pairs with identical odds for analysis: 

4 & 10 each have odds of 3/36. The odds compared to 7 are (3/36 / 9/36) = 1/3
5 & 9 each have odds of 4/36. The odds compared to 7 are (4/36 / 10/36) = 2/5
6 & 8 each have odds of 5/36. The odds compared to 7 are (5/36 / 11/36) = 5/11

We can then use these ratios with the odds from the first roll to see the 
overall odds of winning for each opening roll:

2: 1/36 * 0 (loss on first roll) = 0
3: 2/36 * 0 (loss on first roll) = 0
4: 3/36 * 1/3 = 1/36
5: 4/36 * 2/5 = 2/45
6: 5/36 * 5/11 = 25/396
7: 6/36 * 1 (win on first roll) = 1/6
8: 5/36 * 5/11 = 25/396
9: 4/36 * 2/5 = 2/45
10: 3/36 * 1/3 = 1/36
11: 2/36 * 1 (win on first roll) = 1/12
12: 1/36 * 0 (loss on first roll) = 0

These can be summed to 244/495, or ~49.293%. This is similar to the empirical
observed rate of 49.296%.

c) What is the mean for the length of a game of craps? The median? The mode?

In one third of cases, the game ends on the first roll. If not, it once again
depends on the individual dice odds of the point numbers. We can calculate the
average number of times it takes to roll either the point or a 7, then add one
to it because of the first roll which must have taken place.

These odds:

4 & 10 each have odds of 3/36. Adding those of 7, the total is 9/36 or 1/4
5 & 9 each have odds of 4/36. Adding those of 7, the total is 10/36 or 5/18
6 & 8 each have odds of 5/36. Adding those of 7, the total is 11/36

The expected number of rolls is equal to 1 divided by these values, plus 1 for
the starting roll:

2: 1 (loss on first roll)
3: 1 (loss on first roll)
4: 1 + (1 / (1/4) = 5
5: 1 + (1 / (5/18) = 23/5 (4.6)
6: 1 + (1 / (11/36) = 47/11 (4.273)
7: 1 (win on first roll)
8: 1 + (1 / (11/36) = 47/11 (4.273)
9: 1 + (1 / (5/18) = 23/5 (4.6)
10: 1 + (1 / (1/4) = 5
11: 1 (win on first roll)
12: 1 (loss on first roll) 

We then multiply them by the odds of the die roll:

2: 1/36 * 1 (loss on first roll) = 1/36
3: 2/36 * 1 (loss on first roll) = 2/36
4: 3/36 * 5 = 15/36
5: 4/36 * 23/5 = 23/45
6: 5/36 * 47/11 = 235/396
7: 6/36 * 1 (win on first roll) = 1/6
8: 5/36 * 47/11 = 235/396
9: 4/36 * 23/5 = 23/45
10: 3/36 * 5 = 15/36
11: 2/36 * 1 (win on first roll) = 1/18
12: 1/36 * 1 (loss on first roll) = 1/36

The sum of these is 557/165 or ~3.376, the mean length of a game of craps.
This is similar to the empirically observed mean of 3.374.

The mode is a single roll, since one third of all games are decided by the 
first roll, which has winning odds of 8/36, and losing odds of 4/36.
The odds of a second round are 2/3, but this has a high chance of being further
extended: 25/36 (69.4%) for a 6 or 8, and even more likely for other numbers, 
and since this results in an end probability of 11/36 or less, this prevents 
2, or any higher number, from being the mode. This is observed in our output.

The median is based on similar information. One third of games end on the first
roll, and the odds of the game ending on the second for a given point is:

(the odds of a roll ending the game * the odds of having rolled the point in
question during in the first roll)

These probabilities are as follows:

2: 0
3: 0
4: 9/36 * 3/36 = 27/1296
5: 10/36 * 4/36 = 40/1296
6: 11/36 * 5/36 = 55/1296
7: 0
8: 11/36 * 5/36 = 55/1296
9: 10/36 * 4/36 = 40/1296
10: 9/36 * 3/36 = 27/1296
11: 0
12: 0

They sum to 244/1296, or ~18.827%

Since the median is the midpoint of the distribution, and the 33.333% and 
18.827% odds of the first two rolls already sums to 52.16%, the median must 
lie in the distribution of the second roll, and is thus 2. We see this in our
simulation where the first two rounds total 3,335,412 + 1,882,889 = 5,218,301, 
which is 52.183% of the total rolls.

d) Do the chances of winning improve with the length of the game?

Past the first roll, all rolls have an equal probability of winning or losing
due to the independent nature of dice rolls. However, the odds of winning as
a whole, as a funciton of the number of rolls, decreases over time, since any 
die total taken as one's point will be less likely to be rolled than a 7, and 
continuing only exposes a player to more iterations of that uneven chance. The 
dwindling odds of a win can be observed empirically, as the win numbers are 
always lower than loss numbers after the first roll.
'''