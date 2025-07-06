# AI Projects – Web Scraping & Fake Job Detection

This repository contains two applied data science projects demonstrating data extraction, weak labeling, and natural language processing (NLP) using Python. The projects simulate regulatory use cases such as identifying unauthorized online service ads and detecting fraudulent job postings.

---

## Project 1: Detecting Unauthorized Electrical Work Ads on Classified Platforms

### Objective
To identify potentially unauthorized electrical service advertisements posted on public classified platforms by extracting unstructured data and using weak AI-based labeling techniques.

### Data Collection
- Target Platform: [Locanto Australia](https://www.locanto.com.au)
- Scraped 420 advertisements using requests and BeautifulSoup.

### Extracted Fields
- Title  
- Description  
- Contact Info    
- Location  
- Posting Date

### Weak Labeling via LLM
- Labeled ads using [Ollama](https://ollama.com) running the gemma:3n model locally.
- Designed **few-shot prompts** that included:
  - 1–2 labeled examples of legitimate vs. unauthorized job ads
  - Follow-up instruction for binary classification
- Prompt output was parsed into binary "legitimate" / "unauthorized" tags.
- **Results**:
  - 9 ads (~2%) labeled as suspicious — consistent with expectations, but likely under-detected.

### Observations & Limitations
- Despite prompt tuning and few-shot formatting, the **small model size** meant:
  - Weak contextual understanding
  - Limited grasp of subtle phrases or slang
  - Hallucinations or misclassifications
- This highlights the **need for larger models** or supervised training with domain-specific data.

### Future Enhancements
- Build a labeled corpus using human-verified annotations and weakly labeled seeds.
- Explore fine-tuning open LLMs like Mistral or LLaMA for classification accuracy.
- Use embeddings to detect clusters of suspicious ads and recurring phone numbers or phrases.
- Integrate data pipelines with public license registries to cross-check legitimacy.

---

## Project 2: Fake Job Posting Detection (Kaggle Dataset)

### Objective
To build an NLP-based classification model that identifies fraudulent job advertisements using classical machine learning and data balancing.

### Dataset
- Source: [Fake Job Postings Dataset – Kaggle](https://www.kaggle.com/datasets/shivamb/real-or-fake-fake-jobposting-prediction)
- Features include title, description, requirements, and company profile.
- Labels: Real or Fake

### Methodology
1. **Preprocessing**:
   - Cleaned and combined textual fields.
   - Removed stop words, punctuation, and standardized text.

2. **Feature Engineering**:
   - Applied TF-IDF vectorization using unigrams and bigrams.

3. **Handling Class Imbalance**:
   - Used **SMOTE** (Synthetic Minority Oversampling Technique) to balance fake and real job samples in the training set.

4. **Models Used**:
   - Logistic Regression
   - Random Forest

## Model Performance Summary

Trained and evaluated both Logistic Regression and Random Forest classifiers on a SMOTE-balanced dataset to detect fraudulent job postings.

###  Logistic Regression
| Metric        | Value   |
|---------------|---------|
| Best CV Score | 0.886   |
| Test AUC      | 0.852   |
| Accuracy      | 0.822   |
| Precision     | 0.125   |
| Recall        | 0.689   |
| F1-Score      | 0.212   |
| Best Params   | C=0.063, L2 regularization |

- High AUC and strong recall (~0.69) make it suitable when identifying fraud is prioritized.
- Low precision indicates many false positives, a trade-off common in fraud detection.

### Random Forest
| Metric        | Value   |
|---------------|---------|
| Best CV Score | 0.837   |
| Test AUC      | 0.744   |
| Accuracy      | 0.963   |
| Precision     | 0.412   |
| Recall        | 0.156   |
| F1-Score      | 0.226   |
| Best Params   | max_depth=17, n_estimators=170, min_samples_split=2, min_samples_leaf=1 |

- High accuracy and better precision, but recall (~0.16) is too low for reliable fraud detection.
- Suitable when false positives are more costly than misses.

###  Summary

Logistic Regression is the better choice when maximizing fraud capture (recall) is the priority. Random Forest offers better precision but misses many fraudulent postings. Future steps include:
- Threshold tuning or class-weight adjustments
- Enhanced feature engineering
- Transition to transformer-based models (e.g., BERT) for improved contextual understanding

### Observations & Limitations
- Classical models were effective given balanced training data.
- No extensive hyperparameter tuning was conducted due to time constraints.
- TF-IDF is sparse and may miss contextual nuances.

### Future Enhancements
- Explore threshold adjustment and probability calibration for precision-recall balance.
- Apply grid search or Bayesian optimization for model tuning.
- Explore transformer-based models like BERT for better context understanding.
- Incorporate sentence embeddings, entity recognition, or graph-based features.

---

##  Tools & Libraries

- Python 3.10  
- pandas, numpy  
- BeautifulSoup, requests  
- scikit-learn  
- imbalanced-learn (SMOTE)  
- matplotlib, seaborn  
- Ollama (local LLM inference)

---

## Summary

These projects demonstrate two distinct real-world AI pipelines:
- **Project 1**: Scraping and labeling unstructured online data for regulatory inspection.
- **Project 2**: Applying NLP and supervised learning to structured public data.

They reflect core data science capabilities in data wrangling, model experimentation, and practical AI application for safety and fraud detection.

---

## Author

**Joslin Maria Thomas**  
Email: joslinmariathomas94@gmail.com  
