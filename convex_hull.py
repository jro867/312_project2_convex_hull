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

	def merge(self, left_pol, right_pol):

		# farthest_left = right_pol[len(right_pol)-1]
		# print('farther left: ', farthest_left)
		#
		# farthest_right = left_pol[len(left_pol)-1]
		# print('farther right: ', farthest_right)
		print()
		print('left_pol: ', left_pol)
		print()
		print()
		print('right_pol: ', right_pol)
		print()

		# stop = 0
		#
		good_one = 0
		stop = 0
		stop2 = 0
		left_index = len(left_pol)-1
		right_index = 0

		farthest_right = left_pol[left_index]
		farthest_left = right_pol[right_index]
		print()
		print('farthes right: ', farthest_right)
		print('farthes left: ', farthest_left)
		print()
		while stop != 5:
			stop+=1
			print('looking at: ', left_pol[left_index % len(left_pol)])
			left_index -=1

			while stop2 != 5:
				stop2+=1
				print('looking at right: ', right_pol[right_index % len(right_pol)])
				right_index +=1



		#While the edge is not upper tangent to both left and right
		#While the edge is not upper tangent to the left, move counter-clockwise to the next point on the left hull
		#Hint: We want to move to the next point(s) on the left hull as long as the slope decreases
		#While the edge is not upper tangent to the right, move clockwise to the next point on the right hull


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

				if x == 0 and y == 0 : continue
				if x == 0 :
					slope = 0
				else:
					slope = y/x

				if self.debug and self.verbose : print('slope value: ', slope)
				if slope > largest_slope:
					larger_slope = slope

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
			sorted_list = self.sort_based_on_slope(sorted_list)
			if self.debug : self.draw_lines(sorted_list)
			return sorted_list





			# polygon = [QLineF(sorted_list[i],sorted_list[(i+1)%9]) for i in range(9)]
			# assert( type(polygon) == list and type(polygon[0]) == QLineF )


			# self.view.clearPoints()
			# self.view.clearLines()
			# self.view.addPoints( self.points, (0,0,0) )
			#
			# for i in range(10):
			# 	print('justlik them')
			# 	myline = [QLineF(sorted_list[i],sorted_list[(i+1)%10])]
			# 	self.view.addLines(myline,(255,0,0))



			# self.show_hull.emit(polygon,(255,0,0))
			# return sorted_list

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



		# print()
		# print()
		# print('FIRST HALF BR:', first_half)
		# print()
		# print()
		# print('second HALF BR', second_half)
		#
		# merged_array = first_half + second_half
		#
		# print('merged Array: ', merged_array)

		# # polygon = [QLineF(first_half[0], second_half[0])]
		# # print('polygon: ', polygon)
		# print()
		# print()
		# print('How many yimes does this happen:')
		# # print('second_half', second_half)
		# # assert( type(polygon) == list and type(polygon[0]) == QLineF )
		# # self.show_hull.emit(polygon,(255,0,0))
		#
		#
		# #return merge(left, right)

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
		self.points = [QPointF(0.4, 0.1),QPointF(0.8, 0.10),QPointF(0.5, 0.9),QPointF(0.3, 0.2),QPointF(0.7, 0.4),QPointF(0.2, 0.8),QPointF(0, 0.9),QPointF(0.6, 0.8),QPointF(0.1, 0.5),QPointF(0.9, 0.9)]

		#case: 4 points
		#self.points = [QPointF(0.4, 0.1),QPointF(0.8, 0.10),QPointF(0.5, 0.9), QPointF(0.7, 0.63)]

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

		# USE_DUMMY = False
		# if USE_DUMMY:
		# 	# this is a dummy polygon of the first 3 unsorted points
		# 	polygon = [QLineF(self.points[i],self.points[(i+1)%3]) for i in range(3)]
		#
		# 	# when passing lines to the display, pass a list of QLineF objects.  Each QLineF
		# 	# object can be created with two QPointF objects corresponding to the endpoints
		# 	assert( type(polygon) == list and type(polygon[0]) == QLineF )
		# 	# send a signal to the GUI thread with the hull and its color
		# 	self.show_hull.emit(polygon,(255,0,0))
		#
		# else:
		# 	# TODO: PASS THE CONVEX HULL LINES BACK TO THE GUI FOR DISPLAY
		# 	pass

		# send a signal to the GUI thread with the time used to compute the hull
		self.display_text.emit('Time Elapsed (Convex Hull): {:3.3f} sec'.format(t4-t3))
		print('Time Elapsed (Convex Hull): {:3.3f} sec'.format(t4-t3))
