# ☁️ HabotConnect — Cloud & DevOps Engineering Challenge

<p align="center">
  <strong>Production-oriented Cloud Infrastructure • Secure CI/CD • Deterministic Data Validation</strong>
</p>

<p align="center">
  <a href="https://github.com/shashankkanade25/habot-junior-cloud-devops">
    <img src="https://img.shields.io/badge/GitHub-Repository-181717?style=for-the-badge&logo=github" alt="GitHub">
  </a>
  <a href="https://github.com/shashankkanade25/habot-junior-cloud-devops/actions">
    <img src="https://img.shields.io/badge/CI%2FCD-Passing-2ea44f?style=for-the-badge&logo=githubactions" alt="CI/CD">
  </a>
  <img src="https://img.shields.io/badge/Infrastructure-Terraform-844FBA?style=for-the-badge&logo=terraform" alt="Terraform">
  <img src="https://img.shields.io/badge/Cloud-Google%20Cloud-4285F4?style=for-the-badge&logo=googlecloud" alt="Google Cloud">
  <img src="https://img.shields.io/badge/Python-Django%20%2B%20DRF-092E20?style=for-the-badge&logo=django" alt="Django">
</p>

<p align="center">
  <a href="#-overview">Overview</a> •
  <a href="#-architecture">Architecture</a> •
  <a href="#-task-1--cloud-infrastructure">Task 1</a> •
  <a href="#-task-2--poka-yoke-cicd">Task 2</a> •
  <a href="#-task-3--dcyn-validation">Task 3</a> •
  <a href="#-testing">Testing</a>
</p>

---

## 🎯 Overview

This repository contains my implementation for the **Junior Cloud & DevOps Engineer (GCP / Django / React)** hiring challenge for **HabotConnect FZCO**.

The solution focuses on three engineering principles:

> **Infrastructure as Code + Fail-Closed Automation + Deterministic Data Validation**

The implementation covers:

- ☁️ Google Cloud infrastructure provisioned using **Terraform**
- 🔐 IAM and access controls designed around **least privilege**
- 🗄️ Google Cloud Storage raw landing architecture
- 📊 BigQuery staged/enforced data layer
- 🛡️ BigQuery Row-Level Security
- 🚦 Poka-Yoke CI/CD pipeline using GitHub Actions
- 🔎 Automated secret detection using **Gitleaks**
- 🐍 Django REST Framework schema validation
- ✅ Deterministic **DCYN (Yes/No) decision library**
- 🧪 Automated validation tests
- 📋 Schema mapping documentation in Excel format

---

## 🏗️ Architecture

```text
                         ┌──────────────────────────┐
                         │      Developer Commit     │
                         │       / Pull Request      │
                         └────────────┬─────────────┘
                                      │
                                      ▼
                         ┌──────────────────────────┐
                         │    GitHub Actions CI     │
                         │     Poka-Yoke Gate       │
                         └────────────┬─────────────┘
                                      │
                ┌─────────────────────┼─────────────────────┐
                │                     │                     │
                ▼                     ▼                     ▼
        ┌──────────────┐      ┌──────────────┐      ┌──────────────┐
        │ Terraform    │      │   Gitleaks   │      │    Ruff      │
        │ fmt/validate │      │ Secret Scan  │      │ Python Lint  │
        └──────┬───────┘      └──────┬───────┘      └──────┬───────┘
               │                     │                     │
               └─────────────────────┼─────────────────────┘
                                     ▼
                            ┌─────────────────┐
                            │  Django Tests   │
                            │    9 / 9 PASS   │
                            └────────┬────────┘
                                     │
                              ┌──────┴──────┐
                              │             │
                            PASS           FAIL
                              │             │
                              ▼             ▼
                           APPROVE        BLOCK
                                           🚫
