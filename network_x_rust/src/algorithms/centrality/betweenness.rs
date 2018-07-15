use std::collections::HashMap;
use std::thread;
use std::sync::mpsc;
use std::mem;

#[derive(Hash, Eq, PartialEq, Copy, Clone)]
enum EdgeBet {
    Node(u32),
    NodeTuple((u32, u32)),
}


pub fn betweenness_centrality(graph_nodes: &[u32], graph_adj: &HashMap<u32, Vec<u32>>, num_thread: usize) -> HashMap<u32, f32> {
    let (tx, rx) = mpsc::channel();

    let chunked = get_chunked_nodes(graph_nodes, num_thread);

    for nodes in chunked.iter() {
        let sender = mpsc::Sender::clone(&tx);
        let adj = graph_adj.clone();
        let ncopy = nodes.clone();
        let gncopy = graph_nodes.to_vec();
        thread::spawn(move || {
            for n in ncopy.iter() {
                let (mut S, mut P, mut sigma) = single_source_shortest_path_basic(&gncopy, &adj, *n); 
                sender.send((S, P, sigma, *n));
            }
        });
    }

    mem::drop(tx);
    merge_betweenness(rx, graph_nodes)
}

pub fn edge_betwenness_centrality(graph_nodes: &[u32], graph_adj: &HashMap<u32, Vec<u32>>, edges: &[(u32, u32)], num_thread: usize) -> HashMap<(u32, u32), f32> {
    let (tx, rx) = mpsc::channel();

    let chunked = get_chunked_nodes(graph_nodes, num_thread);

    for nodes in chunked.iter() {
        let sender = mpsc::Sender::clone(&tx);
        let adj = graph_adj.clone();
        let ncopy = nodes.clone();
        let gncopy = graph_nodes.to_vec();
        thread::spawn(move || {
            for n in ncopy.iter() {
                let (mut S, mut P, mut sigma) = single_source_shortest_path_basic(&gncopy, &adj, *n); 
                sender.send((S, P, sigma, *n));
            }
        });
    }
    mem::drop(tx);
    merge_edge_betweenness(rx, graph_nodes, edges)
}

fn get_hashmap_from_nodes(graph_nodes: &[u32]) -> HashMap<u32, f32> {
    let mut h = HashMap::new();
    for node in graph_nodes{
        h.insert(*node, 0.0);
    }
    h
}

fn get_edges_hashmaps(nodes: &[u32], edges: &[(u32, u32)]) -> HashMap<EdgeBet, f32> {
    let mut h = HashMap::new();
    for node in nodes {
        h.insert(EdgeBet::Node(*node), 0.0);
    }
    for edge in edges {
        h.insert(EdgeBet::NodeTuple(*edge), 0.0);
    }
    h
}

fn single_source_shortest_path_basic(graph_nodes: &[u32], graph_adj: &HashMap<u32, Vec<u32>>, source: u32) -> (Vec<u32>, HashMap<u32, Vec<u32>>, HashMap<u32, f32>){
    let mut S = Vec::new();
    let mut P = HashMap::new();
    let mut D = HashMap::new();

    for node in graph_nodes {
        P.insert(*node, Vec::new());
    }
    let mut sigma = get_hashmap_from_nodes(graph_nodes);
    sigma.insert(source, 1.0);
    D.insert(source, 0);
    let mut Q = vec![source];
    
    while Q.len() > 0 {
        let v = Q.remove(0);
        S.push(v);
        let Dv = D.entry(v).or_insert(0).clone();
        let sigmav = sigma.entry(v).or_insert(0.0).clone();

        for neighbour in graph_adj.get(&v).unwrap().iter() {
            if !D.contains_key(neighbour) {
                Q.push(*neighbour);
                D.insert(*neighbour, Dv + 1);
            }
            let nv = *D.get(neighbour).unwrap();
            if nv == Dv + 1 {
                sigma.entry(*neighbour).and_modify(|e| {*e += sigmav});
                P.entry(*neighbour).and_modify(|e| {e.push(v)});
            }
        }
    }

    return (S, P, sigma);
}

fn accumulate_basic(betweenness: &mut HashMap<u32, f32>, S: &mut Vec<u32>, P: &mut HashMap<u32, Vec<u32>>, sigma: &mut HashMap<u32, f32>, source: u32) -> HashMap<u32, f32> {
    let mut delta = get_hashmap_from_nodes(&S);
    while S.len() > 0 {
        let w = S.pop().unwrap().clone();
        let coeff = (1.0 + *delta.get(&w).unwrap()) / *sigma.get(&w).unwrap();
        for node in P.get(&w).unwrap().iter() {
            let val = sigma.get(node).unwrap();
            delta.entry(*node).and_modify(|e| {*e += val * coeff});
        }
        if w != source {
            let val = delta.get(&w).unwrap();
            betweenness.entry(w).and_modify(|e| {*e += val});
        }
    }

    betweenness.clone()
}

fn accumulate_edges(betweenness: &mut HashMap<EdgeBet, f32>, S: &mut Vec<u32>, P: &mut HashMap<u32, Vec<u32>>, sigma: &mut HashMap<u32, f32>, source: u32) -> HashMap<EdgeBet, f32> {
    let mut delta = get_hashmap_from_nodes(&S);
    while S.len() > 0 {
        let w = S.pop().unwrap().clone();
        let coeff = (1.0 + *delta.get(&w).unwrap()) / *sigma.get(&w).unwrap();
        for node in P.get(&w).unwrap().iter() {
            let c = sigma.get(node).unwrap() * coeff;
            if !betweenness.contains_key(&EdgeBet::NodeTuple((*node,  w))) {
                betweenness.entry(EdgeBet::NodeTuple((w, *node))).and_modify(|e| {*e += c});
            } else {
                betweenness.entry(EdgeBet::NodeTuple((*node, w))).and_modify(|e| {*e += c});
            }
            delta.entry(*node).and_modify(|e| {*e += c});
            if w != source {
                betweenness.entry(EdgeBet::Node(w)).and_modify(|e| {*e += delta.get(&w).unwrap()});
            }
        }
    }
    betweenness.clone()
}

fn rescale(betweenness: &mut HashMap<u32, f32>, n: f32) -> HashMap<u32, f32> {
    let scale = 1.0 / ((n - 1.0) * (n - 2.0));
    let bet = betweenness.clone();
    for (key, _) in bet {
        betweenness.entry(key).and_modify(|e| {*e *= scale});
    }

    betweenness.clone()
}

fn rescale_edges(betweenness: &mut HashMap<(u32, u32), f32>, n: f32) -> HashMap<(u32, u32), f32> {
    let scale = 1.0 / (n * (n - 1.0));
    let bet = betweenness.clone();
    for (key, _) in bet {
        betweenness.entry(key).and_modify(|e| {*e *= scale});
    }
    betweenness.clone()
}

fn get_chunked_nodes(nodes: &[u32], num_thread: usize) -> Vec<Vec<u32>> {
    let mut chunked = Vec::new();
    for n in nodes.chunks(nodes.len() / num_thread) {
        chunked.push(n.to_vec());
    }
    return chunked;
}

fn merge_betweenness(rx: mpsc::Receiver<(Vec<u32>, HashMap<u32, Vec<u32>>, HashMap<u32, f32>, u32)>, graph_nodes: &[u32]) -> HashMap<u32, f32> {
    let mut betweenness = get_hashmap_from_nodes(&graph_nodes);
    for received in rx {
        let (mut S, mut P, mut sigma, source) = received;
        betweenness = accumulate_basic(&mut betweenness, &mut S, &mut P, &mut sigma, source);
    }

    rescale(&mut betweenness, graph_nodes.len() as f32)
}

fn merge_edge_betweenness(rx: mpsc::Receiver<(Vec<u32>, HashMap<u32, Vec<u32>>, HashMap<u32, f32>, u32)>, 
    graph_nodes: &[u32], edges: &[(u32, u32)]) -> HashMap<(u32, u32), f32> {
        
    let mut betweenness = get_edges_hashmaps(graph_nodes, edges);
    for received in rx {
        let (mut S, mut P, mut sigma, source) = received;
        betweenness = accumulate_edges(&mut betweenness, &mut S, &mut P, &mut sigma, source);
    }

    for node in graph_nodes.iter() {
        betweenness.remove_entry(&EdgeBet::Node(*node));
    }


    // Recreate hashmap containing edges only
    let mut edges_betweenness: HashMap<(u32, u32), f32> = HashMap::new();
    for (keys, values) in betweenness {
        if let EdgeBet::NodeTuple(val) = keys {
            edges_betweenness.insert(val, values); 
        }
    }

    rescale_edges(&mut edges_betweenness, graph_nodes.len() as f32)
}