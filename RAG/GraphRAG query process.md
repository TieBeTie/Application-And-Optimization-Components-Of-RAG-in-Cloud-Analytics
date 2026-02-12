#RAG 
## Given

- [[Graph]] $G$ — graph-structured data source
- [[Query]] $Q$ — user-defined query

## Components

| Component           | Symbol               | Input → Output                                   |
| ------------------- | -------------------- | ------------------------------------------------ |
| [[Query Processor]] | $\Omega^{Processor}$ | $Q \rightarrow \hat{Q}$ (processed query)        |
| [[Retriever]]       | $\Omega^{Retriever}$ | $(\hat{Q}, G) \rightarrow C$ (retrieved content) |
| [[Organizer]]       | $\Omega^{Organizer}$ | $C \rightarrow S$ (structured content)           |
| [[Generator]]       | $\Omega^{Generator}$ | $(\hat{Q}, S) \rightarrow A$ (answer)            |

## Pipeline

$$Q \xrightarrow{\Omega^{Processor}} \hat{Q} \xrightarrow{\Omega^{Retriever}} C \xrightarrow{\Omega^{Organizer}} S \xrightarrow{\Omega^{Generator}} A$$

