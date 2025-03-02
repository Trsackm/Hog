"""The Game of Hog."""

from dice import six_sided, make_test_dice
from ucb import main, trace, interact

GOAL = 100  # The goal of Hog is to score 100 points.

######################
# Phase 1: Simulator #
######################


def roll_dice(num_rolls, dice=six_sided):
    """Simulate rolling the DICE exactly NUM_ROLLS > 0 times. Return the sum of
    the outcomes unless any of the outcomes is 1. In that case, return 1.

    num_rolls:  The number of dice rolls that will be made.
    dice:       A function that simulates a single dice roll outcome. Defaults to the six sided dice.
    """
    # These assert statements ensure that num_rolls is a positive integer.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls > 0, 'Must roll at least once.'
    # BEGIN PROBLEM 1
    i = 1
    score = 0
    SowSad = False
    while i <= num_rolls:
        a = dice()
        if(a == 1):
            SowSad = True
        else:
            score = score + a 
        i = i + 1
    if SowSad:
        return 1
    else:
        return score
    # END PROBLEM 1


def boar_brawl(player_score, opponent_score):
    """Return the points scored when the current player rolls 0 dice according to Boar Brawl.

    player_score:     The total score of the current player.
    opponent_score:   The total score of the other player.

    """
    # BEGIN PROBLEM 2
    return max(3*(abs(digit(player_score,0)-digit(opponent_score,1))),1)
    # END PROBLEM 2

def digit(number,place):
    return (number%pow(10,place+1))//pow(10,place)

def take_turn(num_rolls, player_score, opponent_score, dice=six_sided):
    """Return the points scored on a turn rolling NUM_ROLLS dice when the
    current player has PLAYER_SCORE points and the opponent has OPPONENT_SCORE points.

    num_rolls:       The number of dice rolls that will be made.
    player_score:    The total score of the current player.
    opponent_score:  The total score of the other player.
    dice:            A function that simulates a single dice roll outcome.
    """
    # Leave these assert statements here; they help check for errors.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls >= 0, 'Cannot roll a negative number of dice in take_turn.'
    assert num_rolls <= 10, 'Cannot roll more than 10 dice.'
    # BEGIN PROBLEM 3
    if num_rolls == 0:
        return boar_brawl(player_score, opponent_score)
    else:
        return roll_dice(num_rolls, dice)
    # END PROBLEM 3


def simple_update(num_rolls, player_score, opponent_score, dice=six_sided):
    """Return the total score of a player who starts their turn with
    PLAYER_SCORE and then rolls NUM_ROLLS DICE, ignoring Sus Fuss.
    """
    score = player_score + take_turn(num_rolls, player_score, opponent_score, dice)
    return score

def is_prime(n):
    """Return whether N is prime."""
    if n == 1:
        return False
    k = 2
    while k < n:
        if n % k == 0:
            return False
        k += 1
    return True

def num_factors(n):
    """Return the number of factors of N, including 1 and N itself."""
    # BEGIN PROBLEM 4
    counter = 1
    divisor = 1
    while divisor <= n/2:
        if n%divisor == 0:
            counter += 1
        divisor += 1
    return counter 
    # END PROBLEM 4

def sus_points(score):
    """Return the new score of a player taking into account the Sus Fuss rule."""
    # BEGIN PROBLEM 4
    if num_factors(score) == 3 or num_factors(score) == 4: 
        return findNextprime(score) # function that finds the next prime given a number
    else:
        return score
    # END PROBLEM 4

def findNextprime(n):
    counter = n
    while True: 
        if is_prime(counter): 
            return counter
        counter += 1
    
def sus_update(num_rolls, player_score, opponent_score, dice=six_sided):
    """Return the total score of a player who starts their turn with
    PLAYER_SCORE and then rolls NUM_ROLLS DICE, *including* Sus Fuss.
    """
    # BEGIN PROBLEM 4
    return sus_points(simple_update(num_rolls, player_score, opponent_score, dice ))
    # END PROBLEM 4


def always_roll_5(score, opponent_score):
    """A strategy of always rolling 5 dice, regardless of the player's score or
    the opponent's score.
    """
    return 5


def play(strategy0, strategy1, update,
         score0=0, score1=0, dice=six_sided, goal=GOAL):
    """Simulate a game and return the final scores of both players, with
    Player 0's score first and Player 1's score second.

    E.g., play(always_roll_5, always_roll_5, sus_update) simulates a game in
    which both players always choose to roll 5 dice on every turn and the Sus
    Fuss rule is in effect.

    A strategy function, such as always_roll_5, takes the current player's
    score and their opponent's score and returns the number of dice the current
    player chooses to roll.

    An update function, such as sus_update or simple_update, takes the number
    of dice to roll, the current player's score, the opponent's score, and the
    dice function used to simulate rolling dice. It returns the updated score
    of the current player after they take their turn.

    strategy0: The strategy for player0.
    strategy1: The strategy for player1.
    update:    The update function (used for both players).
    score0:    Starting score for Player 0
    score1:    Starting score for Player 1
    dice:      A function of zero arguments that simulates a dice roll.
    goal:      The game ends and someone wins when this score is reached.
    """
    who = 0  # Who is about to take a turn, 0 (first) or 1 (second)
    # BEGIN PROBLEM 5
    while score0 < goal and score1 < goal:
        if who == 0:
            #player0 turn
            score0 = update(strategy0(score0,score1), score0, score1, dice)
        else:
            #player1 turn
            score1 = update(strategy1(score1,score0), score1, score0, dice)
        who = 1 - who
        
    # END PROBLEM 5
    return score0, score1


#######################
# Phase 2: Strategies #
#######################


def always_roll(n):
    """Return a player strategy that always rolls N dice.

    A player strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    >>> strategy = always_roll(3)
    >>> strategy(0, 0)
    3
    >>> strategy(99, 99)
    3
    """
    assert n >= 0 and n <= 10
    # BEGIN PROBLEM 6
    def roller(score0,score1):
        return n
    return roller
    # END PROBLEM 6


def catch_up(score, opponent_score):
    """A player strategy that always rolls 5 dice unless the opponent
    has a higher score, in which case 6 dice are rolled.

    >>> catch_up(9, 4)
    5
    >>> strategy(17, 18)
    6
    """
    if score < opponent_score:
        return 6  # Roll one more to catch up
    else:
        return 5


def is_always_roll(strategy, goal=GOAL):
    """Return whether STRATEGY always chooses the same number of dice to roll 
    for every possible combination of score and opponent_score
    given a game that goes to GOAL points.

    >>> is_always_roll(always_roll_5)
    True
    >>> is_always_roll(always_roll(3))
    True
    >>> is_always_roll(catch_up)
    False
    """
    # BEGIN PROBLEM 7
    score0, score1 = 0,0
    while score0 <= goal:
        while score1 <= goal:
            if strategy(score0,score1) != strategy(score0, score1 + 1):
                return False
            score1 += 1
        score1 = 0
        score0 += 1
    return True
    # END PROBLEM 7


def make_averaged(original_function, times_called=1000):
    """Return a function that returns the average value of ORIGINAL_FUNCTION
    called TIMES_CALLED times.

    To implement this function, you will have to use *args syntax.

    >>> dice = make_test_dice(4, 2, 5, 1)
    >>> averaged_dice = make_averaged(roll_dice, 40)
    >>> averaged_dice(1, dice)  # The avg of 10 4's, 10 2's, 10 5's, and 10 1's
    3.0
    """
    # BEGIN PROBLEM 8
    def averageR(*args):
        i, average = 0, 0
        while i < times_called:
            average += original_function(*args)
            i +=  1
        return average/times_called
    return averageR

    # END PROBLEM 8


def max_scoring_num_rolls(dice=six_sided, times_called=1000):
    """Return the number of dice (1 to 10) that gives the maximum average score for a turn.
    Assume that the dice always return positive outcomes.

    >>> dice = make_test_dice(1, 6)
    >>> max_scoring_num_rolls(dice)
    1
    """
    # BEGIN PROBLEM 9
    is_this_MAX, num_rolls_MAX, i = 0,1,1
    while i <= 10:
        testRoll_value = make_averaged(roll_dice,times_called)(i,dice)
        if testRoll_value > is_this_MAX: 
            is_this_MAX = testRoll_value
            num_rolls_MAX = i
        i += 1
    return num_rolls_MAX       
    # END PROBLEM 9


def winner(strategy0, strategy1):
    """Return 0 if strategy0 wins against strategy1, and 1 otherwise."""
    score0, score1 = play(strategy0, strategy1, sus_update)
    if score0 > score1:
        return 0
    else:
        return 1


def average_win_rate(strategy, baseline=always_roll(6)):
    """Return the average win rate of STRATEGY against BASELINE. Averages the
    winrate when starting the game as player 0 and as player 1.
    """
    win_rate_as_player_0 = 1 - make_averaged(winner)(strategy, baseline)
    win_rate_as_player_1 = make_averaged(winner)(baseline, strategy)

    return (win_rate_as_player_0 + win_rate_as_player_1) / 2


def run_experiments():
    """Run a series of strategy experiments and report results."""
    six_sided_max = max_scoring_num_rolls(six_sided)
    print('Max scoring num rolls for six-sided dice:', six_sided_max)

    print('always_roll(6) win rate:', average_win_rate(always_roll(6))) # near 0.5
    print('catch_up win rate:', average_win_rate(catch_up))
    print('always_roll(3) win rate:', average_win_rate(always_roll(3)))
    print('always_roll(8) win rate:', average_win_rate(always_roll(8)))

    print('boar_strategy win rate:', average_win_rate(boar_strategy))
    print('sus_strategy win rate:', average_win_rate(sus_strategy))
    print('final_strategy win rate:', average_win_rate(final_strategy))
    "*** You may add additional experiments as you wish ***"



def boar_strategy(score, opponent_score, threshold=11, num_rolls=6):
    """This strategy returns 0 dice if Boar Brawl gives at least THRESHOLD
    points, and returns NUM_ROLLS otherwise. Ignore the Sus Fuss rule.
    """
    # BEGIN PROBLEM 10
    if boar_brawl(score,opponent_score) >= threshold: 
        return 0
    else:
        return num_rolls  # Remove this line once implemented.
    # END PROBLEM 10


def sus_strategy(score, opponent_score, threshold=11, num_rolls=6):
    """This strategy returns 0 dice when rolling 0 increases the score by at least
    THRESHOLD points, and returns NUM_ROLLS otherwise. Consider both the Boar Brawl and 
    Suss Fuss rules."""
    # BEGIN PROBLEM 11
    if sus_update(0,score, opponent_score) - score >= threshold:
        return 0
    else: 
        return num_rolls  # Remove this line once implemented.
    # END PROBLEM 11


def final_strategy(score, opponent_score):
    """Write a brief description of your final strategy.
    This first looks if it is possible to win in 10 moves. 
    If not, it will see if boar_brawl can increase the score by 10. 
    If not, it looks for increasingly dire situations (and returning increasingly largers num_rolls) for the player trying a all-or nothing approach if the gap is too large.

    *** YOUR DESCRIPTION HERE ***
    """
    # BEGIN PROBLEM 12
    i = 0
    test_dice = make_averaged(six_sided, 10)
    while i < 10: 
        score_tracker = simple_update(i,score,opponent_score,test_dice)
        if score_tracker >= GOAL:
            return i
        else: 
            i += 1
    if boar_brawl(score,opponent_score)> 10:
        return 0
    if score - opponent_score > 10:
        return 3
    else: 
        if score - opponent_score < 0: 
            if score - opponent_score < -30:
                return 8
            return 6
        return 4
    # END PROBLEM 12


##########################
# Command Line Interface #
##########################

# NOTE: The function in this section does not need to be changed. It uses
# features of Python not yet covered in the course.

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




def s(x, y):
    if x == 60 and y == 0:
        return 0  
    else:     
        return 1