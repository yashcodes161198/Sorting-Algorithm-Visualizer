import pygame
import random
import math
pygame.init()

class DrawInformation:
	BLACK = 0, 0, 0
	WHITE = 255, 255, 255
	GREEN = 0, 255, 0
	RED = 255, 0, 0
	BACKGROUND_COLOR = WHITE

	GRADIENTS = [
		(128, 128, 128),
		(160, 160, 160),
		(192, 192, 192)
	]

	FONT = pygame.font.SysFont('comicsans', 30)
	LARGE_FONT = pygame.font.SysFont('comicsans', 40)

	SIDE_PAD = 100
	TOP_PAD = 150

	def __init__(self, width, height, lst):
		# this is the constructor for class DrawInformation
		self.width = width
		self.height = height

		self.window = pygame.display.set_mode((width, height)) #when we work with pygame, we need to access the drawing area. to easily access this drawing area, we can set it as an attribute of class DrawInformation
		pygame.display.set_caption("Sorting Algorithm Visualization")#this sets the title of our pygame window
		self.set_list(lst) #here we are simply calling another function set_list 

	def set_list(self, lst):
		# #this methos/fun takes the list lst as input and decides 2 things:
		# 1. the resolution of our drawing area. ie what height of bar corresponds to a value on the list
		# 2. the starting x-coordinate(top left corner of the left-most bar)
		self.lst = lst
		self.min_val = min(lst)
		self.max_val = max(lst)

		self.block_width = round((self.width - self.SIDE_PAD) / len(lst))
		self.block_height = math.floor((self.height - self.TOP_PAD) / (self.max_val - self.min_val))
		self.start_x = self.SIDE_PAD // 2


def draw(draw_info, algo_name, ascending):
	draw_info.window.fill(draw_info.BACKGROUND_COLOR)#each time the draw method is called, fill the drawing area with BACKGROUND_COLOR

	title = draw_info.LARGE_FONT.render(f"{algo_name} - {'Ascending' if ascending else 'Descending'}", 1, draw_info.GREEN)
	draw_info.window.blit(title, (draw_info.width/2 - title.get_width()/2 , 5))

	controls = draw_info.FONT.render("R - Reset | SPACE - Start Sorting | A - Ascending | D - Descending", 1, draw_info.BLACK)
	draw_info.window.blit(controls, (draw_info.width/2 - controls.get_width()/2 , 45))

	sorting = draw_info.FONT.render("I - Insertion Sort | B - Bubble Sort", 1, draw_info.BLACK)
	draw_info.window.blit(sorting, (draw_info.width/2 - sorting.get_width()/2 , 75))

	draw_list(draw_info)
	pygame.display.update() #update the display area 


def draw_list(draw_info, color_positions={}, clear_bg=False):
	lst = draw_info.lst #redefining lst so that we dont have to use draw_info.lst again and again

	if clear_bg:
		clear_rect = (draw_info.SIDE_PAD//2, draw_info.TOP_PAD, 
						draw_info.width - draw_info.SIDE_PAD, draw_info.height - draw_info.TOP_PAD)
		pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect)

	for i, val in enumerate(lst):
	# enumerate(lst) is a function which returns index-value pairs while iterating through the list
		x = draw_info.start_x + i * draw_info.block_width
		y = draw_info.height - (val - draw_info.min_val) * draw_info.block_height

		color = draw_info.GRADIENTS[i % 3] #to pick one of three shades of grey

		if i in color_positions:
			color = color_positions[i] 

		pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, draw_info.height))
		# this is a STL from pygame that allows us to draw rectangle in any specific display window
		# pygame.draw.rect(window object, color, (x&y coordinate of top left corner of your rectangle, width, height))	the rectangle is drawn from top-left to bottom-right
	if clear_bg:
		pygame.display.update()


def generate_starting_list(n, min_val, max_val):
	#this method generates a list. the for loop fills the list lst with n random integers between (min_val, max_val) inclusive
	lst = []

	for _ in range(n):
	# here underscore (_) is used as a variable. to read further on uses if (_) go to datacamp.com/tutorial/role-underscore-python
		val = random.randint(min_val, max_val)
		lst.append(val)

	return lst


def bubble_sort(draw_info, ascending=True):
	lst = draw_info.lst

	for i in range(len(lst) - 1):
		for j in range(len(lst) - 1 - i):
			num1 = lst[j]
			num2 = lst[j + 1]

			if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
				lst[j], lst[j + 1] = lst[j + 1], lst[j]
				draw_list(draw_info, {j: draw_info.GREEN, j + 1: draw_info.RED}, True)
				yield True

	return lst

def insertion_sort(draw_info, ascending=True):
	lst = draw_info.lst

	for i in range(1, len(lst)):
		current = lst[i]

		while True:
			ascending_sort = i > 0 and lst[i - 1] > current and ascending
			descending_sort = i > 0 and lst[i - 1] < current and not ascending

			if not ascending_sort and not descending_sort:
				break

			lst[i] = lst[i - 1]
			i = i - 1
			lst[i] = current
			draw_list(draw_info, {i - 1: draw_info.GREEN, i: draw_info.RED}, True)
			yield True

	return lst


def main():
	#this is the main event loop of our pygame program
	run = True
	clock = pygame.time.Clock()#this creates an object named clock. It uses STL from pygame and the object has many attributes and funtions that allow us to control how/"in what time" our program will run

	n = 50
	min_val = 0
	max_val = 100

	lst = generate_starting_list(n, min_val, max_val)# generate the list
	draw_info = DrawInformation(800, 600, lst)# call the constructor of DrawInformation
	sorting = False
	ascending = True

	sorting_algorithm = bubble_sort
	sorting_algo_name = "Bubble Sort"
	sorting_algorithm_generator = None

	while run:
		# we need our pygame window to keep running until the variable run==true
		clock.tick(60)#this ensures that our while loop runs at 60 times per sec

		if sorting:
			try:
				next(sorting_algorithm_generator)
			except StopIteration:
				sorting = False
		else:
			draw(draw_info, sorting_algo_name, ascending)

		for event in pygame.event.get():
			# every input to the computer from ceyboard or mouse is recorded (begining from the initialization of pygame) and is stored in a queue.
			# pygame.event.get() returns the quque filled with all those events (oldest first)
			if event.type == pygame.QUIT:
				run = False
			# if at any event, the input is to quit then quit
			if event.type != pygame.KEYDOWN:
				continue
			#  if the event is not a keyboard button press(as event queue has recorded all cursor movements also)
			if event.key == pygame.K_r:
			#  if the event is a keyboard button press and is equal to r then reset the list
			#  executing this reset function is not dependent on the var sorting. this means that we can pause the sorting-animation in the middle if r is pressed and reset the list
				lst = generate_starting_list(n, min_val, max_val)
				draw_info.set_list(lst)
				sorting = False
			elif event.key == pygame.K_SPACE and sorting == False:
			# if SPACE and not already sorting, start sorting
				sorting = True
			# this variable "sorting" is used to atomize the animation/sorting process. ie - dont update any variable or take action on any input as long as the sorting is set to true
				sorting_algorithm_generator = sorting_algorithm(draw_info, ascending)
			elif event.key == pygame.K_a and not sorting:
				ascending = True
			elif event.key == pygame.K_d and not sorting:
				ascending = False
			elif event.key == pygame.K_i and not sorting:
				sorting_algorithm = insertion_sort
			# set the variable sorting_algorithm to insertion sort. this variable can be updated again before we encounter an event of SPACE
				sorting_algo_name = "Insertion Sort"
			elif event.key == pygame.K_b and not sorting:
				sorting_algorithm = bubble_sort
				sorting_algo_name = "Bubble Sort"


	pygame.quit()


if __name__ == "__main__":
	main()
