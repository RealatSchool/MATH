import matplotlib.pyplot as plot
import sympy
import StringIO
import discord

class GraphSession:


    def __init__(self, client, config):
        self.client = client
        self.config = config
	  
    def graph(function, variable):
        density = config["graph"]["density"] #number of points per unit
        scale = config["graph"]["scale"] #number of units per axe
        for point in range(density * scale["x"]): #iterate through all the points in the plot defined by the scale and density
	        plot(point/density,sympy.solve(sympy.parsing.sympy_parser.parse_expr(function.replace("x",str(point/density))), variable)) #set the y coordinate equal to the sympy answer for that x value

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
            picture = discord.File(graph(c[2], c[3])
        except:
            await self.client.send("An error occurred! Please try again.")
        else:
	        await self.client.send(file=picture, channel=message.channel)

def load(client, config):
    return GraphSession(client, config)
