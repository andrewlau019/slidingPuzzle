from Solver import *
from Board import *


def count_inversions(board: str) -> int:
    counter = 0
    for i in range(len(board)):
	    current = board[i]
	    counter += len([x for x in board[i+1:] if current > x and x != ' '])

    return counter


def find_space_row(size: int, board_str: str) -> int:
    return board_str.index(' ')//size


def isSolvable(size, board_str):
	space_row = find_space_row(size, board_str)
	inversion = count_inversions(board_str)
	if size > 2:
		# odd
		if size % 2 == 1:
			if inversion % 2 == 0:
				return True
			else:
				return False
		else:
			if (inversion + space_row) % 2 == 0:
				return True
			else:
				return False
	else:
		return True
# 3 "123 46857" ASTAR


def main():
	print("Input: ", end="")
	user_input = input("")


	size = int(user_input[0])
	initial_board = user_input.split('"')[1]
	method = user_input.split()[-1]
	print(isSolvable(size, initial_board))

	if isSolvable(size, initial_board):
		if method == "BFS":
			BFS_IMPLEMENTATION(size, initial_board)
		elif method == "DFS":
			DFS_IMPLEMENTATION(size, initial_board)
		elif method == "GBFS":
			GBFS_IMPLEMENTATION(size, initial_board)
		elif method.lower() == "astar":
			A_STAR_IMPLEMENTATION(size, initial_board)
	else:
		print("The Board is unsolvable")

if __name__ == "__main__":
	main()