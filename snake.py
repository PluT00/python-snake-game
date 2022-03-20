import curses
import random
import time


class Field:
	def __init__(self, x_size, y_size):
		self.x_size = x_size
		self.y_size = y_size

		self.food = []
		self.snake_parts = [[round(self.x_size / 2), round(self.y_size / 2)]]
		self.spawn_food()

		self.direction = curses.KEY_RIGHT

	def init_field(self):
		field = [['#'] * (self.x_size)]
		for i in range(self.y_size - 2):
			new_row = ['#']
			new_row.extend([' '] * (self.x_size - 2))
			new_row.extend('#')
			field.append(new_row)
		field.append(['#'] * (self.x_size))
		return field

	def draw_field(self, stdscr):
		field = self.init_field()
		snake = '@'
		food = '$'

		field[self.food[1]][self.food[0]] = food
		for snake_part in self.snake_parts:
			field[snake_part[1]][snake_part[0]] = snake

		stdscr.clear()
		for row in field:
			for col in row:
				stdscr.addstr(" " + col + " ")
			stdscr.addstr("\n")
		stdscr.refresh()

	def spawn_food(self):
		if self.food == []:
			self.food = [
				random.randint(2, self.x_size - 2),
				random.randint(2, self.y_size - 2)
			]

	def eat_food(self):
		if self.food in self.snake_parts:
			self.food = []
			self.spawn_food()
			self.snake_parts.insert(0, self.snake_parts[0][::])


class Snake(Field):
	def set_direction(self, stdscr):
		key = stdscr.getch()

		if self.direction == curses.KEY_RIGHT and key == curses.KEY_LEFT:
			return
		if self.direction == curses.KEY_LEFT and key == curses.KEY_RIGHT:
			return
		if self.direction == curses.KEY_UP and key == curses.KEY_DOWN:
			return
		if self.direction == curses.KEY_DOWN and key == curses.KEY_UP:
			return

		if key != -1:
			self.direction = key

	def move(self):
		head = self.snake_parts[-1]
		if len(self.snake_parts) > 1:
			self.snake_parts.append(self.snake_parts[-1][::])
			self.snake_parts.pop(0)

		if self.direction == curses.KEY_RIGHT:
			if head[0] != self.x_size - 2:
				self.snake_parts[-1][0] += 1
			else:
				self.snake_parts[-1][0] = 1
		elif self.direction == curses.KEY_LEFT:
			if head[0] != 1:
				self.snake_parts[-1][0] -= 1
			else:
				self.snake_parts[-1][0] = self.x_size - 2
		elif self.direction == curses.KEY_UP:
			if head[1] != 1:
				self.snake_parts[-1][1] -= 1
			else:
				self.snake_parts[-1][1] = self.y_size - 2
		elif self.direction == curses.KEY_DOWN:
			if head[1] != self.y_size - 2:
				self.snake_parts[-1][1] +=1
			else:
				self.snake_parts[-1][1] = 1

	def is_alive(self):
		head = self.snake_parts[-1]
		body = self.snake_parts[:-1]
		return head not in body

	def run(self, stdscr):
		stdscr.timeout(0)
		stdscr.nodelay(True)
		A = 0
		while True:
			if self.is_alive():
				self.set_direction(stdscr)
				self.eat_food()
				self.move()
				self.draw_field(stdscr)
				stdscr.refresh()
				time.sleep(.4)
			else:
				break
		stdscr.erase()
		stdscr.addstr("Game Over!")
		stdscr.refresh()
		stdscr.nodelay(False)
		stdscr.getkey()


if __name__ == "__main__":
	curses.wrapper(Snake(50, 50).run)