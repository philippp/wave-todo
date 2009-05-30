"""Todo Client"""

__author__ = 'todo-client@notphil.com (Philipp Pfeiffenberger)'

import logging

from waveapi import events
from waveapi import model
from waveapi import robot

from models import TodoItem


def OnParticipantsChanged(properties, context):
  """Invoked when any participants have been added/removed."""
  added = properties['participantsAdded']
  for p in added:
    if p == 'philippp@appspot.com':
      Setup(context)
      break

def OnBlipSubmitted(properties, context):
  logging.debug(dir(properties))
  logging.debug(str(properties))
  logging.debug(str(properties.items()))

def Setup(context):
  """Called when this robot is first added to the wave."""
  root_wavelet = context.GetRootWavelet()

  todoItem = TodoItem.TodoItem( 
    title = root_wavelet.GetTitle(),
    waveId = root_wavelet.GetWaveId()
    )
  todoItem.put()  
  root_wavelet.CreateBlip().GetDocument().SetText("Tagging this wave as a todo item.")


if __name__ == '__main__':
  todo = robot.Robot('Taskmop',
                      image_url='http://dummy.appspot.com/icon.png',
                      profile_url='http://philippp.appspot.com/')
  dummy.RegisterHandler(events.WAVELET_PARTICIPANTS_CHANGED,
                        OnParticipantsChanged)
  dummy.RegisterHandler(events.WAVELET_BLIP_CREATED,
                        OnBlipSubmitted)
  dummy.Run()
