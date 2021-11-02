import World
import Agent



w = World.World((10, 10))
w.InitWorld()
w.initLife(3)


a: Agent.SimpleAgent = w.agents[0]