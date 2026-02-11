Anna told me about RAG-API, which can only find info based on vector search.[]()
I need to propose optimizations to boost the accuracy of retrieval and data compression. Then, we need to find the balance between accuracy, speed, and memory.

To achieve that, I need to get ideas from the other articles
First, I need to get a list of them to compare implementations of retrieval mechanisms and data storage. 
# RAG 

| Article           | $G$       | $Q$                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | $Ω^{Processor}$ | $Ω^{Retriever}$ | $Ω^{Organizer}$ | $Ω^{Generator}$ |
| ----------------- | --------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------- | --------------- | --------------- | --------------- |
| GraphRAG overview | Simple KG | [[GraphRAG.pdf#page=7&annotation=3242R\|NES extract entities by deep learning techniques and LLM, which are represented by nodes in the KG]] then [[GraphRAG.pdf#page=8&annotation=3340R \|relationships between entities are represented by edges, these edges are searched in the KG by vector similarity.]]  [[GraphRAG.pdf#page=9&annotation=3380R\| Nodes and edges are used in traversal to find the data in the KG]]<br><br>[[GraphRAG.pdf#page=8&annotation=3370R\|Query expands by adding info from neighbor nodes, ]] <br>[[GraphRAG.pdf#page=8&annotation=3360R\|also it can be split by subqueries according to the template]]<br><br> |                 |                 |                 |                 |
|                   |           |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |                 |                 |                 |                 |
|                   |           |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |                 |                 |                 |                 |


| Работа | Стратегия обхода/поиска | Граф/иерархия | Метрика / скоринг | Особенности |

| --- | --- | --- | --- | --- |

| GraphRAG Overview (2501.00309) | BFS/DFS/A*/MCTS, multi-hop перед генерацией | KG с узлами/рёбрами | Комбинация sim(emb) + графовые сигналы (кратчайшие пути/мультихоп) | Настаивает на явном графовом поиске, не только эмбеддингах |

| From Local to Global (GraphRAG, 2404.16130) | Агент проходит граф элементов; map-reduce по community summaries | Иерархия сообществ (Louvain/Leiden) | score = λ₁·sim(q, summary) + λ₂·community relevance (центральность/глубина) | Локальные/глобальные summary, агрегируются |

| KG-Guided RAG (2502.06864) | m-hop BFS (`traverse`), DFS для связей; семантика → k-hop KG | KG + расширенный подграф | sim семантики + покрытие k-hop; BFS даёт кандидатов, ранжируются по sim | «Top-K семантика + BFS по соседям» |

| LightRAG (2410.05779) | Векторный top-k по сущностям; подтягивание инцидентных рёбер; без community traversal | Плоский KG | Entities: sim(emb) top-k; edges ранжируются degree+weight; chunks — weighted или vector pick | Фокус на latency; критикует дорогой обход GraphRAG |

| GraphRAG-Bench (2506.02404) | Описывает community/agent/KG traversal у методов бенчмарка | Community detection | Метрики зависят от сравниваемых моделей; часто sim+community | Сам обход не задаёт |

| Unbiased Eval GraphRAG (2506.06331) | Random walk от seed; LLM-guided traversal; отбор community summaries | Сообщества с summary | Рассматривает PageRank/centrality, random-walk вероятности + sim | Анализ смещений/стоимости обходов |

| Iterative GraphRAG (2509.25530) | Итеративное извлечение; community-based и multi-hop режимы | Community detection | По этапам: sim для уточнения + графовая близость на следующем шаге | Сравнение парадигм multi-hop |

| SemRAG (2507.21110) | Семантический top-k → релевантные сообщества → summary/подграф | Leiden-иерархия сообществ | score = λ₁·sim(q, chunk) + λ₂·sim(q, community summary) | Локальный/глобальный поиск по community reports |

| LeanRAG (2508.10391) | Bottom-up dual-level traversal: якорные узлы → подъём по путям | Иерархический KG + summary-слой | score = sim(anchor) + path relevance; отбрасывает дубли | Structure-aware retrieval, минимум дубликатов |

| ReMindRAG (2510.13193) | LLM-guided traversal explore/exploit; память путей (replay) | KG | Политика LLM + память: score по шагу = policy(probs) + reuse веса рёбер | Запоминает удачные обходы в эмбеддингах рёбер |

| T-GRAG (2508.01680) | kNN по временным ключам (не BFS) | Временной ключевой граф | score = sim текстовая · decay(time); top-k kNN | Темпоральная релевантность |

| XGraphRAG (2506.13782) | Поиск подграфов для визуального анализа (алгоритм не детализирован) | — | — | Интерактивная аналитика, не про алгоритм |



