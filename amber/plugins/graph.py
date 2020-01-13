#This really does not work - don't try to use this
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plot
from matplotlib.figure import Figure
from io import BytesIO, StringIO
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor
import string
import os
import random
class GraphSession:


    def __init__(self, client, config):
        self.client = client
        self.config = config
	self.transformations = (standard_transformations + (implicit_multiplication_application,) + (convert_xor,))
	  
    def graph(self, f, variable):
        density = self.config["density"] #number of points per unit
        scale = self.config["scale"] #number of units per axe
        fig=Figure()
        ax=fig.add_subplot(111)
        for point in range(density * scale["x"]): #iterate through all the points in the plot defined by the scale and density
	        ax.plot(point/density, parse_expr(f.replace(variable,str(round(point/density,2))), transformations=transformations).evalf()) #set the y coordinate equal to the sympy evaluation for that x value
        exists = True
        while exists:
            filename = ''.join(random.choice(string.ascii_letters) for i in range(15)) + ".png"
            if os.path.exists(self.config["save_location"] + filename):
                exists = False
        
        fig.savefig(self.config["save_location"] + filename, dpi='figure', format='png')

        return filename

    async def respond(self, message):
        #split to get the equation and variable to pass to the graph function
        c = message.content.strip().split()
        if len(c) != 3:
	        await self.client.send("The format of this command is <equation> <variable to solve for>!", message.channel)
        else:
            c[1] = c[1].replace("=", "").replace("f(" + c[2] + ")", "").replace("y", "")
            try:
                filename = discord.File(fp=self.graph(c[1], c[2]), filename="graph.png")
            except:
                await self.client.send("An error occurred! Please try again.", message.channel)
            else:
                await self.client.send(self.config["web_address"] + filename, message.channel)

def load(client, config):
    return GraphSession(client, config)
