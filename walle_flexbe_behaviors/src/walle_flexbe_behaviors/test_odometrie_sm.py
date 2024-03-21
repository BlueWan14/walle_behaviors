#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from flexbe_states.calculation_state import CalculationState
from flexbe_states.log_key_state import LogKeyState
from flexbe_states.subscriber_state import SubscriberState
from walle_flexbe_states.PIF_move_state import PIF_MoveState
from walle_flexbe_states.compare_condition_state import CompareConditionState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Tue Mar 19 2024
@author: Erwan MAWART
'''
class test_odometrieSM(Behavior):
	'''
	Test odometrie PIF
	'''


	def __init__(self):
		super(test_odometrieSM, self).__init__()
		self.name = 'test_odometrie'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		topic_odometry = "/odometry/filtered_map"
		add_dist = 0.002
		add_rot = 1.5707
		# x:757 y:227
		_state_machine = OperatableStateMachine(outcomes=['failed'])
		_state_machine.userdata.i = 0
		_state_machine.userdata.linear = 0.3
		_state_machine.userdata.angular = 0.5
		_state_machine.userdata.zero = 0.0

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:30 y:40
			OperatableStateMachine.add('get pos-rot init',
										SubscriberState(topic=topic_odometry, blocking=True, clear=False),
										transitions={'received': 'init value x', 'unavailable': 'failed'},
										autonomy={'received': Autonomy.Off, 'unavailable': Autonomy.Off},
										remapping={'message': 'message'})

			# x:1011 y:210
			OperatableStateMachine.add('check position y',
										CompareConditionState(),
										transitions={'value_1': 'set new value y', 'value_2': 'get position linear', 'failed': 'failed'},
										autonomy={'value_1': Autonomy.Off, 'value_2': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'value_1': 'posY', 'value_2': 'y'})

			# x:1076 y:302
			OperatableStateMachine.add('check position z',
										CompareConditionState(),
										transitions={'value_1': 'set new value z', 'value_2': 'get position angular', 'failed': 'failed'},
										autonomy={'value_1': Autonomy.Off, 'value_2': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'value_1': 'posZ', 'value_2': 'z'})

			# x:240 y:174
			OperatableStateMachine.add('forward',
										PIF_MoveState(),
										transitions={'done': 'get position linear'},
										autonomy={'done': Autonomy.Off},
										remapping={'linear': 'linear', 'angular': 'zero'})

			# x:1449 y:218
			OperatableStateMachine.add('get position angular',
										SubscriberState(topic=topic_odometry, blocking=True, clear=False),
										transitions={'received': 'set value z', 'unavailable': 'failed'},
										autonomy={'received': Autonomy.Off, 'unavailable': Autonomy.Off},
										remapping={'message': 'message_angular'})

			# x:346 y:68
			OperatableStateMachine.add('get position linear',
										SubscriberState(topic=topic_odometry, blocking=True, clear=False),
										transitions={'received': 'set value x', 'unavailable': 'failed'},
										autonomy={'received': Autonomy.Off, 'unavailable': Autonomy.Off},
										remapping={'message': 'message_linear'})

			# x:30 y:117
			OperatableStateMachine.add('init value x',
										CalculationState(calculation=lambda p: p.pose.pose.position.x),
										transitions={'done': 'init value y'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'message', 'output_value': 'x'})

			# x:30 y:194
			OperatableStateMachine.add('init value y',
										CalculationState(calculation=lambda p: p.pose.pose.position.y),
										transitions={'done': 'init value z'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'message', 'output_value': 'y'})

			# x:30 y:271
			OperatableStateMachine.add('init value z',
										CalculationState(calculation=lambda p: p.pose.pose.orientation.z),
										transitions={'done': 'forward'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'message', 'output_value': 'z'})

			# x:631 y:318
			OperatableStateMachine.add('nombre cycle',
										CalculationState(calculation=lambda x: (x+1)/4),
										transitions={'done': 'print'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'i', 'output_value': 'i'})

			# x:413 y:232
			OperatableStateMachine.add('print',
										LogKeyState(text='nombre de tours: {}', severity=Logger.REPORT_HINT),
										transitions={'done': 'forward'},
										autonomy={'done': Autonomy.Off},
										remapping={'data': 'i'})

			# x:1170 y:31
			OperatableStateMachine.add('set new value x',
										CalculationState(calculation=lambda x: x+add_dist),
										transitions={'done': 'stop linear'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'posX', 'output_value': 'x'})

			# x:1253 y:136
			OperatableStateMachine.add('set new value y',
										CalculationState(calculation=lambda y: y+add_dist),
										transitions={'done': 'stop linear'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'posY', 'output_value': 'y'})

			# x:805 y:365
			OperatableStateMachine.add('set new value z',
										CalculationState(calculation=lambda z: z-add_rot),
										transitions={'done': 'nombre cycle'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'posZ', 'output_value': 'z'})

			# x:568 y:18
			OperatableStateMachine.add('set value x',
										CalculationState(calculation=lambda p: p.pose.pose.position.x),
										transitions={'done': 'check position x'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'message_linear', 'output_value': 'posX'})

			# x:842 y:113
			OperatableStateMachine.add('set value y',
										CalculationState(calculation=lambda p: p.pose.pose.position.y),
										transitions={'done': 'check position y'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'message_linear', 'output_value': 'posY'})

			# x:1296 y:352
			OperatableStateMachine.add('set value z',
										CalculationState(calculation=lambda p: p.pose.pose.orientation.z),
										transitions={'done': 'check position z'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'message_angular', 'output_value': 'posZ'})

			# x:1478 y:60
			OperatableStateMachine.add('stop linear',
										PIF_MoveState(),
										transitions={'done': 'turn'},
										autonomy={'done': Autonomy.Off},
										remapping={'linear': 'zero', 'angular': 'zero'})

			# x:1682 y:143
			OperatableStateMachine.add('turn',
										PIF_MoveState(),
										transitions={'done': 'get position angular'},
										autonomy={'done': Autonomy.Off},
										remapping={'linear': 'zero', 'angular': 'angular'})

			# x:782 y:23
			OperatableStateMachine.add('check position x',
										CompareConditionState(),
										transitions={'value_1': 'set new value x', 'value_2': 'set value y', 'failed': 'failed'},
										autonomy={'value_1': Autonomy.Off, 'value_2': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'value_1': 'posX', 'value_2': 'x'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
