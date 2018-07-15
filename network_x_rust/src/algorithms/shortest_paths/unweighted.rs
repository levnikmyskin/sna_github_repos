use std::collections::{HashMap, HashSet};
use std::thread;
use std::sync::mpsc;
use std::mem;

pub fn all_pairs_shortest_path_length(graph_nodes: &Vec<u32>, graph_adj: &HashMap<u32, Vec<u32>>) -> Vec<(u32, Vec<(u32, u32)>)>{
    let g_nodes = graph_nodes.clone();
    let nodes_chunks = g_nodes.chunks(graph_nodes.len() / 4);
    let (tx, rx) = mpsc::channel();

    let mut chunks: Vec<Vec<u32>> = Vec::new();
    for nodes in nodes_chunks {
        chunks.push(nodes.to_vec());
    }
    
    for nodes in chunks.iter() {
        let sender = mpsc::Sender::clone(&tx);
        let adj = graph_adj.clone();
        let ncopy = nodes.clone();
        let g_nodes = graph_nodes.clone();
        thread::spawn(move || {
            let mut paths = Vec::new();
            for n in ncopy.iter() {
                let path = single_source_shortest_path_length(&g_nodes, &adj, *n, 0);
                paths.push((*n, path));
            }
            sender.send(paths);
        });
    }

    mem::drop(tx);
    return merge_vectors(rx)
}

fn single_source_shortest_path_length(graph_nodes: &[u32], graph_adj: &HashMap<u32, Vec<u32>>, source: u32, cutoff: u32) -> Vec<(u32, u32)> {
    // Check if source node is among graph nodes
    if !graph_nodes.iter().any(|n| source == *n) {
        panic!("Source {} is not in G", source)
    }

    return _single_shortest_path_length(graph_adj, vec![source], cutoff);
}

fn _single_shortest_path_length(adj: &HashMap<u32, Vec<u32>>, firstlevel: Vec<u32>, _cutoff: u32) -> Vec<(u32, u32)> {
    let mut path_length = Vec::new();
    let mut seen = HashSet::new();
    let mut level: u32 = 0;
    let mut nextlevel = firstlevel;

    // not using cutoff at the moment
    while nextlevel.len() > 0{
        let thislevel = nextlevel.clone();
        nextlevel.clear();
        for node in thislevel.iter() {
            if !seen.contains(node){
                seen.insert(*node);
                nextlevel.extend(adj.get(node).unwrap());
                path_length.push((node.clone(), level));
            }
        }
        level += 1;
    }

    return path_length;
}

fn merge_vectors(rx: mpsc::Receiver<Vec<(u32, Vec<(u32, u32)>)>>) -> Vec<(u32, Vec<(u32, u32)>)> {
    let mut final_vec = Vec::new();
    for mut received in rx {
        final_vec.append(&mut received);
    }

    final_vec
}