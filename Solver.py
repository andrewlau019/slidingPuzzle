from Board import *



def BFS_IMPLEMENTATION(size, given_initial_board):
	from collections import deque
	from copy import deepcopy


	def move(board, direction):
		row, col = BFS_BOARDS().find_blank_position(board)
		new_row, new_col = row, col

		if direction == 'UP':
			new_row -= 1
		elif direction == 'DOWN':
			new_row += 1
		elif direction == 'LEFT':
			new_col -= 1
		elif direction == 'RIGHT':
			new_col += 1

		if 0 <= new_row < len(board) and 0 <= new_col < len(board[0]):
			new_board = deepcopy(board)
			new_board[row][col], new_board[new_row][new_col] = new_board[new_row][new_col], new_board[row][col]
			return new_board
		return None

	def bfs_solver(size, initial_board, goal):
		global node_created, max_queue_size, visited_count, solution_depth

		initial_board = [list(initial_board[i:i + size]) for i in range(0, len(initial_board), size)]
		visited = set()
		queue = deque([(initial_board, [])])

		while queue:
			current_board, moves = queue.popleft()
			if BFS_BOARDS().is_goal(current_board, goal):
				return moves
			visited_count += 1
			for direction in ['UP', 'DOWN', 'LEFT', 'RIGHT']:
				new_board = move(current_board, direction)
				if new_board and BFS_BOARDS().board_to_tuple(new_board) not in visited:
					visited.add(BFS_BOARDS().board_to_tuple(new_board))
					queue.append((new_board, moves + [direction]))
					node_created += 1
					max_queue_size = max(max_queue_size, len(queue))

	with open('readme.txt', 'a+') as wfile:
		global node_created, max_queue_size, visited_count, solution_depth
		i = [x for x in [(2, '213 '), (3, ' 12345678'), (4, "123456789ABCDEF ")] if x[0] == size][0]
		max_queue_size = 0
		visited_count = 0
		solution_depth = 0
		node_created = 0

		size = i[0]
		initial_board = given_initial_board
		goal = i[1]

		moves = bfs_solver(size, initial_board, goal)
		for i in range(len(moves)):
			print(f"Step {i + 1}: {moves[i]}")

		wfile.write(f"---------\n")
		wfile.write(f"size: {size}\n")
		wfile.write(f"initial board: {initial_board}\n")
		wfile.write(f"goal: {goal}\n")
		wfile.write(f"searchmethod: BFS\n")
		wfile.write(f"{max_queue_size}, {visited_count}, {node_created}, {solution_depth}\n")
		wfile.close()


def DFS_IMPLEMENTATION(size, initial_board):
	import sys


	sys.setrecursionlimit(10000)

	visited_count = 0
	max_queue_size = 0
	node_created = 0

	def sliding_puzzle_dfs(board_size, board_state, goal):
		def get_moves(position, board_size):
			row, col = divmod(position, board_size)
			counter = 0
			for r_diff, c_diff in ((0, 1), (1, 0), (0, -1), (-1, 0)):
				new_row, new_col = row + r_diff, col + c_diff
				if 0 <= new_row < board_size and 0 <= new_col < board_size:
					yield new_row * board_size + new_col, ["RIGHT", "UP", "LEFT", "DOWN"][counter]
				counter += 1

		def dfs(visited, path, goal, direction=None):
			global visited_count, node_created, max_queue_size
			if path[-1] == goal:
				return path, [direction]

			visited.add(path[-1])
			visited_count += 1
			empty_tile_index = path[-1].index(' ')

			for next_move, direction in get_moves(empty_tile_index, board_size):
				new_board = list(path[-1])
				max_queue_size = max(max_queue_size, len(path))
				new_board[empty_tile_index], new_board[next_move] = new_board[next_move], new_board[empty_tile_index]
				new_board_str = ''.join(new_board)


				if new_board_str not in visited:
					new_path = dfs(visited, path + [new_board_str], goal, direction)
					node_created += 1
					# print(new_path)
					if new_path:
						return new_path[0], new_path[1] + [direction]

			visited.remove(path[-1])
			return None

		initial_state = board_state

		return dfs(set(), [initial_state], goal, direction=None)

	node_created = 0
	visited_count = 0
	max_queue_size = 0

	i = [x for x in [(2, "213 "), (3, " 12345678"), (4, "123456789ABCDEF ")] if x[0] == size][0]
	board_size = size
	board_state = initial_board
	goal = i[1]
	solution, answers = sliding_puzzle_dfs(board_size, board_state, goal)

	for i in range(len(answers)):
	 print(f"Step {i}: {answers[i]}")


	with open("readme.txt", "a+") as wfile:
		wfile.write(f"---------\n")
		wfile.write(f"size: {size}\n")
		wfile.write(f"initial board: {initial_board}\n")
		wfile.write(f"goal: {goal}\n")
		wfile.write(f"searchmethod: BFS\n")
		wfile.write(f"{max_queue_size}, {visited_count}, {node_created}, {solution_depth}\n")
		wfile.close()


def GBFS_IMPLEMENTATION(size, initial_board):
	import heapq
	import sys


	def greedy_best_first_search(puzzle):
		global node_created, visited_count, max_queue_size
		visited = set()
		frontier = [puzzle]

		while frontier:
			current_puzzle = heapq.heappop(frontier)
			max_queue_size = max(max_queue_size, len(frontier))

			visited.add(current_puzzle.board)
			visited_count += 1

			if current_puzzle.is_goal():
				return current_puzzle

			for move in current_puzzle.possible_moves():
				if move.board not in visited:
					heapq.heappush(frontier, move)
					node_created += 1

		return None



	def gbfs_main(size, inital_board):
		global node_created, visited_count, max_queue_size

		goal_board = [x for x in [(2, "213 "), (3, " 12345678"), (4, "123456789ABCDEF ")] if x[0] == size][0][1]

		puzzle = GBFS_BOARDS().Puzzle(inital_board, goal_board, size)
		solution = greedy_best_first_search(puzzle)

		if solution:
			print("Solution found!")
			steps = GBFS_BOARDS().reconstruct_solution(solution)
			for i, step in enumerate(steps):
				print(f"Step {i}: {step}")

		else:
			print("No solution found.")

		with open("readme.txt", "a+") as wfile:
			wfile.write(f"---------\n")
			wfile.write(f"size: {size}\n")
			wfile.write(f"initial board: {initial_board}\n")
			wfile.write(f"goal: {goal_board}\n")
			wfile.write(f"searchmethod: BFS\n")
			wfile.write(f"{max_queue_size}, {visited_count}, {node_created}, {solution_depth}\n")
			wfile.close()

	gbfs_main(size, initial_board)


def A_STAR_IMPLEMENTATION(size, initial_board):
	import heapq
	from collections import namedtuple

	Node = namedtuple('Node', ['state', 'parent', 'action', 'cost'])
	node_created = 0
	visited_count = 0
	max_queue_size = 0





	def manhattan_distance(state, goal, grid_size):
		distance = 0
		for i in range(1, grid_size ** 2):
			row1, col1 = divmod(state.index(i), grid_size)
			row2, col2 = divmod(goal.index(i), grid_size)
			distance += abs(row1 - row2) + abs(col1 - col2)
		return distance

	def a_star_search(initial_state, goal_state, grid_size):
		global visited_count, node_created, max_queue_size
		frontier = [(manhattan_distance(initial_state, goal_state, grid_size), 0, Node(initial_state, None, None, 0))]
		explored = set()

		while frontier:
			_, _, current = heapq.heappop(frontier)
			max_queue_size = max(max_queue_size, len(frontier))
			if current.state == goal_state:
				return current

			explored.add(current.state)
			visited_count += 1

			for neighbor_state, action in ASTAR_BOARDS().get_neighbors(current.state, grid_size):
				if neighbor_state not in explored:
					neighbor_cost = current.cost + 1
					heapq.heappush(frontier, (
						manhattan_distance(neighbor_state, goal_state, grid_size) + neighbor_cost, neighbor_cost,
						Node(neighbor_state, current, action, neighbor_cost)))
					node_created += 1
		return None

	def a_star_main(size, initial_board):
		global node_created, visited_count, max_queue_size
		grid_size = size
		initial_state = ASTAR_BOARDS().input_converter(initial_board)

		goal_state = ASTAR_BOARDS().input_converter(
			[x[1] for x in [(2, "213 "), (3, "47315862 "), (4, "123456789ABCDEF ")] if x[0] == size][0])

		result = a_star_search(initial_state, goal_state, grid_size)
		if result is None:
			print("No solution found")
		else:
			path = []
			while result.parent is not None:
				path.append(result.action)
				result = result.parent
			path.reverse()
			for i in range(len(path)):
				print(f"Step {i}: {path[i]}")

			with open("readme.txt", "a+") as w:
				w.write("----------------\n")
				w.write(f"size: {grid_size}\n")
				w.write(f"initial: {initial_state}\n")
				w.write(f"goal: {goal_state}\n")
				w.write(f"searchmethod: AStar\n")
				w.write(f"{visited_count} {node_created} {visited_count} {max_queue_size}\n")

	a_star_main(size, initial_board)


