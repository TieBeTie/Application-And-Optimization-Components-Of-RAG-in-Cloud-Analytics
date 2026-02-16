# Relation Extraction

## Intuition

Find relations between entities in text. Produces triplets $(h, r, t)$ that become edges in a [[Graph|Knowledge Graph]].

## Definition

Given a sentence $s$ and a set of entities $\{e_1, \ldots, e_k\} \subset s$, extract a set of relational triplets:

$$\text{RE}(s) = \{(h, r, t) \mid h, t \in \text{entities},\ r \in \mathcal{R}\}$$

where $h$ = head (subject), $t$ = tail (object), $r$ = relation type from a predefined set $\mathcal{R}$.

### Example

"Albert Einstein was born in Ulm."

$$(\text{Albert Einstein},\ \text{born\_in},\ \text{Ulm})$$

Maps to edge: $\text{Albert Einstein} \xrightarrow{\text{born\_in}} \text{Ulm}$ in [[Graph]] $G$.

## Properties

### Approaches

| Approach | Method |
|----------|--------|
| Pipeline | [[Named Entity Recognition\|NER]] first, then classify relation for each entity pair |
| Joint | Extract entities and relations simultaneously |
| Seq2Seq | Generate triplets as sequences (LLM-based) |

Pipeline is simpler but suffers from error propagation (NER errors cascade into RE).

### Overlapping problem

One entity can participate in multiple triplets:

"Einstein was born in Ulm and worked at Princeton."

$\Rightarrow$ (Einstein, born\_in, Ulm) **and** (Einstein, worked\_at, Princeton).

Joint extraction handles this better than pipeline.

## In RAG

[[Query Processor]] extracts relations from [[Query]] $Q$, maps them to edges in [[Graph]] $G$ via [[Vector Similarity]].

$$Q \xrightarrow{\text{RE}} \{(h, r, t)\} \xrightarrow{\text{sim}} \text{edges in } G$$

See also: [[Named Entity Recognition]], [[Vector Similarity]], [[Query Processor]]

#nlp #query-processing
