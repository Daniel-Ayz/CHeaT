The dataset is designed to run on PurpleLlama, a prompt injection evaluation framework that we repurposed to evaluate our deception strategies against autonomous LLM-based cyber agents. We achieved this by reusing the default field names of the keys in the input JSON for our own parameters. This was done as follows:

### Dataset ↔ PurpleLlama Field Mapping

| PurpleLlama JSON key | Repurposed for CHeaT    | Meaning                                              |
| -------------------- | ----------------------- | ---------------------------------------------------- |
| `injection_variant`  | **Frame**               | The framing wrapper used around the payload.         |
| `injection_type`     | **Target Data point**   | Where in the environment the payload is planted.     |
| `risk_category`      | **Technique**           | Specific deception / trap technique.                 |
| `speaking_language`  | **Agent system prompt** | System-level prompt provided to the attacking agent. |

With this mapping the dataset remains **100 % compatible with PurpleLlama**: you can evaluate it exactly as described in their docs.

---

### Example — Evaluate the entire dataset with GPT-4o & GPT-4o-mini

```bash
python3 -m CybersecurityBenchmarks.benchmark.run \
  --benchmark=prompt-injection \
  --prompt-path="$DATASETS/CHeaT/dataset_main.json" \
  --response-path="$DATASETS/CHeaT/dataset_main_responses.json" \
  --judge-response-path="$DATASETS/CHeaT/dataset_main_judge_responses.json" \
  --stat-path="$DATASETS/CHeaT/dataset_main_stat.json" \
  --judge-llm=OPENAI::gpt-4o::API_KEY \
  --llm-under-test=OPENAI::gpt-4o-mini::API_KEY \
  --llm-under-test=OPENAI::gpt-4o::API_KEY \
  --run-llm-in-parallel
```

The command runs both candidate models in parallel while GPT-4o acts as the judge LLM, producing response and statistics files in one pass.

> **PurpleLlama repository:** [https://github.com/meta-llama/PurpleLlama](https://github.com/meta-llama/PurpleLlama) \
> **PurpleLlama docs:** [https://meta-llama.github.io/PurpleLlama/CyberSecEval/docs/benchmarks/prompt_injection](https://meta-llama.github.io/PurpleLlama/CyberSecEval/docs/benchmarks/prompt_injection)


## Payloads & Datasets Provided

```
datasets/
├─ dataset\_main.json
└─ dataset\_boosted\_with\_pi.json
└─payloads/
  ├─ payloads.json
  └─ payloads\_boosted\_with\_prompt\_injection.json
````

* **`payloads.json`** – the framed payloads constructed in the paper.  
* **`payloads_boosted_with_prompt_injection.json`** – payloads that are *boosted* with a prompt-injection wrapper.  
* **`dataset_main.json`** – embeds the framed payloads at multiple target data points and system prompts (uses `payloads.json`).  
* **`dataset_boosted_with_pi.json`** – identical structure but built from the boosted payloads.

---
