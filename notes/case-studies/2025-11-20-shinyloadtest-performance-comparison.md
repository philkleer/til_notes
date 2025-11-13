# Case Study: Benchmarking Shiny app performance across environments with `shinyloadtest`
_Date: 2025-11-20_

## Context
After optimizing a Shiny application, I wanted to quantify the performance difference. To do this, I used **shinyloadtest** to simulate realistic user sessions and compare three environments:

1. New version deployed to Kubernetes with cache
2. New version deployed to Kubernetes
3. Old version deployed to Kubernetes

## Method

I used the **shinyloadtest + shinycannon** workflow:

1. **Record** a representative user session locally which creates a `.log` file describing all user interactions.

```r
library(shinyloadtest)
record_session("http://localhost:8080")
``` 

2. Replay and benchmark the session with `shinycannon`: This runs multiple concurrent simulated sessions against the app (either locally or on Kubernetes) and saves performance metrics. `shinycannon` stores raw performance logs, which I later combined into a data frame using `shinyloadtest::load_runs()`.

```bash
shinycannon recording.log \
  https://app-url.example.org \
  --workers 5 --loaded-duration-minutes 2 \
  --output-dir results-new-version
```

3. Analyze results in R using `shinyloadtest::load_runs()`:

```r
df <- load_runs(
  `new in kubernetes with cache` = "run_tests/new_kube_cache",
  `new in kubernetes` = "run_test/new_kube",
  `old in kubernetes` = "run_test/old_kube"
)
```

4. I generated an HTML report summarizing latency distributions, throughput, and response timing using `shinyloadtest::shinyloadtest_report()`.

```r
shinyloadtest::shinyloadtest_report(df, "report_comparison.html")
```

## Results

Each test used 5 concurrent simulated users; absolute timings depend on CPU/network resources of the test host. I present median values and minimum and maximum in the brackets.

### Total way of seeing everything

| Environment            | Session Duration | Total HTTP         | Maximum Websocket (latency* / total)  | Slowest process (as defined in old version) |
|------------------------|------------------|--------------------|---------------------------------------|---------------------------------------------|
| New version with cache | 61 [46.6 - 100]  | 1.44 [1.34 - 1.53] | 3.55 [2.20 - 5.53] / 59.1 [44 - 98.8] | 0.175 [0.119 - 0.460]                       |
| New version            | 183 [153 - 192]  | 2.15 [1.64 - 2.92] | 4.56 [2.31 - 6.29] / 173 [151 - 190]  | 0.413 [0.412 - 0.430]                       |
| Old version            | 224 [221 - 238]  | 2.36 [1.95 - 2.99] | 2.96 [1.58 - 3.84] / 221 [206 - 235]  | 1.24 [0.629 - 4.40]                         |

> [!NOTE]
> WebSocket latency measures message-level round-trip time, which can increase slightly in caching architectures even when overall responsiveness improves.

![Overall](assets/shiny-comparison-de-en.png)

![5 slowest processes in old version](assets/shiny-comparison-en.png)

- **New version (structure + cache, Kubernetes)**: more stable under load — faster median response time.  
- **New version (structure, Kubernetes)**: loads the first view faster, but overall execution remains roughly three times slower than the cached version
- **Old version (Kubernetes)**: ~ 3.5 times slower than new version with cache in total and for loading first view ca. 60% slower, more variance at higher concurrency.

Caching reduced redundant computation by reusing previously generated results—such as precomputed data summaries, plots, and reactive expressions—across user sessions. Instead of recalculating expensive operations every time, the app now retrieves these results directly from memory or a local cache layer. This optimization not only lowered CPU load but also shortened response times under concurrency, leading to smoother user interactions and more stable performance during load tests.

### Simple back and forth between two pages

| Environment            | Session Duration   |
|------------------------|--------------------|
| New version with cache | 19.3 [12.4 - 23.9] |
| New version            | 28.7 [15.8 - 35.8] |
| Old version            | 28.1 [15.0 - 34.5] |

## Takeaways

- **Optimizing reactive logic** in Shiny directly improved scalability.  
- `shinyloadtest` is an excellent lightweight tool to validate improvements.

## References
- [`shinyloadtest`](https://rstudio.github.io/shinyloadtest/)
