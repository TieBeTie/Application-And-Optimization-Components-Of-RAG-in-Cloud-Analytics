# Groundedness

## Intuition
Checks that the answer contains nothing beyond what the retrieved chunks support. Complements [[Faithfulness]]: faithfulness checks completeness (are anchors covered?), groundedness checks parsimony (is anything extra added?).

## Definition
The LLM judge extracts all factual claims from the answer and verifies each against chunks:

$$\text{Groundedness} = \frac{|\{cl \in \text{Claims} : \exists c \in C_k,\; cl \text{ supported by } c\}|}{|\text{Claims}|}$$

## Properties

### Component
Generator. A failure here means the generator added claims not present in any retrieved chunk — hallucination.

### Relationship
If Groundedness < 1 and [[Recall_at_k]] = 1, the retriever was perfect but the generator hallucinated extra content.

If Groundedness < 1, [[Faithfulness]] may still be 1 — anchors are covered, but the answer contains additional unsupported claims.

#rag #metrics #groundedness
