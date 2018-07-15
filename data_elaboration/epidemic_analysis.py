import ndlib.models.epidemics.SIRModel as sir
import ndlib.models.epidemics.SIModel as si
import ndlib.models.epidemics.SISModel as sis
import ndlib.models.epidemics.ThresholdModel as thresh
import ndlib.models.ModelConfig as mc
from ndlib.viz.mpl.DiffusionTrend import DiffusionTrend


def get_epidemic_analysis(graph):
    # csvfile = "network.csv"

    # graph_ba = nx.barabasi_albert_graph(1000, 5, seed=None)
    # graph_er = nx.erdos_renyi_graph(1000, 0.1)

    get_epidemic_si(graph)
    get_epidemic_threshold(graph)
    get_epidemic_sir(graph)
    get_epidemic_threshold(graph)


def get_epidemic_si(graph, beta, perc_inf, infected_nodes):
    model_si = si.SIModel(graph)

    cfg_si = mc.Configuration()
    cfg_si.add_model_parameter("beta", beta)
    cfg_si.add_model_parameter("percentage_infected", perc_inf)
    cfg_si.add_model_parameter("Infected", infected_nodes)
    model_si.set_initial_status(cfg_si)

    iteration_si = model_si.iteration_bunch(50)
    trends_si = model_si.build_trends(iteration_si)
    viz_si = DiffusionTrend(model_si, trends_si)
    viz_si.plot()


def get_epidemic_sis(graph, beta, lamb, perc_inf, infected_nodes):
    model_sis = sis.SISModel(graph)

    cfg_sis = mc.Configuration()
    cfg_sis.add_model_parameter("beta", beta)
    cfg_sis.add_model_parameter("lambda", lamb)
    cfg_sis.add_model_parameter("percentage_infected", perc_inf)
    cfg_sis.add_model_parameter("Infected", infected_nodes)
    model_sis.set_initial_status(cfg_sis)

    iteration_sis = model_sis.iteration_bunch(100)
    trends_sis = model_sis.build_trends(iteration_sis)
    viz_sis = DiffusionTrend(model_sis, trends_sis)
    viz_sis.plot()


def get_epidemic_threshold(graph, perc_inf, threshold, infected_nodes):
    model_threshold = thresh.ThresholdModel(graph)

    cfg_threshold = mc.Configuration()
    cfg_threshold.add_model_parameter("percentage_infected", perc_inf)
    cfg_threshold.add_model_parameter("Infected", infected_nodes)

    for node in graph.nodes():
        cfg_threshold.add_node_configuration("threshold", node, threshold)
    model_threshold.set_initial_status(cfg_threshold)

    iteration_threshold = model_threshold.iteration_bunch(25)
    trends_threshold = model_threshold.build_trends(iteration_threshold)
    viz_threshold = DiffusionTrend(model_threshold, trends_threshold)
    viz_threshold.plot()


def get_epidemic_sir(graph, beta, gamma, perc_inf, infected_nodes):
    model_sir = sir.SIRModel(graph)

    cfg_sir = mc.Configuration()
    cfg_sir.add_model_parameter("beta", beta)  # infection
    cfg_sir.add_model_parameter("gamma", gamma)  # recovery
    cfg_sir.add_model_parameter("percentage_infected", perc_inf)
    cfg_sir.add_model_parameter("Infected", infected_nodes)
    model_sir.set_initial_status(cfg_sir)

    iterations_sir = model_sir.iteration_bunch(100, node_status=True)
    trends_sir = model_sir.build_trends(iterations_sir)
    viz_sir = DiffusionTrend(model_sir, trends_sir)
    viz_sir.plot()


# TODO: analizzare differenti modelli di diffusione SI SIR SIS Threshold
    # TODO: 1)simulare su CRAWLED, ER e BA 2)ripetere variando le condizioni iniziali (settare nodi più importanti infetti)
    
    # A common goal for which diffusion simulations are executed is to perform
    # comparison among different models (or different instantiations of a same model).
