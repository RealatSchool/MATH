import matplotlib.pyplot as plot
import sympy

class GraphSession:


    def __init__(self, client, config):
        self.client = client
        self.config = config
	  
    def graph(function):
        density = config["graph"]["density"]
        scale = config["graph"]["scale"]
	
    async def respond(self, message):
        #split to get the equation and then turn it from a string into something that sympy can understand
        c = message.content.strip().split()
	if len(c) != 4:
	    response = "The format of this command is <equation> <variable to solve for>!"
	else:
            answers = sympy.solve(sympy.parsing.sympy_parser.parse_expr(c[2]), c[3])
            #check for answers and send them if there are any
            if answer.len == 0:
	        response = "There are no solutions!"
            else:
                response = "The answers are "
                for answer in answers:
                    response = response + answer + ", "
                response = response[:-2]
	await self.client.send(response, message.channel)

def load(client, config):
    return GraphSession(client, config)
