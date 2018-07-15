#![feature(proc_macro, proc_macro_path_invoc, specialization, const_fn)]

extern crate pyo3;
mod algorithms;
mod utils;

use algorithms::shortest_paths::generics::shortest_path;
use algorithms::centrality::betweenness;
use pyo3::prelude::*;
use std::collections::HashMap;
use utils::extract_hashmap_from_vec;



#[py::modinit(networkxrust)]
fn init_mod(py: Python, m: &PyModule) -> PyResult<()> {


    m.add_class::<Elab>()?;
    Ok(())
}

#[py::class]
pub struct Elab {
    graph_nodes: Vec<u32>,
    graph_adj: Vec<(u32, Vec<u32>)>,
    sh_path: Vec<(u32, Vec<(u32, u32)>)>
}

#[py::methods]
impl Elab{
    #[new]
    fn __new__(obj: &PyRawObject, graph_nodes: Vec<u32>, graph_adj: Vec<(u32, Vec<u32>)>) -> PyResult<()> {
        let mut el = Elab{graph_nodes: graph_nodes, graph_adj: graph_adj, sh_path: Vec::new(),};
        obj.init(|_| el)
    }

    #[getter]
    fn graph_nodes(&self) -> PyResult<Vec<u32>> {
        Ok(self.graph_nodes.clone())
    }

    #[getter]
    fn graph_adj(&self) -> PyResult<Vec<(u32, Vec<u32>)>> {
        Ok(self.graph_adj.clone())
    }

    fn add(&mut self, adj: Vec<(u32, Vec<u32>)>) -> PyResult<()> {
       self.graph_adj.extend(adj); 
       Ok(())
    }

    // Requires lot of RAM with huge networks
    fn shortest_path_length(&mut self, py: Python) -> PyResult<()> {
        let adj = extract_hashmap_from_vec(&self.graph_adj);
        let nodes = self.graph_nodes.clone();
        let result = py.allow_threads(move || shortest_path(&nodes, &adj));
        self.sh_path = result;
        Ok(())
    }

    fn get_chunk_of_shpath(&mut self, i: usize) -> PyResult<(u32, Vec<(u32, u32)>)> {
        let elem = self.sh_path.remove(i);
        self.sh_path.shrink_to_fit();
        Ok(elem)
    }

    fn betweenness_centrality(&self, py: Python, num_thread: usize) -> PyResult<HashMap<u32, f32>> {
        let adj = extract_hashmap_from_vec(&self.graph_adj);
        Ok(py.allow_threads(move || betweenness::betweenness_centrality(&self.graph_nodes, &adj, num_thread)))
    }

    fn edge_betwenness_centrality(&self, py: Python, num_thread: usize, edges: Vec<(u32, u32)>) -> PyResult<HashMap<(u32, u32), f32>> {
        let adj = extract_hashmap_from_vec(&self.graph_adj);
        Ok(py.allow_threads(move || betweenness::edge_betwenness_centrality(&self.graph_nodes, &adj, &edges, num_thread)))
    }
}
