# Chapter 2 – Imbalance Bars Implementation

This project implements **Dollar Imbalance Bars** from *Advances in Financial Machine Learning*.

## 📁 Project Structure

* `data/` → contains datasets
* `notebooks/` → Jupyter notebooks
* `src/` → Python scripts

## ⚙️ Setup

1. Install Python (3.8+ recommended)

2. Install dependencies:

```
pip install -r requirements.txt
```

3. Run Jupyter:

```
jupyter notebook
```

4. Open the notebook:

```
notebooks/2019-04-11_OP_Dollar-Imbalance-Bars.ipynb
```

## 📊 Data

Place your dataset in:

```
data/imbalance_bars_3_100000.csv
```

## 🧠 Description

This project generates imbalance bars by sampling trades based on **order flow imbalance** rather than fixed time intervals.

## ▶️ Example

Run the Python script:

```
python src/imbalance_bars.py
```
