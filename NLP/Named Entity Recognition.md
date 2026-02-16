# Named Entity Recognition (NER)

## Intuition

Find named entities (people, places, organizations, ...) in text and classify their type. First step in mapping text to a [[Graph]].

## Definition

A sequence labeling task: given a sequence of tokens $x_1, \ldots, x_n$, assign a label $y_i$ to each token.

$$f: (x_1, \ldots, x_n) \to (y_1, \ldots, y_n), \quad y_i \in \mathcal{T}$$

where $\mathcal{T}$ is a tag set (e.g. IOB format).

### Example

| Token | Tag |
|-------|-----|
| Albert | B-PER |
| Einstein | I-PER |
| was | O |
| born | O |
| in | O |
| Ulm | B-LOC |

B = beginning of entity, I = inside, O = outside.

## Properties

### IOB tagging

| Tag | Meaning |
|-----|---------|
| B-X | Beginning of entity of type X |
| I-X | Inside (continuation) of entity X |
| O | Outside any entity |

Variants: IO, IOB/BIO, IOBES (adds E = end, S = single token).

### Approaches

| Approach | Method |
|----------|--------|
| Rule-based | Regex, dictionaries, gazetteers |
| Feature-based ML | CRF, HMM with handcrafted features |
| Deep learning | BiLSTM-CRF, Transformer-based |
| LLM-based | Prompt-based extraction (best accuracy) |

### Entity types

Standard: PER, LOC, ORG, DATE, NUM.

Domain-specific: Gene, Disease, Drug (biomedical), Financial Instrument (finance).

> Entity recognition should capture both semantic name AND entity type.

## In RAG

[[Query Processor]] extracts entities from [[Query]] $Q$, maps them to nodes in [[Graph]] $G$ via [[Vector Similarity]].

$$Q \xrightarrow{\text{NER}} \{e_1, \ldots, e_k\} \xrightarrow{\text{sim}} \text{nodes in } G$$

See also: [[Relation Extraction]], [[Vector Similarity]], [[Query Processor]]

#nlp #query-processing
