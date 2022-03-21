import curses
import random
import sys
import time


class Menu:
	def __init__(self):
		self.position = 0
		self.items = ['New game', 'Quit']

		self.state = 'in_menu'

	def navigation(self, stdscr):
		key = stdscr.getch()

		if key == curses.KEY_UP and self.position > 0:
			self.position -= 1
		elif key == curses.KEY_DOWN and self.position < len(self.items) - 1:
			self.position += 1
		if key in {curses.KEY_ENTER, 10, 13}:
			if self.position == 0:
				self.state = 'in_game'
			elif self.position == 1:
				sys.exit()

	def draw_menu(self, stdscr):
		curses.curs_set(0)
		stdscr.erase()
		for key, item in enumerate(self.items):
			if self.position == key:
				stdscr.addstr(key + 5, 10, "-> " + item + " <-", curses.A_BOLD)
			else:
				stdscr.addstr(key + 5, 10, "   " + item + "   ")
		stdscr.refresh()

	def run_menu(self, stdscr):
		self.draw_menu(stdscr)
		self.navigation(stdscr)


class Field:
	def __init__(self, x_size, y_size):
		self.menu = Menu()

		self.x_size = x_size
		self.y_size = y_size

		self.food = []
		self.start_snake = [[round(self.x_size / 2), round(self.y_size / 2)]]
		self.snake_parts = [[round(self.x_size / 2), round(self.y_size / 2)]][::]
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
		head = '@'
		body = 'o'
		food = '$'

		field[self.food[1]][self.food[0]] = food
		for key, snake_part in enumerate(self.snake_parts):
			if key == len(self.snake_parts) - 1:
				field[snake_part[1]][snake_part[0]] = head
			else:
				field[snake_part[1]][snake_part[0]] = body

		stdscr.clear()
		for row in field:
			for col in row:
				stdscr.addstr(" " + col + " ")
			stdscr.addstr("\n")

		stdscr.addstr(
			self.y_size - 1, self.x_size * 3 + 5,
			f'Score: {len(self.snake_parts) - 1}'
		)
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

	def is_alive(self):
		head = self.snake_parts[-1]
		body = self.snake_parts[:-1]
		if head in body:
			self.menu.state = 'in_menu'
			self.snake_parts = self.start_snake[::]


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

	def run(self, stdscr):
		stdscr.timeout(0)
		stdscr.nodelay(True)
		curses.curs_set(0)
		while True:
			self.is_alive()
			if self.menu.state == 'in_game':
				self.set_direction(stdscr)
				self.eat_food()
				self.move()
				self.draw_field(stdscr)
				stdscr.refresh()

				time_to_wait = 0.4 - len(self.snake_parts) / 100
				if time_to_wait >= 0.1:
					time.sleep(time_to_wait)
				else:
					time.sleep(0.1)
			elif self.menu.state == 'in_menu':
				self.menu.run_menu(stdscr)


if __name__ == "__main__":
	curses.wrapper(Snake(50, 50).run)