import matplotlib.pyplot as plot
from sympy import *
from io import StringIO
import discord
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor

class GraphSession:


    def __init__(self, client, config):
        self.client = client
        self.config = config
        self.transformations = (standard_transformations + (implicit_multiplication_application,) + (convert_xor,))
	  
    def graph(self, f, variable):
        density = self.config["density"] #number of points per unit
        scale = self.config["scale"] #number of units per axe
        for point in range(density * scale["x"]): #iterate through all the points in the plot defined by the scale and density
	        plot(point/density, solve(parse_expr(f.replace("x",str(round(point/density,2)))), transformations=self.transformations)) #set the y coordinate equal to the sympy answer for that x value

        image_data = StringIO.StringIO()
        plot.savefig(image_data, format='jpg')
        image_data.seek(0)
        return image_data

    async def respond(self, message):
        #split to get the equation and variable to pass to the graph function
        c = message.content.strip().split()
        if len(c) != 4:
	        response = "The format of this command is <equation> <variable to solve for>!"
        c[2] = c[2].replace("=", "").replace("f(x)", "").replace("y", "")
        try:
            picture = discord.File(self.graph(c[2], c[3]))
        except:
            await self.client.send("An error occurred! Please try again.", message.channel)
        else:
	        await message.channel.send(file=picture)

def load(client, config):
    return GraphSession(client, config)
