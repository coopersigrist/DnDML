import matplotlib.pyplot as plt

class Plot():
    '''
    This is a plot object that will be used to draw plots 

    This will allow us to do all our plotting code with one line with selected attributes of the plotting
    from the user on the GUI

    We can also save and delete these plots (TODO as well as add any other features that seem prudent ) 
    '''

    def __init__(save=False, legend=True, grid=False, name='default'): 
        # TODO Choose all args that would be needed to make different plots ^^ 
        pass
    
    def save_plot(self):
        # TODO Implement a saver which will save the PNG in the saved_plots folder with a particular name
        pass

    def delete_plot(self):
        # TODO This should delete the PNG that was saved with self.name in the process of deleting this object
        pass

    def make_plot(self, x=[], y=[], z=None, title='default'):
        # TODO The main method of this class -- this should create the plot designated by the params along with taking inputs and a name
        pass