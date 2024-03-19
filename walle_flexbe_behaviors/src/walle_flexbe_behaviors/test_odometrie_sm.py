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
		topic_odometry = "/odometry/filtered"
		# x:556 y:329
		_state_machine = OperatableStateMachine(outcomes=['failed'])
		_state_machine.userdata.i = 0
		_state_machine.userdata.linear = 1.0
		_state_machine.userdata.angular = 25.0
		_state_machine.userdata.zero = 0.0
		_state_machine.userdata.x = 0.0
		_state_machine.userdata.y = 0.0
		_state_machine.userdata.z = 0.0

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:40 y:46
			OperatableStateMachine.add('forward',
										PIF_MoveState(),
										transitions={'done': 'get position linear'},
										autonomy={'done': Autonomy.Off},
										remapping={'linear': 'linear', 'angular': 'zero'})

			# x:691 y:231
			OperatableStateMachine.add('check position y',
										CompareConditionState(),
										transitions={'value_1': 'set new value y', 'value_2': 'get position linear', 'failed': 'failed'},
										autonomy={'value_1': Autonomy.Off, 'value_2': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'value_1': 'posY', 'value_2': 'y'})

			# x:716 y:380
			OperatableStateMachine.add('check position z',
										CompareConditionState(),
										transitions={'value_1': 'set new value z', 'value_2': 'get position angular', 'failed': 'failed'},
										autonomy={'value_1': Autonomy.Off, 'value_2': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'value_1': 'posZ', 'value_2': 'z'})

			# x:1107 y:302
			OperatableStateMachine.add('get position angular',
										SubscriberState(topic=topic_odometry, blocking=True, clear=False),
										transitions={'received': 'set value z', 'unavailable': 'failed'},
										autonomy={'received': Autonomy.Off, 'unavailable': Autonomy.Off},
										remapping={'message': 'message_angular'})

			# x:222 y:74
			OperatableStateMachine.add('get position linear',
										SubscriberState(topic=topic_odometry, blocking=True, clear=False),
										transitions={'received': 'set value x', 'unavailable': 'failed'},
										autonomy={'received': Autonomy.Off, 'unavailable': Autonomy.Off},
										remapping={'message': 'message_linear'})

			# x:248 y:278
			OperatableStateMachine.add('nombre cycle',
										CalculationState(calculation=lambda x: (x+1)/4),
										transitions={'done': 'print'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'i', 'output_value': 'i'})

			# x:89 y:170
			OperatableStateMachine.add('print',
										LogKeyState(text='nombre de tours: {}', severity=Logger.REPORT_HINT),
										transitions={'done': 'forward'},
										autonomy={'done': Autonomy.Off},
										remapping={'data': 'i'})

			# x:813 y:28
			OperatableStateMachine.add('set new value x',
										CalculationState(calculation=lambda x: x+1.0),
										transitions={'done': 'stop linear'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'posX', 'output_value': 'x'})

			# x:899 y:154
			OperatableStateMachine.add('set new value y',
										CalculationState(calculation=lambda y: y+1.0),
										transitions={'done': 'stop linear'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'posY', 'output_value': 'y'})

			# x:405 y:388
			OperatableStateMachine.add('set new value z',
										CalculationState(calculation=lambda z: z+90.0),
										transitions={'done': 'nombre cycle'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'posZ', 'output_value': 'z'})

			# x:414 y:15
			OperatableStateMachine.add('set value x',
										CalculationState(calculation=lambda p: p.pos.pos.position.x),
										transitions={'done': 'check position x'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'message_linear', 'output_value': 'posX'})

			# x:666 y:132
			OperatableStateMachine.add('set value y',
										CalculationState(calculation=lambda p: p.pos.pos.position.y),
										transitions={'done': 'check position y'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'message_linear', 'output_value': 'posY'})

			# x:975 y:401
			OperatableStateMachine.add('set value z',
										CalculationState(calculation=lambda p: p.pos.pos.orientation.z),
										transitions={'done': 'check position z'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'message_angular', 'output_value': 'posZ'})

			# x:1097 y:58
			OperatableStateMachine.add('stop linear',
										PIF_MoveState(),
										transitions={'done': 'turn'},
										autonomy={'done': Autonomy.Off},
										remapping={'linear': 'zero', 'angular': 'zero'})

			# x:1210 y:151
			OperatableStateMachine.add('turn',
										PIF_MoveState(),
										transitions={'done': 'get position angular'},
										autonomy={'done': Autonomy.Off},
										remapping={'linear': 'zero', 'angular': 'angular'})

			# x:599 y:30
			OperatableStateMachine.add('check position x',
										CompareConditionState(),
										transitions={'value_1': 'set new value x', 'value_2': 'set value y', 'failed': 'failed'},
										autonomy={'value_1': Autonomy.Off, 'value_2': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'value_1': 'posX', 'value_2': 'x'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
