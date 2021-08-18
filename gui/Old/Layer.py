from RendererObj import Renderer, Vec2D

class AlarmManager:
    
    allAlarms = []
    for i in range(0, 100):
        allAlarms.append(False)
    size = 100
    nextEmpty = 0
    #have it as a state machine and ask alarmmanager for changes and states
    #have an alarm trigger soemthing
    # or bth

    @staticmethod
    def set_alarm(ID, aBoolean):
        if ID > -1 and ID < AlarmManager.size:
            AlarmManager.allAlarms[ID] = aBoolean

    @staticmethod
    def get_new_ID():
        AlarmManager.nextEmpty += 1
        return AlarmManager.nextEmpty - 1
        

class Layer:

    def __init__(self, size: Vec2D, topLeft: Vec2D):
        self.topLeft = topLeft
        self.bottomRight = topLeft + size
        self.objects = []

    def draw(self):
        for object in self.objects:
            object.draw()
