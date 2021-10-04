"""CS 61A Presents The Game of Hog."""

from dice import six_sided, four_sided, make_test_dice
from ucb import main, trace, interact

GOAL_SCORE = 100  # The goal of Hog is to score 100 points.
FIRST_101_DIGITS_OF_PI = 31415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679


######################
# Phase 1: Simulator #
######################


def roll_dice(num_rolls, dice=six_sided):
    """Simulate rolling the DICE exactly NUM_ROLLS > 0 times. Return the sum of
    the outcomes unless any of the outcomes is 1. In that case, return 1.

    num_rolls:  The number of dice rolls that will be made.
    dice:       A function that simulates a single dice roll outcome.
    """

    ###############
    # My Solution #
    ###############

    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls > 0, 'Must roll at least once.'

    i = 0
    score = 0
    pigout = False
    while i < num_rolls:
        roll = dice()
        if roll == 1:
            pigout = True
        else:
            score+=roll
        i+=1

    if pigout == True:
        score=1

    return score

def free_bacon(score):
    """Return the points scored from rolling 0 dice (Free Bacon).

    score:  The opponent's current score.
    """

    ###############
    # My Solution #
    ###############

    assert score < 100, 'The game should be over.'
    pi = FIRST_101_DIGITS_OF_PI

    pi = pi//(10**(100-score))

    return pi % 10 + 3


def take_turn(num_rolls, opponent_score, dice=six_sided):
    """Simulate a turn rolling NUM_ROLLS dice, which may be 0 (Free Bacon).
    Return the points scored for the turn by the current player.

    num_rolls:       The number of dice rolls that will be made.
    opponent_score:  The total score of the opponent.
    dice:            A function that simulates a single dice roll outcome.
    """

    ###############
    # My Solution #
    ###############

    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls >= 0, 'Cannot roll a negative number of dice in take_turn.'
    assert num_rolls <= 10, 'Cannot roll more than 10 dice.'
    assert opponent_score < 100, 'The game should be over.'

    if num_rolls==0:
        return free_bacon(opponent_score)
    else:
        return roll_dice(num_rolls, dice)

def extra_turn(player_score, opponent_score):
    """Return whether the player gets an extra turn."""

    ###############
    # My Solution #
    ###############

    return (pig_pass(player_score, opponent_score) or
            swine_align(player_score, opponent_score))

def swine_align(player_score, opponent_score):
    """Return whether the player gets an extra turn due to Swine Align.

    player_score:   The total score of the current player.
    opponent_score: The total score of the other player."""

    ###############
    # My Solution #
    ###############

    a = player_score
    b = opponent_score

    if (a==0) or (b==0):
        return False

    while b:
        a, b = b, a % b
    
    
    if a >= 10:
        return True
    
    return False

def pig_pass(player_score, opponent_score):
    """Return whether the player gets an extra turn due to Pig Pass.

    player_score:   The total score of the current player.
    opponent_score: The total score of the other player."""

    ###############
    # My Solution #
    ###############

    if (player_score < opponent_score) & (opponent_score-player_score < 3):
        return True
    else:
        return False

def other(who):
    """Return the other player, for a player WHO numbered 0 or 1."""
    return 1 - who

def silence(score0, score1):
    """Announce nothing (see Phase 2)."""
    return silence

def play(strategy0, strategy1, score0=0, score1=0, dice=six_sided,
         goal=GOAL_SCORE, say=silence):
    """Simulate a game and return the final scores of both players, with Player
    0's score first, and Player 1's score second.

    A strategy is a function that takes two total scores as arguments (the
    current player's score, and the opponent's score), and returns a number of
    dice that the current player will roll this turn.

    strategy0:  The strategy function for Player 0, who plays first.
    strategy1:  The strategy function for Player 1, who plays second.
    score0:     Starting score for Player 0
    score1:     Starting score for Player 1
    dice:       A function of zero arguments that simulates a dice roll.
    goal:       The game ends and someone wins when this score is reached.
    say:        The commentary function to call at the end of the first turn.
    """

    ###############
    # My Solution #
    ###############
    
    player, player_score, opponent_score = 0, score0, score1
    commentary = say

    while (score0 < goal) & (score1 < goal):
        rolls = 0

        if player == 0:
            
            rolls = strategy0(score0, score1)

            score0 += take_turn(rolls, score1, dice)
            commentary = commentary(score0, score1)
            
            if (score0 >= goal):
                    break
            
            if extra_turn(score0, score1) == False:
                player = other(player)    

                
        else:
            rolls = strategy1(score1, score0)

            score1 += take_turn(rolls, score0, dice)
            commentary = commentary(score0, score1)
 
            if (score1 >= goal):
                 break

            if extra_turn(score1, score0) == False:
                player = other(player)    
        
    return score0, score1


#######################
# Phase 2: Commentary #
#######################


def say_scores(score0, score1):
    """A commentary function that announces the score for each player."""
    print("Player 0 now has", score0, "and Player 1 now has", score1)
    return say_scores

def announce_lead_changes(last_leader=None):
    """Return a commentary function that announces lead changes."""

    ###############
    # My Solution #
    ###############

    def say(score0, score1):
        if score0 > score1:
            leader = 0
        elif score1 > score0:
            leader = 1
        else:
            leader = None
        if leader != None and leader != last_leader:
            print('Player', leader, 'takes the lead by', abs(score0 - score1))
        return announce_lead_changes(leader)
    return say

def both(f, g):
    """Return a commentary function that says what f says, then what g says."""
    def say(score0, score1):
        return both(f(score0, score1), g(score0, score1))
    return say

def announce_highest(who, last_score=0, running_high=0):
    """Return a commentary function that announces when WHO's score
    increases by more than ever before in the game."""

    ###############
    # My Solution #
    ###############

    assert who == 0 or who == 1, 'The who argument should indicate a player.'

    def say(score0, score1):
        if who == 1:
            score_gained = score1 - last_score
            current_high = running_high
            if score_gained > running_high:
                print (f'{score_gained} point(s)! The most yet for Player {who}')
                current_high = score_gained
            return announce_highest(who, score1, current_high)        
        else:
            score_gained = score0 - last_score
            current_high = running_high
            if score_gained > running_high:
                print (f'{score_gained} point(s)! The most yet for Player {who}')
                current_high = score_gained
            return announce_highest(who, score0, current_high)   
    return say


#######################
# Phase 3: Strategies #
#######################


def always_roll(n):
    """Return a strategy that always rolls N dice.

    A strategy is a function that takes two total scores as arguments (the
    current player's score, and the opponent's score), and returns a number of
    dice that the current player will roll this turn."""

    def strategy(score, opponent_score):
        return n
    return strategy

def make_averaged(original_function, trials_count=1000):
    """Return a function that returns the average value of ORIGINAL_FUNCTION
    when called.

    To implement this function, you will have to use *args syntax, a new Python
    feature introduced in this project.  See the project description."""

    ###############
    # My Solution #
    ###############

    def return_average(*args):
        count = 0
        results = 0
        while count < trials_count:
            results+= original_function(*args)
            count+=1
        return results/trials_count
    
    return return_average

def max_scoring_num_rolls(dice=six_sided, trials_count=1000):
    """Return the number of dice (1 to 10) that gives the highest average turn
    score by calling roll_dice with the provided DICE over TRIALS_COUNT times.
    Assume that the dice always return positive outcomes."""

    ###############
    # My Solution #
    ###############

    best_roll = make_averaged(roll_dice, trials_count)

    roll = 1
    avg = []
    while roll <= 10:
        avg.append(best_roll(roll, dice))
        roll+=1

    max_roll = max(avg)
    result = avg.index(max_roll) + 1

    return result, max_roll

def winner(strategy0, strategy1):
    """Return 0 if strategy0 wins against strategy1, and 1 otherwise."""
    score0, score1 = play(strategy0, strategy1)
    if score0 > score1:
        return 0
    else:
        return 1

def average_win_rate(strategy, baseline=always_roll(4)):
    """Return the average win rate of STRATEGY against BASELINE. Averages the
    winrate when starting the game as player 0 and as player 1.
    """
    win_rate_as_player_0 = 1 - make_averaged(winner)(strategy, baseline)
    win_rate_as_player_1 = make_averaged(winner)(baseline, strategy)

    return (win_rate_as_player_0 + win_rate_as_player_1) / 2

def run_experiments():
    """Run a series of strategy experiments and report results."""
    if True:  # Change to False when done finding max_scoring_num_rolls
        six_sided_max = max_scoring_num_rolls(six_sided)
        print('Max scoring num rolls for six-sided dice:', six_sided_max)

    if True:  # Change to True to test always_roll(8)
        print('always_roll(8) win rate:', average_win_rate(always_roll(8)))

    if True:  # Change to True to test bacon_strategy
        print('bacon_strategy win rate:', average_win_rate(bacon_strategy))

    if True:  # Change to True to test extra_turn_strategy
        print('extra_turn_strategy win rate:', average_win_rate(extra_turn_strategy))

    if True:  # Change to True to test final_strategy
        print('final_strategy win rate:', average_win_rate(final_strategy))

def bacon_strategy(score, opponent_score, cutoff=8, num_rolls=6):
    """This strategy rolls 0 dice if that gives at least CUTOFF points, and
    rolls NUM_ROLLS otherwise.
    """

    ###############
    # My Solution #
    ###############

    if free_bacon(opponent_score) >= cutoff:
        return 0
    else:
        return num_rolls

def extra_turn_strategy(score, opponent_score, cutoff=8, num_rolls=6):
    """This strategy rolls 0 dice when it triggers an extra turn. It also
    rolls 0 dice if it gives at least CUTOFF points and does not give an extra turn.
    Otherwise, it rolls NUM_ROLLS.
    """

    ###############
    # My Solution #
    ###############

    score_after_bacon = score + free_bacon(opponent_score)

    if extra_turn(score_after_bacon, opponent_score):
        return 0

    return bacon_strategy(score, opponent_score, cutoff, num_rolls) 


##########################
# Command Line Interface #
##########################


# NOTE: Functions in this section do not need to be changed. They use features
# of Python not yet covered in the course.


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions."""
    import argparse
    parser = argparse.ArgumentParser(description="Play Hog")
    parser.add_argument('--run_experiments', '-r', action='store_true',
                        help='Runs strategy experiments')

    args = parser.parse_args()

    if args.run_experiments:
        run_experiments()