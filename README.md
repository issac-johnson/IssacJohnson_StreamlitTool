### Streamlit Data-Cleansing, Profiling \& ML Tool



#### Author: Issac Johnson

#### URL : https://datalensaitool.streamlit.app/


***1. Stack Choices (Polars vs Pandas)***



For this project, I chose **Polars** as the primary data processing library because it is fast, memory-efficient, and scales better with large datasets compared to Pandas. One of its biggest advantages is **lazy execution**, which means transformations are only applied when required, helping to save time during data-cleaning steps.

That said, **Pandas** is still used in specific cases. For example, the data profiling module works best with Pandas, so I converted the Polars LazyFrame to a Pandas DataFrame where necessary. Pandas is also handy for quick type checks and for displaying previews in Streamlit.

***2. Data Profiling Integration***



The profiling functionality is implemented using **ydata-profiling**, as mentioned in the assignment. Since this library operates on Pandas DataFrames, the LazyFrame is converted before generating the report. The profiling output includes:

* Dataset statistics
* Correlation matrices
* Missing values summary
* Additional dataset insights



**Please note** : In the live Streamlit application, the profiling report is displayed directly within the interface for user convenience,
                  home.py serves as the entry point for the Streamlit application 

***3. ML Model Use-Case***



The machine learning section uses a **scikit-learn** model trained on the well-known Titanic dataset ([Kaggle link](https://www.kaggle.com/c/titanic/data)). The goal is to predict whether a passenger survived based on features such as age, class, and gender.

To optimize performance, the trained model is stored using **joblib**, allowing it to be loaded instantly without retraining. On the ML prediction page, users can enter feature values and receive predictions in real-time.



***4. Tips for Handling Large Files \& Optimizing Performance***



While building this application, I followed these practices to improve performance and handle large datasets efficiently:

* Use **Polars LazyFrame** for data cleaning to defer computations until necessary.
* Select only the columns you truly need early in the process.
* Convert to Pandas only when required (e.g., for profiling).
* Avoid generating full profiling reports for extremely large datasets.
* Use Streamlit filters (sliders, multiselect, etc.) to reduce the dataset before heavy operations.



##### **References**



While building this project, I referred to the following official resources and documentation:



* **Python** – [https://docs.python.org/3/](https://docs.python.org/3/)
* **Polars** – [https://pola-rs.github.io/polars/](https://pola-rs.github.io/polars/)
* **Pandas** – [https://pandas.pydata.org/](https://pandas.pydata.org/)
* **Streamlit** – [https://docs.streamlit.io/](https://docs.streamlit.io/)
* **ydata-profiling** – [https://ydata-profiling.ydata.ai/docs/master/index.html](https://ydata-profiling.ydata.ai/docs/master/index.html)
* **scikit-learn** – [https://scikit-learn.org/stable/](https://scikit-learn.org/stable/)
* **PyArrow** – [https://arrow.apache.org/docs/python/](https://arrow.apache.org/docs/python/)
* **Joblib** – [https://joblib.readthedocs.io/](https://joblib.readthedocs.io/)
* **Titanic Dataset (Kaggle)** – [https://www.kaggle.com/c/titanic/data](https://www.kaggle.com/c/titanic/data)
