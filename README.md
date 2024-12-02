
<div align="center">
<img src="./images/Logo.png" alt="pipeline"/>
</div>

<div align="center">

[![GitHub stars](https://img.shields.io/github/stars/PhamTrinhDuc/Chatbot-Mental-Health-with-Llamaindex)](https://github.com/PhamTrinhDuc/Chatbot-Mental-Health-with-Llamaindex/stargazers)[![GitHub issues](https://img.shields.io/github/issues/PhamTrinhDuc/Chatbot-Mental-Health-with-Llamaindex)](https://github.com/PhamTrinhDuc/Chatbot-Mental-Health-with-Llamaindex/issues)

# MENTAL HEALTH WITH LLAMAINDEX

</div>


## **To Install This Application, Follow These Steps:**

#### Step 1. Clone the repository:
    git clone https://github.com/PhamTrinhDuc/Chatbot-Mental-Health-with-Llamaindex.git
    cd Chatbot-Mental-Health-with-Llamaindex

#### Step 2. (Optional) Create and activate a virtual environment:
- For Unix/macOS:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

- For Windows:
```bash
python -m venv venv
.\venv\Scripts\activate
```
- Conda:
```bash
conda create -n <env_name> python=<python_version> 
conda activate env_name
```

#### Step 3. Before starting your application, you need to fill in some evironment variables. Create a `.env` file and fill in these
```bash
OPENAI_API_KEY = "sk-dojvF..."
```

#### Step 4. Install the necessary libraries for the project 
```bash
pip install -r requirements.txt
```

#### Step 5. Chat interface
```bash
python test_code.py # ingest data
streamlit run Home🏠.py
```