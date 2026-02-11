# Relation Extraction

Identify relations between entities. Similar to [[Named Entity Recognition]].

## Applications

- Sentiment analysis
- Question answering
- Summarization
- Building [[Graph|Knowledge Graph]]

## How it works

Extract triplets: `(subject, relation, object)`

## Example

Query: "What is the capital of China?"
→ Relation: `capital_of`
→ Triplet: `(?, capital_of, China)`

## In RAG Pipeline

[[Query Processor]] → Relation Extraction → [[Retriever]]

1. Extract relations from [[Query]] $Q$
2. Match relations to edges in [[Graph]] $G$ via [[Vector Similarity]]
3. [[Retriever]] searches matching edges

## Search

Edges in $G$ are matched by [[Vector Similarity]] (same as [[Named Entity Recognition|NER]] for nodes).

#nlp #query-processing
