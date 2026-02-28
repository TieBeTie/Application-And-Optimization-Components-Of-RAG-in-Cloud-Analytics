# Диаграммы архитектуры RAG

## 1. Baseline — текущая система МТС

```mermaid
graph TD
    A[PDF / DOCX / RTF / CSV] --> B[LibreChat RAG API]
    B --> C[Text Splitter\nтокенный чанкинг]
    C --> D[BGE-M3 Embedder]
    D --> E[(Vector Store flat)]
    F[Запрос пользователя] --> G[Retriever top-4 chunks]
    E --> G
    G --> H[LLM self-hosted]
    H --> I[Ответ]

    style C fill:#ffaaaa,stroke:#cc0000
    style G fill:#ffaaaa,stroke:#cc0000
```

Проблема: CSV режется по токенам → 4 строки без заголовков → нет контекста.

---

## 2. Предложенная архитектура — полный pipeline

```mermaid
graph TD
    subgraph Индексация
        A[Документы\nPDF / DOCX / CSV] --> B{Тип?}
        B -->|CSV| C[Table-aware Chunker\nгруппы строк + заголовок]
        B -->|PDF, DOCX| D[Standard Chunker]
        C --> E[spaCy NER + RE\nсущности и связи]
        D --> E
        E --> F[(Knowledge Graph\nLightRAG)]
        E --> G[(BGE-M3\nVector Store)]
        F --> H[GMM Clustering\nсемантические кластеры]
        H --> I[Иерархия уровней\nbez LLM-суммаризаций]
    end

    subgraph Retrieval и генерация
        J[Запрос пользователя] --> K[Query Processor]
        K --> L[Hybrid Retriever]
        I --> L
        G --> L
        L --> M[Graph traversal\nbottom-up]
        L --> N[Vector search\nfallback]
        M --> O[Organizer\nранжирование + token limit]
        N --> O
        O --> P[vLLM Generator]
        P --> Q[Ответ]
    end

    style C fill:#aaffaa,stroke:#009900
    style H fill:#aaffaa,stroke:#009900
    style M fill:#aaffaa,stroke:#009900
```

---

## 3. Workflow запроса — упрощённая схема

```mermaid
graph LR
    A[Запрос\nпользователя] --> B[Query Processor]
    B --> C[Hybrid Retriever\nграф + вектор]
    C --> D[Organizer\ntoken limit]
    D --> E[vLLM Generator]
    E --> F[Ответ]

    G[(Knowledge Graph\nLightRAG + иерархия)] --> C
    H[(BGE-M3\nVector Store)] --> C
```

---

## 4. Построение иерархии графа

```mermaid
graph TD
    A[Документы] --> B[spaCy NER + RE]
    B --> C[Граф уровень 0\nконкретные сущности\nИванов, Договор-123, 15.03.2024]
    C --> D[BGE-M3 эмбеддинги]
    D --> E[GMM Clustering]
    E --> F[Граф уровень 1\nкластеры\nДоговорная база, Финансы]
    F --> G[BGE-M3 агрегация]
    G --> H[GMM Clustering]
    H --> I[Граф уровень 2\nверхнеуровневые темы]

    style E fill:#cce5ff,stroke:#0066cc
    style H fill:#cce5ff,stroke:#0066cc
```

Ключевое: каждый уровень — агрегация векторов (дёшево), не LLM-суммаризация (дорого).

---

## 5. Сравнение подходов к построению иерархии

```mermaid
graph TD
    subgraph GraphRAG дорого
        A1[Уровень 0] -->|LLM суммаризация| B1[Уровень 1]
        B1 -->|LLM суммаризация| C1[Уровень 2]
    end

    subgraph Наш подход дёшево
        A2[Уровень 0] -->|GMM + avg embedding| B2[Уровень 1]
        B2 -->|GMM + avg embedding| C2[Уровень 2]
    end
```
