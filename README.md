<h1 align="center">
  CHeaT&nbsp;🛡️— Cloak • Honey • Trap
</h1>

<p align="center">
  <a href="#-tool-quick-start">Quick&nbsp;Start</a> •
  <a href="#-repository-layout">Repo&nbsp;Layout</a> •
  <a href="#-paper">Paper</a> •
  <a href="#-datasets">Datasets</a> •
  <a href="#%EF%B8%8F-ctf-machines)">CTF&nbspMachines</a> •
  <a href="#-token-landmines">Token&nbsp;Landmines</a> •
  <a href="#-demo-notebook">Demo&nbsp;Notebook</a> •
  <a href="#-citation">Citation</a>
</p>

---

## 🌟 Project Overview
CHeaT (Cloak–Honey–Trap) is a research toolkit that **defends networks against autonomous LLM-powered pentesting agents** by:

1. **Cloaking** sensitive data with misdirection  
2. Planting **Honey** tokens to detect & fingerprint LLM agents  
3. Setting **Traps** that stall or crash abusive agents  

All techniques are described in our USENIX Security ’25 white-paper and implemented in a light-weight CLI.

---

## 🚀 Tool Quick Start

> **TL;DR**

```bash
# clone repo & enter tool folder
git clone https://github.com/your-user/CHeaT.git
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

## 📂 Repository Layout

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

---

## 📜 Paper

The full methodology, threat model, and evaluation are in **“Cloak, Honey, Trap: Proactive Defenses Against LLM Agents.”**
Read the PDF or check the arXiv link in the paper header for details.
Key numbers:

* 6 strategies / 15 techniques
* 11 CTF machines
* Works even with GPT-4o back-end agents

---

## 📊 Datasets

Directory **`datasets/`** collects:

---

## 🖥️ CTF Machines

Ready-to-import OVA VMs used in the paper’s evaluation:

* `UbuntuX`, `VulBox`, `Shocker`, …
* Each folder contains **`README.md`** with flag locations & solution.

---

## 💣 Token Landmines

`token-landmines/` provides per-model rare-token sequences that induce hallucinations or context collapse.
Use them in **Trap T4.4** or study robustness across models.

---

## 📒 Demo Notebook

Launch the Jupyter notebook in `demo-notebook/` to:

* Step through the white-paper experiments
* Mix-and-match techniques live
* Sandbox to play in

---

## 📄 License

MIT © 2025 Ayzenshteyn • Weiss • Mirsky

---

## 🤝 Citation

For citations:

```bibtex
@inproceedings{Ayzenshteyn2025CHeaT,
  title={{CHeaT}: Cloak, Honey, Trap – Proactive Defenses Against LLM Agents},
  author={Daniel Ayzenshteyn and Roy Weiss and Yisroel Mirsky},
  booktitle={USENIX Security},
  year={2025}
}
```

Happy trapping! 🕸️
