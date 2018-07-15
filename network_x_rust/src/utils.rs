use std::collections::HashMap;

pub  fn extract_hashmap_from_vec(graph_adj: &Vec<(u32, Vec<u32>)>) -> HashMap<u32, Vec<u32>> {
    let mut adj = HashMap::new();
    for (key, value) in graph_adj.iter() {
        adj.insert(*key, value.clone());
    }
    adj
}