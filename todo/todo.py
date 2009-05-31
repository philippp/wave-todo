"""Todo Client"""

__author__ = 'todo-client@notphil.com (Philipp Pfeiffenberger)'

import logging

from waveapi import events
from waveapi import model
from waveapi import robot

from models import TodoItem

DEBUG = True
BOT_NAME = 'Taskmop'
CMD_LIST_TASKS = 'show'

def OnParticipantsChanged(properties, context):
  """Invoked when any participants have been added/removed."""
  added = properties['participantsAdded']
  for p in added:
    if p == 'philippp@appspot.com':
      Setup(context)
      break

def OnBlipSubmitted(properties, context):
  """ Called when user submits a blip, checks if it is a command """
  root_wavelet = context.GetRootWavelet()
  newBlip = context.GetBlipById( properties['blipId'] )
  textAdded = str(newBlip.GetDocument().GetText())

  if "%s: %s" % (BOT_NAME, CMD_LIST_TASKS) in textAdded:
    listText = ""
    todoItems = TodoItem.TodoItem.all().fetch(1000)
    for todoItem in todoItems: 
      listText += "%s \n" % todoItem.title
    newBlip.CreateChild().GetDocument().SetText(listText) 
  elif "%s: help" % BOT_NAME in textAdded:
    newBlip.CreateChild().GetDocument().SetText(Help())    
  elif DEBUG:
    newBlip.CreateChild().GetDocument().SetText("I do not understand %s" % textAdded)    
    
def Help():
  """ Generate and return a help string """
  help = ""
  for cmd, desc in {CMD_LIST_TASKS:"List all Tasks"}.items():
    help += "%s: %s - %s" % (BOT_NAME, cmd, desc)
  return help

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
  todo = robot.Robot(BOT_NAME,
                      image_url='http://dummy.appspot.com/icon.png',
                      profile_url='http://philippp.appspot.com/')
  todo.RegisterHandler(events.BLIP_SUBMITTED,
                        OnBlipSubmitted)
  todo.RegisterHandler(events.WAVELET_PARTICIPANTS_CHANGED,
                        OnParticipantsChanged)
  todo.Run()
