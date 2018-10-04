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

	def sort_based_on_slope(self, list_point):

		largest_slope = 0
		second_place = 'none'
		length = len(list_point)

		for i in range(length):
			print('i:',i)
			x1 = list_point[0].x()
			x2 = list_point[(i+1) % length].x()
			y1 = list_point[0].y()
			y2 = list_point[(i+1) % length].y()

			print(list_point[0], list_point[(i+1) % length])
			# print('y', list_point[0].y() - list_point[(i+1) % length].y())
			# print('x', list_point[0].x() - list_point[(i+1) % length].x())

			x = x1-x2
			y = y1-y2

			if x == 0 and y == 0 : continue
			slope = x/y
			# slope = (list_point[0].y() - list_point[(i+1) % length].y())/(list_point[0].x() - list_point[(i+1) % length].x())
			print('slope: ', slope)
			return list_point



	def find_using_divide_and_conquer_strategy(self, sorted_list):

		length = len(sorted_list)
		if length <= 12 :
			print('less than three: ', sorted_list)
			# sorted_list = self.sort_based_on_slope(sorted_list)


			# polygon = [QLineF(sorted_list[i],sorted_list[(i+1)%9]) for i in range(9)]
			# assert( type(polygon) == list and type(polygon[0]) == QLineF )


			self.view.clearPoints()
			self.view.clearLines()
			self.view.addPoints( self.points, (0,0,0) )

			for i in range(10):
				print('justlik them')
				myline = [QLineF(sorted_list[i],sorted_list[(i+1)%10])]
				self.view.addLines(myline,(255,0,0))
			# self.show_hull.emit(polygon,(255,0,0))
			# return sorted_list

		# middle_index = math.ceil(length/2)
		# print('middle index:: ', middle_index)
		# first_half,second_half=sorted_list[:middle_index],sorted_list[middle_index:]
		#
		#
		# first_half = self.find_using_divide_and_conquer_strategy(first_half)
		# second_half = self.find_using_divide_and_conquer_strategy(second_half)
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

		# self.points = [QPointF(4, 1),QPointF(6, 10),QPointF(5, 9)]
		# self.points = [QPointF(4, 1),QPointF(8, 10),QPointF(5, 9),QPointF(3, 2),QPointF(7, 4),QPointF(2, 8),QPointF(0, 9),QPointF(6, 8),QPointF(1, 5),QPointF(9, 9)]
		self.points = [QPointF(0.4, 0.1),QPointF(0.8, 0.10),QPointF(0.5, 0.9),QPointF(0.3, 0.2),QPointF(0.7, 0.4),QPointF(0.2, 0.8),QPointF(0, 0.9),QPointF(0.6, 0.8),QPointF(0.1, 0.5),QPointF(0.9, 0.9)]
		# self.points = [QPointF(-0.43632431120059234, 0.5116084083144479),QPointF(-0.37970486136133474, 0.4596634965202573), QPointF(-0.15885683833831, -0.4821664994140733),QPointF(-0.04680609169528838, 0.1667640789100624),QPointF(0.02254944273721704, -0.19013172509917142), QPointF(0.23673799335066326, -0.4989873172751189), QPointF(0.5675971780695452, -0.3933745478421451), QPointF(0.6888437030500962, 0.515908805880605), QPointF(0.797676575935987,0.36796786383088254),QPointF(0.8162257703906703,0.009373711634780513)]
		# print('O points: ', self.points)

		sorted_points = sorted(self.points, key=self.point_sorting)
		print('sorted points: ', sorted_points)
		t2 = time.time()
		print('Time Elapsed (Sorting): {:3.3f} sec'.format(t2-t1))

		t3 = time.time()
		# TODO: COMPUTE THE CONVEX HULL USING DIVIDE AND CONQUER
		self.find_using_divide_and_conquer_strategy(sorted_points)
		t4 = time.time()
		print("running...")
		USE_DUMMY = False
		if USE_DUMMY:
			# this is a dummy polygon of the first 3 unsorted points
			polygon = [QLineF(self.points[i],self.points[(i+1)%3]) for i in range(3)]

			# when passing lines to the display, pass a list of QLineF objects.  Each QLineF
			# object can be created with two QPointF objects corresponding to the endpoints
			assert( type(polygon) == list and type(polygon[0]) == QLineF )
			# send a signal to the GUI thread with the hull and its color
			self.show_hull.emit(polygon,(255,0,0))

		else:
			# TODO: PASS THE CONVEX HULL LINES BACK TO THE GUI FOR DISPLAY
			pass

		# send a signal to the GUI thread with the time used to compute the hull
		self.display_text.emit('Time Elapsed (Convex Hull): {:3.3f} sec'.format(t4-t3))
		print('Time Elapsed (Convex Hull): {:3.3f} sec'.format(t4-t3))
