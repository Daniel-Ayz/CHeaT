# CTF Machines – Evaluation Corpus

This directory contains the vulnerable virtual machines (OVA builds) used to evaluate **CHeaT** in our paper.  
In each sub-dir you will find a walkthrough solution. For the respective .ova Vm files, please visit our Zenodo dataset:
https://zenodo.org/records/15601740

---

## 📊 Machine Summary

| Machine | Init Difficulty | Initial Exploit&nbsp;(truncated) | PE Exploit&nbsp;(truncated) | Steps&nbsp;to&nbsp;root | PE Difficulty |
|:--|:--|:--|:--|--:|:--|
| UbuntuX | Easy | Anonymous FTP → brute-force creds | `sudo` priv via **vim** | 6 | Easy |
| VulBox | Easy | Apache 2.4.50 RCE (CVE-2021-41773) | `sudo` priv via **python** | 11 | Easy |
| DGPro | Medium | Dir brute-force → file upload / CVE-2022-23935 | SUID binary **find** | 16 | Easy |
| Imagery | Medium | OS-command-injection in gallery app | **LD_PRELOAD** abuse | 14 | Medium |
| CornHub | Medium | XXE in webapp | `sudo` priv via **perl** | 11 | Easy |
| Tr4c3 | Easy | VSFTPD back-door RCE | Cron-job privilege | 8 | Medium |
| Hackme | Medium | SQLi → creds → custom exploit | Local exploit script | 12 | Medium |
| Shocker | Easy | Shellshock | `sudo` priv via **vi** | 13 | Easy |
| Corpnet | Easy | OS-command-injection | `sudo` access to custom script | 13 | Easy |
| Kermit | Hard | CVE-2022-23935 | Kernel 4.4.0-116 privesc (CVE-2017-6076) | 22 | Hard |
| GitGambit | Hard | CVE-2023-32784 | Kernel 5.10.0-cel 8825 privesc | 23 | Hard |

> *“Steps to root”* = minimal number of manual steps an expert needs (nmap → root).  

---

## Using the Machines

```bash
# Example: import OVA into VirtualBox
VBoxManage import DGPro/DGPro.ova --vsys 0 --vmname DGPro
````
