#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from walle_flexbe_states.PIF_subscribeROS_state import PIF_SubscriberROSState
from flexbe_states.calculation_state import CalculationState
from flexbe_states.check_condition_state import CheckConditionState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Thu Mar 07 2024
@author: Erwan MAWART
'''
class PIF_SpinSM(Behavior):
	'''
	Detection dechet.
	'''


	def __init__(self):
		super(PIF_SpinSM, self).__init__()
		self.name = 'PIF_Spin'

		# parameters of this behavior
		self.add_parameter('wait_time', '1')
		self.add_parameter('topic_detectTrash', '')
		self.add_parameter('topic_cmd_vel', '')

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		complete_spin = 8
		# x:109 y:154, x:682 y:150, x:520 y:221
		_state_machine = OperatableStateMachine(outcomes=['clear', 'detected', 'failed'], output_keys=['direction'])
		_state_machine.userdata.zero = 0
		_state_machine.userdata.angular = 45
		_state_machine.userdata.i = 1
		_state_machine.userdata.direction = None

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:50 y:52
			OperatableStateMachine.add('End loop',
										CheckConditionState(predicate=lambda x: x > complete_spin),
										transitions={'true': 'clear', 'false': 'Check for trash'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'input_value': 'i'})

			# x:281 y:25
			OperatableStateMachine.add('i + 1',
										CalculationState(calculation=lambda x: x + 1),
										transitions={'done': 'End loop'},
										autonomy={'done': Autonomy.Off},
										remapping={'input_value': 'i', 'output_value': 'i'})

			# x:449 y:117
			OperatableStateMachine.add('Check for trash',
										PIF_SubscriberROSState(topic=self.detectTrash, wait_time=self.wait_time, blocking=True, clear=False),
										transitions={'received': 'detected', 'unavailable': 'failed', 'no_data': 'i + 1'},
										autonomy={'received': Autonomy.Off, 'unavailable': Autonomy.Off, 'no_data': Autonomy.Off},
										remapping={'message': 'direction'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
