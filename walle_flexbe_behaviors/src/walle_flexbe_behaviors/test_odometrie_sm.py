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
from walle_flexbe_states.PIF_move_state import PIFMoveState
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
		topic_cmd_vel = "/cmd_vel"
		# x:30 y:365, x:130 y:365
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.i = 0
		_state_machine.userdata.linear = 25.0
		_state_machine.userdata.angular = 10.0
		_state_machine.userdata.zero = 0.0

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:30 y:40
			OperatableStateMachine.add('Nb tours',
										CalculationState(calculation=lambda x: x + 1),
										transitions={'done': 'Forward'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'i', 'output_value': 'i'})

			# x:191 y:90
			OperatableStateMachine.add('Forward',
										PIFMoveState(topic=topic_cmd_vel),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off},
										remapping={'linear': 'linear', 'angular': 'zero'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
