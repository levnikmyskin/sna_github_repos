import networkx as nx
import ndlib.models.epidemics.SIRModel as sir
import ndlib.models.ModelConfig as mc
import json
from data_elaboration.network_setup import create_network_from_csv

# TODO: ehhhh importare la roba... non credo sia questo quello che intendevi ihih
csvfile = "network.csv"

graph_ba = nx.barabasi_albert_graph(1000, 5, seed=None)
graph_er = nx.erdos_renyi_graph(1000, 0.1)
grap_crawled = create_network_from_csv(csvfile)


model = sir.SIRModel(grap_crawled)
print(json.dumps(model.parameters, indent=2))
# da qui capisco quali sono i parametri necessari al modello (in questo caso Infection & Recovery Rate ovviamente
# per settare i parametri istanzio un oggetto configuration a cui poi passo i parametri necessari

cfg = mc.Configuration()
cfg.add_model_parameter("beta", 0.001) #infection
cfg.add_model_parameter("gamma", 0.01) #recovery
cfg.add_model_parameter("percentage_infected", 0.10)

model.set_initial_status(cfg)

iterations = model.iteration_bunch(200, node_status=True)

trends = model.build_trends(iterations)

from ndlib.viz.mpl.DiffusionTrend import DiffusionTrend
viz = DiffusionTrend(model, trends)
viz.plot()

# TODO: analizzare differenti modelli di diffusione SI SIR SIS Threshold
# TODO: 1)simulare su CRAWLED, ER e BA 2)ripetere variando le condizioni iniziali (settare nodi più importanti infetti)

# A common goal for which diffusion simulations are executed is to perform
# comparison among different models (or different instantiations of a same model).