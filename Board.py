# global variables for logging
max_queue_size = 0
visited_count = 0
solution_depth = 0
node_created = 0

class BFS_BOARDS:
	def board_to_tuple(self, board):
		return tuple(tuple(row) for row in board)

	def find_blank_position(self, board):
		for row in range(len(board)):
			for col in range(len(board[0])):
				if board[row][col] == ' ':
					return row, col

	def is_goal(self, board, goal):

		flattened_board = [cell for row in board for cell in row]
		return ''.join(flattened_board) == goal


class GBFS_BOARDS:
	def reconstruct_solution(self, puzzle):
		steps = []
		while puzzle.parent:
			steps.append(puzzle.parent[1])
			puzzle = puzzle.parent[0]

		# steps.append(puzzle.parent[1])
		return steps[::-1]

	class Puzzle:
		def __init__(self, board, goal, size, parent=None):
			self.board = board
			self.goal = goal
			self.size = size
			self.parent = parent

		def __lt__(self, other):
			return self.heuristic() < other.heuristic()

		def heuristic(self):
			count = 0
			for i, tile in enumerate(self.board):
				if tile != self.goal[i] and tile != ' ':
					count += 1
			return count

		def is_goal(self):
			return self.board == self.goal

		def possible_moves(self):
			moves = []
			space_index = self.board.index(' ')

			# Move up
			if space_index - self.size >= 0:
				new_board = list(self.board)
				new_board[space_index], new_board[space_index - self.size] = new_board[space_index - self.size], \
					new_board[
						space_index]
				moves.append(GBFS_BOARDS().Puzzle("".join(new_board), self.goal, self.size, parent=(self, "up")))

			# Move down
			if space_index + self.size < len(self.board):
				new_board = list(self.board)
				new_board[space_index], new_board[space_index + self.size] = new_board[space_index + self.size], \
					new_board[
						space_index]
				moves.append(GBFS_BOARDS().Puzzle("".join(new_board), self.goal, self.size, parent=(self, "down")))

			# Move left
			if space_index % self.size != 0:
				new_board = list(self.board)
				new_board[space_index], new_board[space_index - 1] = new_board[space_index - 1], new_board[space_index]
				moves.append(GBFS_BOARDS().Puzzle("".join(new_board), self.goal, self.size, parent=(self, "left")))

			# Move right
			if (space_index + 1) % self.size != 0:
				new_board = list(self.board)
				new_board[space_index], new_board[space_index + 1] = new_board[space_index + 1], new_board[space_index]
				moves.append(GBFS_BOARDS().Puzzle("".join(new_board), self.goal, self.size, parent=(self, "right")))

			return moves

		def print_board(self):
			for i in range(0, len(self.board), self.size):
				print(" ".join(self.board[i:i + self.size]))

class ASTAR_BOARDS:

	def input_converter(self, text: str):
		result = []
		for i in text:
			if i.isdigit():
				result.append(int(i))
			elif i == ' ':
				result.append(0)
			elif i in [chr(x) for x in range(65, 91)]:
				result.append(ord(i) - 55)
		return tuple(result)

	def get_neighbors(self, state, grid_size):
		neighbors = []
		zero_index = state.index(0)
		row, col = divmod(zero_index, grid_size)

		moves = [
			(-1, 0, 'Up'),
			(1, 0, 'Down'),
			(0, -1, 'Left'),
			(0, 1, 'Right')
		]

		for dr, dc, action in moves:
			new_row, new_col = row + dr, col + dc
			if 0 <= new_row < grid_size and 0 <= new_col < grid_size:
				new_state = list(state)
				new_index = new_row * grid_size + new_col
				new_state[zero_index], new_state[new_index] = new_state[new_index], new_state[zero_index]
				neighbors.append((tuple(new_state), action))

		return neighbors