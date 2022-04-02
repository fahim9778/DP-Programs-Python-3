""" A Dynamic Programming Approach in Python 3.8 to calculate minimum coins required
    to make change of given amount & coin denominations """
import sys

infinity = sys.maxsize - 1  # defining system's maximum value as infinity


def beautify_table(amount):
    """ Function that prepares topmost DP table heading """
    print('\t', end='')
    print(*range(amount + 1), sep='\t', end='\n')
    print("_" * (amount * 5), sep='\t')


def print_dp_table(dp_table, amount, coins):
    """ Function that shows DP table values """
    beautify_table(amount)

    for row in range(1, len(dp_table)):
        print(f' {coins[row - 1]} |', end='')
        for col in range(len(dp_table[row])):
            if dp_table[row][col] == infinity:  # printing for infinite values to coins
                print(float('inf'), end='\t')
            else:
                print(dp_table[row][col], end='\t')
        print()


def which_coins(dp_table, amount, coins):
    """ Function that calculates which coins can be taken to make the minimum change """
    total_coins = len(coins)
    row = total_coins
    col = amount
    coins_to_take = []

    while (col > 0) and (row > 0):
        if dp_table[row][col] != dp_table[row - 1][col]:
            coins_to_take.append(coins[row - 1])
            col = col - coins[row - 1]
        else:
            row = row - 1
    return coins_to_take


def dp_minimum_coin_change(amount_to_fill, coins):
    """ Function to calculate the DP Table values """
    total_coins = len(coins)

    # Create a 2D-array of size [total coins + 1][amount + 1]
    dp_table = [[None] * (amount_to_fill + 1) for _ in range(total_coins + 1)]

    # Initialise DP array
    # Base Case 1: If price = 0 then min coins needed = 0 considering null set. So dp[i][0] = 0.
    for i in range(total_coins + 1):
        dp_table[i][0] = 0

    #  Base Case 2: If no. of coins = 0 then we would need infinite coins to get to price.
    #  So dp[0][j] = inf -1 ("-1 to avoid overflow)
    for j in range(amount_to_fill + 1):
        dp_table[0][j] = infinity

    # Now, for other cases, if (coin value > amount value), then copy from above cell
    # else, min(Exclude,  1 + Include)
    # Exclude == upper cell value
    # Include == 1+ minCoinsRequired(N-coins[i])
    for i in range(1, total_coins + 1):
        for j in range(1, amount_to_fill + 1):
            if coins[i - 1] > j:
                dp_table[i][j] = dp_table[i - 1][j]  # copy from above cell
            else:
                dp_table[i][j] = min(dp_table[i - 1][j], 1 + dp_table[i][j - coins[i - 1]])

    print_dp_table(dp_table, amount_to_fill, coins)

    # Returning multiple values to the calling function
    return [dp_table[total_coins][amount_to_fill], which_coins(dp_table, amount_to_fill, coins)]


if __name__ == '__main__':

    price = int(input("Input total amount: "))

    coins = list(map(int, input("Enter space separated coin values: ").strip().split()))

    coins.sort()

    [minCoins, coinsToTake] = dp_minimum_coin_change(price, coins)

    if minCoins >= infinity:
        print("\nImpossible to fill")
    else:
        print(f'\nMinimum coins required = {minCoins}')
        print(f'Possible Coin Values : {coinsToTake}')
