# Named Entity Recognition (NER)

Extract named entities from text and map them to nodes in [[Graph]] $G$.

## Approaches

1. **Rule-based** — handcrafted rules, no annotated data
2. **Unsupervised** — learn without labels
3. **Feature-based supervised** — traditional ML with manual features
4. **Deep learning / LLM** — best accuracy, but slower

Recent developments show LLM-based extraction achieves best results.

## Example

Query: "What is the best way to guess the color of the eye of the baby?"
→ Entities: `baby`, `eye`, `color`
→ Map to nodes in [[Graph]] $G$

## In RAG Pipeline

[[Query Processor]] → NER → [[Retriever]]

1. Extract entities from [[Query]] $Q$
2. Recognize entity **type** (not just name)
3. Map to nodes in [[Graph]] $G$ via [[Vector Similarity]]
4. [[Retriever]] uses types to match nodes for exploration

## Search

Nodes in $G$ are matched by [[Vector Similarity]] (embeddings).

> Entity recognition should be based on both semantic name AND entity type.

See also: [[Relation Extraction]] (same approach for edges)

#nlp #query-processing
