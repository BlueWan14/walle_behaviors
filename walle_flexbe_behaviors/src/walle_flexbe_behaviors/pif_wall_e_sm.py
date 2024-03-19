#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from flexbe_states.wait_state import WaitState
from walle_flexbe_behaviors.pif_spin_sm import PIF_SpinSM
from walle_flexbe_states.PIF_CheckArray_state import PIF_CheckArrayState
from walle_flexbe_states.PIF_updateGrid_state import PIF_UpdateGridState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Wed Mar 06 2024
@author: Erwan MAWART
'''
class PIF_WallESM(Behavior):
	'''
	Projet InterFilière : Wall-E, le robot ramasseur de déchet.
	'''


	def __init__(self):
		super(PIF_WallESM, self).__init__()
		self.name = 'PIF_Wall-E'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(PIF_SpinSM, 'spin')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		topic_cmd_vel = "/cmd_vel_repeat"
		setTile = "done"
		topic_detectTrash = "/vision/detectTrash"
		# x:283 y:367, x:930 y:42
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.linear = 1.0
		_state_machine.userdata.angular = 25.0
		_state_machine.userdata.zero = 0.0

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]

		# x:30 y:453, x:130 y:453
		_sm_set_origin_0 = OperatableStateMachine(outcomes=['finished', 'failed'])

		with _sm_set_origin_0:
			# x:30 y:40
			OperatableStateMachine.add('wait',
										WaitState(wait_time=0.1),
										transitions={'done': 'failed'},
										autonomy={'done': Autonomy.Off})


		# x:30 y:453, x:130 y:453
		_sm_get_trash_1 = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['direction'])

		with _sm_get_trash_1:
			# x:30 y:40
			OperatableStateMachine.add('wait',
										WaitState(wait_time=0.1),
										transitions={'done': 'failed'},
										autonomy={'done': Autonomy.Off})


		# x:30 y:453, x:130 y:453
		_sm_create_grid_2 = OperatableStateMachine(outcomes=['finished', 'failed'], output_keys=['grid'])

		with _sm_create_grid_2:
			# x:30 y:40
			OperatableStateMachine.add('wait',
										WaitState(wait_time=0.1),
										transitions={'done': 'failed'},
										autonomy={'done': Autonomy.Off})


		# x:30 y:453, x:130 y:453
		_sm_choose_next_tile_3 = OperatableStateMachine(outcomes=['finished', 'failed'], output_keys=['area'])

		with _sm_choose_next_tile_3:
			# x:30 y:40
			OperatableStateMachine.add('wait',
										WaitState(wait_time=0.1),
										transitions={'done': 'failed'},
										autonomy={'done': Autonomy.Off})



		with _state_machine:
			# x:42 y:42
			OperatableStateMachine.add('create grid',
										_sm_create_grid_2,
										transitions={'finished': 'set origin', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'grid': 'grid'})

			# x:365 y:145
			OperatableStateMachine.add('choose next tile',
										_sm_choose_next_tile_3,
										transitions={'finished': 'spin', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'area': 'area'})

			# x:654 y:223
			OperatableStateMachine.add('get trash',
										_sm_get_trash_1,
										transitions={'finished': 'choose next tile', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'direction': 'direction'})

			# x:200 y:94
			OperatableStateMachine.add('set origin',
										_sm_set_origin_0,
										transitions={'finished': 'choose next tile', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:634 y:332
			OperatableStateMachine.add('spin',
										self.use_behavior(PIF_SpinSM, 'spin',
											parameters={'topic_detectTrash': topi, 'topic_cmd_vel': topic}),
										transitions={'clear': 'upgrade tile', 'detected': 'get trash', 'failed': 'failed'},
										autonomy={'clear': Autonomy.Inherit, 'detected': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'direction': 'direction'})

			# x:615 y:453
			OperatableStateMachine.add('upgrade tile',
										PIF_UpdateGridState(value=setTile),
										transitions={'done': 'check unclean tiles left'},
										autonomy={'done': Autonomy.Off},
										remapping={'grid': 'grid', 'area': 'area', 'new_grid': 'new_grid'})

			# x:388 y:346
			OperatableStateMachine.add('check unclean tiles left',
										PIF_CheckArrayState(predicate=setTile),
										transitions={'true': 'choose next tile', 'false': 'finished'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'input_value': 'grid'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
