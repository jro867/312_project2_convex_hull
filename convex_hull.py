#!/usr/bin/python3
# why the shebang here, when it's imported?  Can't really be used stand alone, right?  And fermat.py didn't have one...
# this is 4-5 seconds slower on 1000000 points than Ryan's desktop...  Why?


from which_pyqt import PYQT_VER
if PYQT_VER == 'PYQT5':
	from PyQt5.QtCore import QLineF, QPointF, QThread, pyqtSignal
elif PYQT_VER == 'PYQT4':
	from PyQt4.QtCore import QLineF, QPointF, QThread, pyqtSignal
else:
	raise Exception('Unsupported Version of PyQt: {}'.format(PYQT_VER))



import time
import math



class ConvexHullSolverThread(QThread):
	def __init__( self, unsorted_points,demo, view):
		self.points = unsorted_points
		self.pause = demo
		self.view = view
		QThread.__init__(self)

	def __del__(self):
		self.wait()

	def point_sorting(self, point):
		# print('X value: ', point.x())
		return point.x()

	show_hull = pyqtSignal(list,tuple)
	display_text = pyqtSignal(str)

# some additional thread signals you can implement and use for debugging, if you like
	show_tangent = pyqtSignal(list,tuple)
	erase_hull = pyqtSignal(list)
	erase_tangent = pyqtSignal(list)
	debug = True
	verbose = False

	def find_upper(self, found, counter, pivot, list_of_points, looping_direction, slope_direction) :

		initial_index = 0
		initial_slope = 0
		point_to_compare_to = 0

		print('LOOKING AT DIRECTION: ', looping_direction)



		if looping_direction == 'left' :
			initial_slope = 1000
			initial_index = list_of_points.index(list_of_points[len(sorted(list_of_points, key=self.point_sorting))-1])
			# sorted_left_polygon = sorted(left_pol, key=self.point_sorting)
			# most_left_point = sorted_left_polygon[len(sorted_left_polygon)-1]
			# starting_left_point = left_pol.index(most_left_point)
		else :
			initial_index += counter

		while not found:
			# right_point = right_pol[right_index % len(right_pol)]
			point_to_compare_to = list_of_points[initial_index % len(list_of_points)]
			print('looking at to compare: ', point_to_compare_to)

			slope = self.calculate_slope(pivot, point_to_compare_to)

			print('pivot ', pivot)
			print('to compare to ', point_to_compare_to)

			attempted_line = [QLineF(pivot,point_to_compare_to)]
			self.view.addLines(attempted_line,(51,76,255))

			print('temp upper slope: ', slope)
			print('upper slope', initial_slope)

			print('increase: ', slope_direction == 'increase')
			print()
			print('decresed: ', slope_direction == 'decreased')
			print(slope_direction)
			print()
			print()

			if (slope > initial_slope and slope_direction == 'increase') or (slope < initial_slope and slope_direction == 'decreased') :
				initial_slope = slope
				print('found final slope: ', initial_slope)
				#check for the next one, if next one is bigger then keep going otherwise quit
				print()
				print('current index: ', initial_index)
				print('in: ', list_of_points)
				print()
				if looping_direction == 'left' :
					next_index = initial_index-1
				else :
					next_index = initial_index+1

				print('different index: ', next_index)
				print()
				print()
				print('can you do that: ', list_of_points[next_index % len(list_of_points)])
				slope = self.calculate_slope(pivot, list_of_points[next_index % len(list_of_points)])
				print('second slope: ', slope)

				if (slope > initial_slope and slope_direction == 'increase') or (slope < initial_slope and slope_direction == 'decreased') :
					if (looping_direction == 'right') :
						initial_index +=1
					else :
						initial_index -=1
				else :
					found = True
					attempted_line = [QLineF(pivot,point_to_compare_to)]
					self.view.addLines(attempted_line,(0,0,0))
				#draw the line with different Color
			# else :
				#draw the same line than before with a different color??? DO I NEED TO DELETE THE OTHER ONE FIZRT??

			if (looping_direction == 'right') :
				initial_index +=1
			else :
				initial_index -=1

		return (found, point_to_compare_to)

	def merge(self, left_pol, right_pol):

		# farthest_left = right_pol[len(right_pol)-1]
		# print('farther left: ', farthest_left)
		#
		# farthest_right = left_pol[len(left_pol)-1]
		# print('farther right: ', farthest_right)
		print('==TOP===')
		print('left_pol: ', left_pol)
		print()
		print()
		print('right_pol: ', right_pol)
		print()

		# stop = 0
		#
		good_one = 0
		upper_slope = 0
		temp_upper_slope = 0
		stop = 0
		stop2 = 0
		#to get this left index you have to sort the array and get the
		sorted_left_polygon = sorted(left_pol, key=self.point_sorting)
		most_left_point = sorted_left_polygon[len(sorted_left_polygon)-1]
		starting_left_point = left_pol.index(most_left_point)

		if self.debug and self.verbose :
			print('SORTED POINTS FOR LEFTED POINT: ', sorted_left_polygon)
			print('POINT___: ', most_left_point)
			print('Index of left most point: ', starting_left_point)
			print()
			print()

		# left_index = len(left_pol)-1
		left_index = starting_left_point
		right_index = 0

		# farthest_right = left_pol[left_index]
		farthest_right = left_pol[starting_left_point]#THIS IS A DUPLICATED starting_left_point
		farthest_left = right_pol[right_index]

		found_upper = False
		found_lower = False

		final_pivot_left = 0
		final_pivot_right = 0
		balance = 0

		print()
		print('0000000000 MERGING 00000000000000000000000000000')


		print('farthes right: ', farthest_right)
		print('farthes left: ', farthest_left)
		print()
		while stop != 1:
		# while not found_upper:
			stop+=1

			left_point = left_pol[left_index % len(left_pol)]
			print('looking at: ', left_point)
			left_index -=1

			left_upper_tangent = False
			right_upper_tangent = False
			counter = 0

			while balance != 2 :

				(left_upper_tangent, pivot_left) = self.find_upper(False, counter, left_point, right_pol, 'right', 'increase') #save pivots and compare when they came back if they are the same we are done
				(right_upper_tangent, pivot_right) = self.find_upper(False, counter, pivot_left, left_pol, 'left', 'decreased')
				print('whats looking at now: ', pivot_right)
				if (final_pivot_left == pivot_left) and (final_pivot_right == pivot_right) :
					balance +=1
					print('was balance so far: ', balance)

				final_pivot_left = pivot_left
				final_pivot_right = pivot_right
				left_point = pivot_right
				counter += 1
				print('now counter: ', counter)

			# # while stop2 != 3:
			# while not found_upper:
			# 	stop2+=1
			# 	right_point = right_pol[right_index % len(right_pol)]
			# 	print('looking at right: ', right_point)
			#
			# 	temp_upper_slope = self.calculate_slope(left_point, right_point)
			#
			# 	print('create line with left point: ', left_point)
			# 	print('create line with right point: ', right_point)
			# 	attempted_line = [QLineF(left_point,right_point)]
			# 	self.view.addLines(attempted_line,(51,76,255))
			#
			# 	print('temp upper slope: ', temp_upper_slope)
			# 	print('upper slope', upper_slope)
			#
			# 	if temp_upper_slope > upper_slope :
			# 		upper_slope = temp_upper_slope
			# 		print('found final slope: ', upper_slope)
			# 		#check for the next one, if next one is bigger then keep going otherwise quit
			# 		print()
			# 		print('current index: ', right_index)
			# 		print('in: ', right_pol)
			# 		print()
			# 		different_index = right_index+1
			# 		print('different index: ', different_index)
			# 		print()
			# 		print()
			# 		print('can you do that: ', right_pol[different_index % len(right_pol)])
			# 		second_temp_upper_slope = self.calculate_slope(left_point, right_pol[different_index % len(right_pol)])
			# 		print('second slope: ', second_temp_upper_slope)
			#
			# 		if second_temp_upper_slope > upper_slope :
			# 			right_index +=1
			# 		else :
			# 			found_upper = True
			# 			found_lower = True
			# 			attempted_line = [QLineF(left_point,right_point)]
			# 			self.view.addLines(attempted_line,(0,0,0))
			# 		#draw the line with different Color
			# 	# else :
			# 		#draw the same line than before with a different color??? DO I NEED TO DELETE THE OTHER ONE FIZRT??
			#
			# 	right_index +=1


	# def merge(self, left_pol, right_pol):
	#
	# 	# farthest_left = right_pol[len(right_pol)-1]
	# 	# print('farther left: ', farthest_left)
	# 	#
	# 	# farthest_right = left_pol[len(left_pol)-1]
	# 	# print('farther right: ', farthest_right)
	# 	print('==TOP===')
	# 	print('left_pol: ', left_pol)
	# 	print()
	# 	print()
	# 	print('right_pol: ', right_pol)
	# 	print()
	#
	# 	# stop = 0
	# 	#
	# 	good_one = 0
	# 	upper_slope = 0
	# 	temp_upper_slope = 0
	# 	stop = 0
	# 	stop2 = 0
	# 	#to get this left index you have to sort the array and get the
	# 	sorted_left_polygon = sorted(left_pol, key=self.point_sorting)
	# 	most_left_point = sorted_left_polygon[len(sorted_left_polygon)-1]
	# 	starting_left_point = left_pol.index(most_left_point)
	#
	# 	if self.debug and self.verbose :
	# 		print('SORTED POINTS FOR LEFTED POINT: ', sorted_left_polygon)
	# 		print('POINT___: ', most_left_point)
	# 		print('Index of left most point: ', starting_left_point)
	# 		print()
	# 		print()
	#
	# 	# left_index = len(left_pol)-1
	# 	left_index = starting_left_point
	# 	right_index = 0
	#
	# 	# farthest_right = left_pol[left_index]
	# 	farthest_right = left_pol[starting_left_point]#THIS IS A DUPLICATED starting_left_point
	# 	farthest_left = right_pol[right_index]
	#
	# 	found_upper = False
	# 	found_lower = False
	#
	# 	print()
	# 	print('farthes right: ', farthest_right)
	# 	print('farthes left: ', farthest_left)
	# 	print()
	# 	# while stop != 5:
	# 	while not found_upper:
	# 		# stop+=1
	#
	# 		left_point = left_pol[left_index % len(left_pol)]
	# 		print('looking at: ', left_point)
	# 		left_index -=1
	#
	# 		# while stop2 != 3:
	# 		while not found_upper:
	# 			stop2+=1
	# 			right_point = right_pol[right_index % len(right_pol)]
	# 			print('looking at right: ', right_point)
	#
	# 			temp_upper_slope = self.calculate_slope(left_point, right_point)
	#
	# 			print('create line with left point: ', left_point)
	# 			print('create line with right point: ', right_point)
	# 			attempted_line = [QLineF(left_point,right_point)]
	# 			self.view.addLines(attempted_line,(51,76,255))
	#
	# 			print('temp upper slope: ', temp_upper_slope)
	# 			print('upper slope', upper_slope)
	#
	# 			if temp_upper_slope > upper_slope :
	# 				upper_slope = temp_upper_slope
	# 				print('found final slope: ', upper_slope)
	# 				#check for the next one, if next one is bigger then keep going otherwise quit
	# 				print()
	# 				print('current index: ', right_index)
	# 				print('in: ', right_pol)
	# 				print()
	# 				different_index = right_index+1
	# 				print('different index: ', different_index)
	# 				print()
	# 				print()
	# 				print('can you do that: ', right_pol[different_index % len(right_pol)])
	# 				second_temp_upper_slope = self.calculate_slope(left_point, right_pol[different_index % len(right_pol)])
	# 				print('second slope: ', second_temp_upper_slope)
	#
	# 				if second_temp_upper_slope > upper_slope :
	# 					right_index +=1
	# 				else :
	# 					found_upper = True
	# 					found_lower = True
	# 					attempted_line = [QLineF(left_point,right_point)]
	# 					self.view.addLines(attempted_line,(0,0,0))
	# 				#draw the line with different Color
	# 			# else :
	# 				#draw the same line than before with a different color??? DO I NEED TO DELETE THE OTHER ONE FIZRT??
	#
	# 			right_index +=1



		#While the edge is not upper tangent to both left and right
		#While the edge is not upper tangent to the left, move counter-clockwise to the next point on the left hull
		#Hint: We want to move to the next point(s) on the left hull as long as the slope decreases
		#While the edge is not upper tangent to the right, move clockwise to the next point on the right hull
	def calculate_slope(self, left_point, right_point) :

		print()
		print('calculating slope::: ')
		print('left point: ', left_point)
		print('right point: ', right_point)
		print()
		x = left_point.x() - right_point.x()
		y = left_point.y() - right_point.y()

		if x == 0 or y == 0 :
			return 0
		else:
			return y/x


	def sort_based_on_slope(self, list_point):

		largest_slope = -1000
		length = len(list_point)
		if length == 2: return list_point

		if self.debug and self.verbose :
			print("\n==== SORTING BASED ON SLOPE =====")
			print()
			print()

		for i in range(length):

			if i != 0:
				if self.debug and self.verbose : print('>> i << ==> ', i)
				# print(list_point[0], list_point[(i+1) % length])
				x = list_point[0].x() - list_point[i].x()
				y = list_point[0].y() - list_point[i].y()

				print('first point: ', list_point[0])
				print('VS: ')
				print('next one" ', list_point[i])
				print()
				print('x: ', x)
				print('y: ', y)

				if x == 0 and y == 0 : continue
				if x == 0 :
					slope = 0
				else:
					slope = y/x

				if self.debug and self.verbose : print('slope value: ', slope)
				if slope > largest_slope:
					print('largest slope was: ', largest_slope)
					largest_slope = slope


					if i > 1:
						larger_slope = list_point[i]
						smaller_slope = list_point[i-1]
						list_point[i-1] = larger_slope
						list_point[i] = smaller_slope

		if self.debug and self.verbose :
			print()
			print('List of POINTS AFTER sorting: ', list_point)
			print('====       =====')
			print()
			print()

		return list_point

	def draw_lines(self, points):

		for i in range(len(points)):
			myline = [QLineF(points[i],points[(i+1)%len(points)])]
			self.view.addLines(myline,(255,0,0))

	'''
	─┼─┼─╔╦╗┬┬  ┬┬┌┬┐┌─┐  ┌─┐┌┐┌┌┬┐  ┌─┐┌─┐┌┐┌┌─┐ ┬ ┬┌─┐┬─┐
	─┼─┼─ ║║│└┐┌┘│ ││├┤   ├─┤│││ ││  │  │ │││││─┼┐│ │├┤ ├┬┘
     	 ═╩╝┴ └┘ ┴─┴┘└─┘  ┴ ┴┘└┘─┴┘  └─┘└─┘┘└┘└─┘└└─┘└─┘┴└─

	'''

	def divide_and_conquer(self, sorted_list):

		if self.debug : self.view.addPoints( self.points, (0,0,0) )

		length = len(sorted_list)
		if length <= 3 :
			print()
			print("chunk received: ", sorted_list)
			sorted_list = self.sort_based_on_slope(sorted_list)
			print("chunk leaving: ", sorted_list)
			print()
			print()
			if self.debug : self.draw_lines(sorted_list)
			return sorted_list


		middle_index = math.ceil(length/2)
		# print('middle index:: ', middle_index)
		first_half,second_half=sorted_list[:middle_index],sorted_list[middle_index:]
		#
		#

		first_half = self.divide_and_conquer(first_half)
		second_half = self.divide_and_conquer(second_half)

		if self.debug and self.verbose :
			print('first_half coming back: ', first_half)
			print()
			print('second_half coming back: ', second_half)


		self.merge(first_half, second_half)
		merge = first_half + second_half
		return merge


	def run( self):

		assert( type(self.points) == list and type(self.points[0]) == QPointF )
		n = len(self.points)
		print( 'Computing Hull for set of {} points'.format(n) )

		t1 = time.time()

		'''
		─┼─┼─╔╦╗┌─┐┌┐┌┬ ┬┌─┐┬    ┌┬┐┌─┐┌─┐┌┬┐┬┌┐┌┌─┐
		─┼─┼─║║║├─┤││││ │├─┤│     │ ├┤ └─┐ │ │││││ ┬
     		 ╩ ╩┴ ┴┘└┘└─┘┴ ┴┴─┘   ┴ └─┘└─┘ ┴ ┴┘└┘└─┘
		'''

		#case: 10 points user friendly
		# self.points = [QPointF(0.4, 0.1),QPointF(0.8, 0.10),QPointF(0.5, 0.9),QPointF(0.3, 0.2),QPointF(0.7, 0.4),QPointF(0.2, 0.8),QPointF(0, 0.9),QPointF(0.6, 0.8),QPointF(0.1, 0.5),QPointF(0.9, 0.9)]

		#case: 4 points
		# self.points = [QPointF(0.4, 0.1),QPointF(0.8, 0.10),QPointF(0.5, 0.9), QPointF(0.7, 0.63)]

		#case: 6 poinys
		# self.points = [QPointF(0.4, 0.1),QPointF(0.8, 0.10),QPointF(0.5, 0.9),QPointF(0.3, 0.2),QPointF(0.7, 0.4),QPointF(0.2, 0.8)]
		# self.points = [QPointF(0.4, 0.1),QPointF(0.8, 0.10),QPointF(0.5, 0.9),QPointF(0.3, 0.2),QPointF(0.7, 0.4),QPointF(0.2, 0.8),QPointF(0.6, 0.96)]
		self.points = [QPointF(0.4, 0.1),QPointF(0.8, 0.10),QPointF(0.5, 0.8),QPointF(0.3, 0.2),QPointF(0.2, 0.8),QPointF(0.6, 0.96)]
		# self.points = [QPointF(0.4, 0.1),QPointF(0.8, 0.10),QPointF(0.5, 0.9),QPointF(0.3, 0.2),QPointF(0.7, 0.4),QPointF(0.2, 0.8),QPointF(0, 0.9)]

		#case: Base case with no sorting needed
		# self.points = [QPointF(0.4, 0.1),QPointF(0.8, 0.10),QPointF(0.5, 0.9)]

		#case: Needs to be sorted because of the slope
		# self.points = [QPointF(0.4, 0.1),QPointF(0.8, 0.10),QPointF(0.5, -0.3)]

		#case: Just two points
		# self.points = [QPointF(0.4, 0.1),QPointF(0.8, 0.10)]

		# self.points = [QPointF(-0.43632431120059234, 0.5116084083144479),QPointF(-0.37970486136133474, 0.4596634965202573), QPointF(-0.15885683833831, -0.4821664994140733),QPointF(-0.04680609169528838, 0.1667640789100624),QPointF(0.02254944273721704, -0.19013172509917142), QPointF(0.23673799335066326, -0.4989873172751189), QPointF(0.5675971780695452, -0.3933745478421451), QPointF(0.6888437030500962, 0.515908805880605), QPointF(0.797676575935987,0.36796786383088254),QPointF(0.8162257703906703,0.009373711634780513)]
		# print('O points: ', self.points)
		'''
		================================================
		'''

		sorted_points = sorted(self.points, key=self.point_sorting)
		if self.debug and self.verbose :
			print('SORTED POINTS: ', sorted_points)
			print()
			print()

		t2 = time.time()
		print('Time Elapsed (Sorting): {:3.3f} sec'.format(t2-t1))

		t3 = time.time()

		if self.debug:
			self.view.clearPoints()
			self.view.clearLines()

		self.divide_and_conquer(sorted_points)
		t4 = time.time()

		# send a signal to the GUI thread with the time used to compute the hull
		self.display_text.emit('Time Elapsed (Convex Hull): {:3.3f} sec'.format(t4-t3))
		print('Time Elapsed (Convex Hull): {:3.3f} sec'.format(t4-t3))
