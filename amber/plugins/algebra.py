from sympy import *
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor

class AlgebraSession:


    def __init__(self, client, config):
        self.client = client
        self.config = config
        self.transformations = (standard_transformations + (implicit_multiplication_application,) + (convert_xor,))
	
	
    async def respond(self, message):
        #split to get the equation and then turn it from a string into something that sympy can understand
        c = message.content.strip().split()
        if len(c) != 3:
            response = "The format of this command is <equation>!"
        else:
            #split the equation into 2 parts using the = sign as the divider, parse, and turn into an equation sympy can understand - use common notation not python notation https://stackoverflow.com/questions/59632620/sympy-has-syntax-errors
            equation = Eq(parse_expr(c[2].split("=")[0], transformations=self.transformations), parse_expr(c[2].split("=")[1], transformations=self.transformations))
            answers = solve(equation)
            #check for answers and send them if there are any
            if len(answers) == 0:
                response = "There are no solutions!"
            else:
                response = "The answer(s) are "
                for answer in answers:
                    response = response + str(answer) + ", "
                response = response[:-2]
        await self.client.send(response, message.channel)

def load(client, config):
    return AlgebraSession(client, config)
