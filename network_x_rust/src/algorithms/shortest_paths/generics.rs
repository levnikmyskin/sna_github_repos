extern crate pyo3;
use std::collections::HashMap;
use algorithms::shortest_paths::unweighted::all_pairs_shortest_path_length;

pub fn shortest_path(graph_nodes: &Vec<u32>, graph_adj: &HashMap<u32, Vec<u32>>) -> Vec<(u32, Vec<(u32, u32)>)>{
    return all_pairs_shortest_path_length(graph_nodes, graph_adj);
}

