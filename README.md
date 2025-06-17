<h1 align="center">
  CHeaT&nbsp;🛡️— Cloak • Honey • Trap
</h1>

<p align="center">
  <a href="#1-overview">Paper</a> •
  <a href="#2-tool-quick-start">Quick&nbsp;Start</a> •
  <a href="#3-repository-layout">Repo&nbsp;Layout</a> •
  <a href="#32-datasets">Datasets</a> •
  <a href="#33-ctf-machines">CTF&nbsp;Machines</a> •
  <a href="#34-token-landmines">Token&nbsp;Landmines</a> •
  <a href="#35-demo-notebook">Demo&nbsp;Notebook</a> •
  <a href="#5-citation">Citation</a>
</p>


---

## 1. Overview

**CHeaT (Cloak–Honey–Trap)** is a command-line tool designed to **defend networks against autonomous, LLM-powered penetration testing agents**. It works by embedding string-based payloads into network assets—payloads specifically crafted to **disrupt, deceive, and detect** such agents.

### Core Defense Strategies:

1. **Cloaking** – Obfuscate sensitive data with strategic misdirection
2. **Honey** – Embed tokens to detect and fingerprint LLM-driven agents
3. **Traps** – Deploy inputs that stall, confuse, or crash malicious automation

CHeaT implements **6 distinct strategies** encompassing **15 payload generation techniques**, forming a layered, proactive defense against LLM-based threats.


For more information on how it works, please see our USENIX Security ’25 publication:

``
Daniel Ayzenshteyn, Weiss, Roy, and Yisroel Mirsky. "Cloak, Honey, Trap: Proactive Defenses Against LLM Agents" 34th USENIX Security Symposium (USENIX Security 25). 2025.‏
``

---

## 2. Tool Quick Start 🚀

> **TL;DR**

```bash
# clone repo & enter tool folder
git clone https://github.com/Daniel-Ayz/CHeaT.git
cd CHeaT

# optional: create venv
python3 -m venv .venv && source .venv/bin/activate

# install (pure-stdlib -> nothing to pull)
pip install -e .

# plant a random defense in a test HTML
echo "<html><body>Hello</body></html>" > /tmp/test.html
cheat --action plant --details '{
  "assettype": "web_file",
  "file_path": "/tmp/test.html",
  "technique": "random",
}'
````

| Action              | Example                                                                                                  |
| ------------------- | -------------------------------------------------------------------------------------------------------- |
| **Plant**           | `cheat --action plant --details '{"assettype":"local_file","file_path":"readme.txt","technique":"S1i"}'` |
| **List installed**  | `cheat --action list --type installed`                                                                   |
| **Remove by ID**    | `cheat --action remove --id "<uuid>"`                                                                    |
| **Remove all**      | `cheat --action remove_all`                                                                              |
| **Point to alt DB** | `cheat ... --database /path/to/db`                                                                       |

See [`cheat/README.md`](cheat/README.md) for full CLI docs.

---

## 3. Repository Layout 

```
CHeaT/
├─ cheat/               ← Python package (tool)
│   ├─ database/        ← default JSON techniques & templates
│   └─ ...
├─ datasets/            ← datasets used in the paper evaluations
├─ ctf-machines/        ← ready-to-run vulnerable VMs
├─ token-landmines/     ← unicode landmines
├─ demo-notebook/       ← Jupyter walkthrough & sandbox
├─ Whitepaper.pdf       ← full academic paper
└─ README.md            ← you are here
```



### 3.1 ``cheat/``

Here you will find the source code to the CHeaT payload injection tool, along with instructions in [`cheat/README.md`](cheat/README.md)

### 3.2 ``datasets/``

In this directory, you will find the datasets used in the paper's evaluations.

Directory **`datasets/`** collects:

```
datasets/
├─ dataset_main.json
├─ dataset_boosted_with_pi.json
├─ dataset_unicode_honeytokens.json
└─payloads/
  ├─ payloads.json
  └─ payloads_boosted_with_prompt_injection.json
````

* **`payloads.json`** – the framed payloads constructed in the paper.  
* **`payloads_boosted_with_prompt_injection.json`** – payloads that are *boosted* with a prompt-injection wrapper.  
* **`dataset_main.json`** – embeds the framed payloads at multiple target data points and system prompts (uses `payloads.json`).  
* **`dataset_boosted_with_pi.json`** – identical structure but built from the boosted payloads.
* **`dataset_unicode_honeytokens`** – dataset used to evaluate the honeytokens (Set A and Set B in T3.2)
  


### 3.3 ``ctf-machines/``

This directory holds the 11 CTF machines (ready-to-import OVA VMs) created for the paper and used in the paper’s evaluation:

`UbuntuX`, `VulBox`, `DGPro`, `Imagery`, `CornHub`, `Tr4c3`, `Hackme`, `Shocker`, `Corpnet`, `Kermit`, `GitGambit`

In each subdirectory, you will find a walkthrough solution. For the respective .ova VM files, please visit our Zenodo dataset.

https://zenodo.org/records/15601740

If you use these CTFs in your work, please cite our paper.



### 3.4 ``token-landmines/``

Here you will find the code used to generate the “landmine tokens” from the paper. Token landmines are rare sequences of tokens that corrupt a model's internal state, causing it to output gibberish or hallucinations.

The contents of this folder will remain empty for one month after publication, allowing vendors time to patch their LLM services.



### 3.5 ``demo-notebook/``

Here you will find a Jupyter notebook which you can use to poke and prod PentestGPT in a safe sandbox:

- Load saved attack snapshots,
- Drop in new hints/traps,
- Watch how the agent reasons and what commands it generates.

---

## 4. License 📄

This project is licensed under the CC BY-NC 4.0 License. Please take a look at the [LICENSE](./LICENSE) file for details.

---

## 5. Citation

If you use our code, datasets, or CTF VMs, please cite us:

```bibtex
@inproceedings{Ayzenshteyn2025CHeaT,
  title={Cloak, Honey, Trap: Proactive Defenses Against LLM Agents},
  author={Daniel Ayzenshteyn and Roy Weiss and Yisroel Mirsky},
  booktitle={USENIX Security},
  year={2025}
}
```


Happy trapping! 🕸️
