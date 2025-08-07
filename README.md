# Detecting Propaganda in Marathi News Articles Using Machine Learning and Deep Learning Techniques

This project presents a first-of-its-kind, linguistically informed and computationally robust system for detecting propaganda in **Marathi news articles**, using both traditional machine learning and deep learning techniques. It addresses a critical gap in misinformation detection for **low-resource Indian languages** and contributes tools, datasets, and insights for regional media integrity.

---

## 📌 Table of Contents

- [Background](#background)
- [Objectives](#objectives)
- [Dataset](#dataset)
- [Methodology](#methodology)
- [Models and Evaluation](#models-and-evaluation)
- [Results](#results)
- [Linguistic Tools](#linguistic-tools)
- [Error Analysis](#error-analysis)
- [Impact](#impact)
- [Limitations](#limitations)
- [Future Work](#future-work)
- [License](#license)
- [Author](#author)

---

## 🧠 Background

Despite Marathi being spoken by over **83 million people**, computational tools for propaganda detection in the language remain underdeveloped. This project tackles:
- High linguistic complexity of Devanagari script
- Scarcity of labeled data
- Limited adaptation of modern NLP models for regional languages

The spread of **political, health, and communal propaganda** in digital Marathi media makes automated detection systems urgently necessary.

---

## 🎯 Objectives

1. Develop a labeled propaganda dataset (MPropCorpus) and lexicon (MarathiPropLex)
2. Design a custom Marathi text preprocessing pipeline
3. Benchmark 6 ML models and a BiLSTM deep learning model
4. Evaluate linguistic features including a novel **Marathi Readability Score (MRS)**

---

## 📚 Dataset

**MPropCorpus**  
- 4,309 Marathi news articles
  - 2,086 labeled as propaganda
  - 2,223 as factual
- Sources: Lokmat, NDTV Marathi, FactCrescendo
- Fields: Title, Content, URL, Source, Label

---

## ⚙️ Methodology

- **Web Scraping**: Modular pipeline using Selenium + BeautifulSoup for extracting thousands of articles
- **Text Preprocessing**:
  - Devanagari normalization
  - Domain-specific stopword removal
  - Indic tokenization
- **Feature Engineering**:
  - TF-IDF vectors (1-grams, 2-grams)
  - Stylistic markers (punctuation, emotion, complexity)

---

## 🤖 Models and Evaluation

### 🧪 Machine Learning Models
| Model              | Accuracy | F1 Score | AUC    | Training Time |
|-------------------|----------|----------|--------|----------------|
| XGBoost           | 99.4%    | 99.5%    | 99.5%  | 88.6s          |
| MLP               | 99.4%    | 99.4%    | 99.4%  | 29.4s          |
| SVM (Linear)      | 99.3%    | 99.3%    | 99.3%  | 0.6s           |

### 🧠 Deep Learning (BiLSTM)
- 2 BiLSTM layers (128 + 64 units)
- Embedding size: 128
- Parameters: 11.9M
- F1 Score: **99.88%**
- Inference Time: <1s/article

---

## 📈 Results

- Near-perfect performance across both ML and DL models
- Emotionally charged and linguistically complex articles more likely to be propaganda
- Readability:
  - Propaganda MRS: 10.35
  - Factual MRS: 10.34
- Custom `MarathiTextProcessor` significantly improved model performance by reducing noise and handling complex script issues

---

## 🧰 Linguistic Tools

### MarathiPropLex
- 1,200+ annotated propaganda terms
- Labeled with techniques like:
  - Name Calling
  - Fear Appeals
  - Glittering Generalities

### Marathi Readability Score (MRS)
```text
MRS = -2.34 + 2.14 × Avg Word Length + 0.01 × Polysyllabic Words
```
## 🧐 Error Analysis
- False Positives: Factual articles with emotive language (e.g., disaster reports)

- False Negatives: Subtle satire or rhetorical content

- Suggestions:

  - Add NER and topic modeling

  - Use time-aware training to detect propaganda evolution
## 🌍 Societal Impact
- Journalists: Instant classification and alerts

- Policy Makers: Regional moderation assistance

- Media Platforms: Real-time flagging of manipulative narratives

- Includes built-in ethical safeguards:

  - Human-in-the-loop review

  - Political bias audits

  - Model transparency reports
## ⚠️ Limitations
- Currently supports only binary classification

- Limited to modern standard Marathi (no dialects)

- High-performance DL models require GPU support

- No real-time deployment in current form
## 🔮 Future Work
- Extend to multi-label classification of propaganda techniques

- Support for code-mixed content (Hindi, English, Marathi)

- Integrate Explainable AI (SHAP, LIME) for transparency

- Deploy as browser plugin or journalist dashboard

- Incorporate temporal modeling for election cycles or viral surges
##  📄 License
This project is licensed under the MIT License – see the LICENSE file for details.
## 👤 Author
**Manjul Mayank**
- M.Tech in Artificial Intelligence & Data Science
- Indian Institute of Technology (IIT) Patna
- Under guidance of **Dr. Sriparna Saha**
- 🔗 GitHub: manjul-mayank


