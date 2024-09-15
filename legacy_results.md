# Legacy results

**Solvable Pass Rate:**
| **Method** | **I1 Instruction** | **I1 Category** | **I1 Tool** | **I2 Category** | **I2 Instruction** | **I3 Instruction** | **Average** |
| --- | --- | --- | --- | --- | --- | --- | --- |
| GPT-3.5-Turbo-0613 (CoT) | 52.2±1.1 | 47.3±0.6 | 53.6±1.3 | 42.5±2.1 | 35.8±2.0 | 48.1±0.8 | 46.6±1.3 |
| GPT-3.5-Turbo-0613 (DFS) | 60.3±1.3 | 66.2±1.2 | 67.1±0.0 | 59.1±0.4 | 51.3±1.2 | 73.8±2.3 | 63.0±1.1 |
| GPT-4-0613 (CoT) | 45.5±0.4 | 57.4±0.3 | 48.8±0.7 | 43.0±0.7 | 46.5±0.9 | 48.1±1.5 | 48.2±0.8 |
| GPT-4-0613 (DFS) | 57.3±0.6 | 57.3±0.3 | 60.9±1.0 | 57.9±1.0 | 51.3±0.8 | 66.4±2.4 | 58.5±1.0 |
| ToolLLaMA v2 (CoT) | 32.3±1.0 | 40.3±0.8 | 36.7±0.5 | 34.7±0.7 | 25.2±0.4 | 33.9±1.5 | 33.9±0.8 |
| ToolLLaMA v2 (DFS) | 44.5±0.9 | 49.6±1.3 | 48.9±2.7 | 50.8±1.1 | 31.9±1.9 | 53.6±2.0 | 46.6±1.7 |
| GPT-3.5-Turbo-1106 (CoT) | 50.4±0.5 | 45.1±1.4 | 50.8±0.3 | 48.7±0.8 | 42.1±0.4 | 55.7±0.0 | 48.8±0.6 |
| GPT-3.5-Turbo-1106 (DFS) | 62.8±0.3 | 63.9±1.2 | 65.6±0.3 | 56.5±0.7 | 56.9±1.2 | 67.2±1.3 | 62.2±0.8 |
| GPT-4-Turbo-Preview (CoT) | 52.8±1.3 | 56.6±0.9 | 51.9±0.5 | 51.9±1.0 | 52.8±0.8 | 52.5±0.0 | 53.1±0.8 |
| GPT-4-Turbo-Preview (DFS) | 59.2±0.5 | 61.7±0.7 | 65.7±1.0 | 55.6±0.6 | 55.2±0.4 | 66.1±4.3 | 60.6±1.3 |

**Solvable Win Rate:** (Reference model: ChatGPT-CoT)
| **Method** | **I1 Instruction** | **I1 Category** | **I1 Tool** | **I2 Instruction** | **I2 Category** | **I3 Instruction** | **Average** |
| --- | --- | --- | --- | --- | --- | --- | --- |
| GPT-3.5-Turbo-0613 (DFS) | 60.7 | 67.3 | 59.5 | 63.2 | 62.1 | 75.4 | 64.7 |
| GPT-4-0613 (CoT) | 54.6 | 58.8 | 58.2 | 75.5 | 60.5 | 62.3 | 61.7 |
| GPT-4-0613 (DFS) | 62.6 | 62.7 | 58.2 | 74.5 | 62.9 | 67.2 | 64.7 |
| ToolLLaMA v2 (CoT) | 31.3 | 28.1 | 33.5 | 35.8 | 33.9 | 24.6 | 31.2 |
| ToolLLaMA v2 (DFS) | 44.8 | 45.8 | 44.3 | 59.4 | 41.1 | 50.8 | 47.7 |
| GPT-3.5-Turbo-1106 (CoT) | 47.2 | 47.7 | 44.9 | 50.9 | 54.0 | 62.3 | 51.2 |
| GPT-3.5-Turbo-1106 (DFS) | 55.8 | 53.6 | 51.9 | 68.9 | 59.7 | 68.9 | 59.8 |
| GPT-4-Turbo-Preview (CoT) | 71.2 | 77.1 | 61.4 | 79.2 | 71.8 | 67.2 | 71.3 |
| GPT-4-Turbo-Preview (DFS) | **73.0** | **75.2** | **68.4** | **77.4** | **66.9** | **60.7** | **70.2** |
We run all models once against `GPT-3.5-Turbo-0613 + CoT` and evaluate them three times. We follow the ToolBench implementation to take the most frequent result for each query during evaluation.