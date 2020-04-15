from agent_based.money_model import MoneyModel
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer


def agent_portrayal(agent):
    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "Layer": 0,
                 "Color": "red",
                 "r": 0.5}
    return portrayal


grid = CanvasGrid(agent_portrayal, 100, 100, 500, 500)
server = ModularServer(MoneyModel,
                       [grid],
                       "Money Model",
                       {"N": 1000, "width": 100, "height": 100})
server.port = 8521  # The default
server.launch()
