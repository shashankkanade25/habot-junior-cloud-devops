# ☁️ HabotConnect — Cloud & DevOps Engineering Hiring Project

<p align="center">
  <img src="https://img.shields.io/badge/GCP-Cloud-4285F4?style=for-the-badge&logo=googlecloud&logoColor=white"/>
  <img src="https://img.shields.io/badge/Terraform-IaC-7B42BC?style=for-the-badge&logo=terraform&logoColor=white"/>
  <img src="https://img.shields.io/badge/GitHub_Actions-CI%2FCD-2088FF?style=for-the-badge&logo=githubactions&logoColor=white"/>
  <img src="https://img.shields.io/badge/Gitleaks-Security-EF4444?style=for-the-badge&logo=github&logoColor=white"/>
  <img src="https://img.shields.io/badge/Django-REST-092E20?style=for-the-badge&logo=django&logoColor=white"/>
  <img src="https://img.shields.io/badge/Python-Validation-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
</p>

<p align="center">
  <b>Secure Infrastructure • Fail-Closed CI/CD • Deterministic Validation</b>
</p>

<p align="center">
  <i>HabotConnect FZCO — Junior Cloud & DevOps Engineer Hiring Project</i>
</p>

<p align="center">
  <a href="#-overview">Overview</a> •
  <a href="#-architecture">Architecture</a> •
  <a href="#️-task-1--terraform-infrastructure">Task 1</a> •
  <a href="#-task-2--poka-yoke-cicd">Task 2</a> •
  <a href="#-task-3--django--dcyn-validation">Task 3</a> •
  <a href="#-screenshots--execution-proof">Proof</a> •
  <a href="#-testing--quality">Testing</a>
</p>

---

## 🎯 Overview

This repository contains my implementation for the **HabotConnect Cloud & DevOps Engineering Hiring Project**.

The solution is built around three engineering controls:

| Challenge | Implementation |
|---|---|
| ☁️ Cloud Infrastructure | Terraform + GCP |
| 🔐 Secure CI/CD | GitHub Actions + Gitleaks + fail-closed quality gates |
| 🧠 Deterministic Validation | Django REST Framework + DCYN |

> **Design principle:** Secure → Automated → Deterministic → Reproducible

---

## 🏗️ Architecture

<img src="docs/screenshots/HabotConnect%20Architecture.png" alt="HabotConnect Architecture">

### CI/CD Quality Gate

```text
Developer
   │
   ▼
GitHub
   │
   ▼
GitHub Actions
   │
   ├── Terraform fmt / validate
   ├── Gitleaks
   ├── Ruff
   └── Django Tests
          │
       PASS / BLOCK
          │
          ▼
   Approved Changes
```

### Cloud Data Layer

```text
Terraform
   │
   ▼
GCS — D0 Raw Landing
   │
   ▼
Validation / Processing
   │
   ▼
BigQuery — D1 Staged / Enforced
   │
   └── Row-Level Security
```

### Application Validation Layer

```text
Student JSON
     │
     ▼
Django REST Framework
     │
     ├── Field Validation
     ├── Cross-Field Validation
     └── DCYN Rules
              │
          ┌───┴───┐
          ▼       ▼
       ACCEPT   REJECT
```

> **Note:** Terraform configuration and planning were validated. Final GCP provisioning was constrained by project permissions/APIs on the provided environment.

---

## ☁️ Task 1 — Terraform Infrastructure

### GCP resources defined

- 🪣 **GCS D0 Raw Landing Bucket**
- 🗄️ **BigQuery D1 Staged/Enforced Dataset + Table**
- 👤 **Dedicated Pipeline Service Account**
- 🔐 **Conditional IAM Binding**
- 🛡️ **BigQuery Row-Level Security**
- ♻️ **Bucket Versioning + Lifecycle Rules**

### D0 Raw Landing Security Controls

- Uniform bucket-level access
- Public access prevention
- Object versioning
- Lifecycle configuration
- Conditional object-level read controls

### D1 Staged/Enforced Controls

`student_onboarding` table includes:

- `student_id`
- `student_name`
- `email`
- `country`
- `organization_id`

Row access policy (RLS) enforces:

```sql
organization_id = 'habot'
```

### Terraform verification commands

```bash
terraform fmt -check -recursive
terraform init -backend=false
terraform validate
terraform plan
```

---

## 🔐 Task 2 — Poka-Yoke CI/CD

The GitHub Actions workflow implements a **fail-closed security and quality gate**.

### Pipeline stages

```text
Git Push / Pull Request
          │
          ▼
Terraform fmt
          │
          ▼
Terraform init
          │
          ▼
Terraform validate
          │
          ▼
Gitleaks Secret Scan
          │
          ▼
Python Dependencies
          │
          ▼
Ruff Lint
          │
          ▼
Django Tests
          │
          ▼
     Final Gate
      /      \
    PASS    BLOCK
```

### Secret detection demonstration

A test secret fixture was intentionally used to validate the control:

```text
API_KEY="sk-test-1234567890abcdefghijklmnop"
```

- Gitleaks detected it
- workflow failed
- change was blocked
- after cleanup, pipeline passed

### Why fail-closed?

- Security failure → stop pipeline  
- Quality failure → stop pipeline  
- Validation failure → stop pipeline  

---

## 🧠 Task 3 — Django + DCYN Validation

Validation stack:

- 🐍 Python
- Django
- Django REST Framework
- `ModelSerializer`
- Cross-field rule validation
- Deterministic DCYN library
- Automated tests

### Example payload

```json
{
  "student_name": "Shashank Kanade",
  "email": "shashankkanade07@gmail.com",
  "age": 12,
  "country": "India",
  "has_learning_difficulty": true,
  "requires_learning_support": true,
  "parental_consent": true
}
```

### Validation rules

| Field | Rule |
|---|---|
| `student_name` | Required, 2–100 chars |
| `email` | Required, valid email, max 254 |
| `age` | Required integer, 3–18 |
| `country` | Required, 2–56 chars |
| Boolean fields | Required |

### Cross-field consistency rule

```text
requires_learning_support = TRUE
AND
has_learning_difficulty = FALSE
        ↓
      REJECT
```

---

## 🧠 DCYN Decision Library

| Rule | Field | YES | NO |
|---|---|---|---|
| DCYN-01 | `has_learning_difficulty` | `true` | `false` |
| DCYN-02 | `requires_learning_support` | `true` | `false` |
| DCYN-03 | `parental_consent` | `true` | `false` |

```text
Same Input + Same Rules = Same Decision
```

---

## 📸 Screenshots & Execution Proof

| Evidence | Screenshot |
|---|---|
| **Gitleaks blocking leaked secret (fail-closed gate)** | ![Gitleaks Fail](docs/1.png) |
| **Django tests passing (9/9)** | ![Django Tests Pass](docs/2.png) |
| **Clean security gate (no leaks detected)** | ![Gitleaks Clean Pass](docs/3.png) |
| **Terraform plan output evidence** | ![Terraform Plan](docs/4.png) |

> These screenshots provide execution proof for CI security behavior, application test quality, and infrastructure planning.

---

## 🧪 Testing & Quality

### Django Tests

```text
Found 9 test(s).
.........
Ran 9 tests in 0.111s

OK
```

✅ 9 / 9 tests passed

### Ruff

```bash
ruff check django_app
```

```text
All checks passed!
```

### Security

- ✅ Gitleaks failure demonstrated
- ✅ Clean Gitleaks run demonstrated

### Terraform

- ✅ `fmt` validated
- ✅ `init` validated
- ✅ `validate` passed
- ✅ `plan` generated

---

## 📁 Repository Structure

```text
habot-junior-cloud-devops/
│
├── .github/
│   └── workflows/
│       └── ci.yml
├── terraform/
│   ├── main.tf
│   ├── variables.tf
│   └── terraform.tfvars.example
├── django_app/
│   ├── dcyn.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   └── migrations/
├── django_project/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── schema/
│   └── schema_mapping.xlsx
├── docs/
│   ├── habotconnect-architecture.png
│   ├── 1.png
│   ├── 2.png
│   ├── 3.png
│   └── 4.png
├── manage.py
├── requirements.txt
└── README.md
```

---

## 🧰 Technology Stack

| Category | Tools |
|---|---|
| ☁️ Cloud | Google Cloud Platform, GCS, BigQuery |
| 🏗️ IaC | Terraform |
| 🔄 CI/CD | GitHub Actions |
| 🔐 Security | Gitleaks, IAM Conditions, Row-Level Security |
| 🐍 Backend | Python, Django, Django REST Framework |
| 🧪 Testing | Django Test Framework, Ruff |
| 📊 Documentation | Markdown, Excel, Architecture Diagram |

---

## 🔒 Security Principles

- **Least Privilege:** Dedicated service identity + scoped IAM
- **Fail Closed:** Any failed gate blocks promotion
- **Secret Protection:** Gitleaks enforces no hardcoded secrets
- **Defense in Depth:** IAM + CI/CD + scanning + data access + app validation
- **Deterministic Rules:** Code-driven decisions, not manual interpretation

---

## 📦 Deliverables

| Deliverable | Location |
|---|---|
| Terraform Infrastructure | `terraform/main.tf` |
| Terraform Variables | `terraform/variables.tf` |
| CI/CD Pipeline | `.github/workflows/ci.yml` |
| DRF Serializer | `django_app/serializers.py` |
| DCYN Library | `django_app/dcyn.py` |
| Automated Tests | `django_app/tests.py` |
| Schema Mapping | `schema/schema_mapping.xlsx` |
| Architecture Diagram | `docs/habotconnect-architecture.png` |
| Execution Proof Screenshots | `docs/1.png` to `docs/4.png` |
| Documentation | `README.md` |

---

## 👨‍💻 Author

**Shashank Kanade**  
**Junior Cloud & DevOps Engineer | Cloud Engineer | SRE**

📧 [shashankkanade07@gmail.com](mailto:shashankkanade07@gmail.com)  
📱 7820963908  
📍 Pune, Maharashtra, India

---

<p align="center">
  ☁️ <b>Secure Infrastructure</b> &nbsp;•&nbsp;
  🔐 <b>Fail-Closed Automation</b> &nbsp;•&nbsp;
  🧠 <b>Deterministic Decisions</b> &nbsp;•&nbsp;
  🧪 <b>Reproducible Engineering</b>
</p>

<p align="center">
  <i>Built for the HabotConnect Cloud & DevOps Engineering Hiring Project.</i>
</p>
