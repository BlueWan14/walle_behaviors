#!/usr/bin/env python
from flexbe_core import EventState, Logger


class CompareConditionState(EventState):
    '''
    Checks if the given condition is true and returns the corresponding outcome.
    This state can be used if the further control flow of the behavior depends on a simple condition.

    ># value_1	    object	    Input to the predicate function.
    ># value_2	    object		Input to the predicate function.

    <= value_1 					Returned if the value_1 is the bigest
    <= value_2 					Returned if the value_2 is the bigest
    <= failed 					Returned if failed
    '''

    def __init__(self):
        super(CompareConditionState, self).__init__(outcomes=['value_1', 'value_2', 'failed'],
                                                  input_keys=['value_1', 'value_2'])
        self._outcome = 'failed'

    def execute(self, userdata):
        return self._outcome

    def on_enter(self, userdata):
        try:
            self._outcome = 'value_1' if userdata.value_1 > userdata.value_2 else 'value_2'
        except Exception as e:
            Logger.logwarn('Failed to execute condition function!\n%s' % str(e))
