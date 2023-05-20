# llm-python
A set of instructional materials, code samples and Python scripts featuring LLMs (GPT etc) through interfaces like llamaindex, langchain, Chroma (Chromadb), Pinecone etc. Mainly used to store reference code for my LangChain tutorials on YouTube. 

<!-- <img src="assets/youtube.png" width="50%" alt="LangChain youtube tutorials" /> -->
![LangChain youtube tutorials](assets/llmseries.png)

Learn LangChain from my YouTube channel:

| Part | LLM Tutorial | Link | Video Duration |
| --- | --- | --- | --- |
| 1 | LangChain + OpenAI tutorial: Building a Q&A system w/ own text data | [Tutorial Video](https://youtu.be/DYOU_Z0hAwo) | 20:00 |
| 2 | LangChain + OpenAI to chat w/ (query)  own Database / CSV | [Tutorial Video](https://youtu.be/Fz0WJWzfNPI) | 19:30 |
| 3 | LangChain + HuggingFace's Inference API (no OpenAI credits required!) | [Tutorial Video](https://youtu.be/dD_xNmePdd0) | 24: 36 |
| 4 | Understanding Embeddings in LLMs | [Tutorial Video](https://youtu.be/6uyBc0jm1xQ) | 29:22 |
| 5 | Query any website with LLamaIndex + GPT3 (ft. Chromadb, Trafilatura) | [Tutorial Video](https://youtu.be/6K1lyyzpxtk) | 11:11 |
| 6 | Locally-hosted, offline LLM w/LlamaIndex + OPT (open source, instruction-tuning LLM) | [Tutorial Video](https://youtu.be/qAvHs6UNb2k) | 32:27 |
| 7 | Building an AI Language Tutor: Pinecone + LlamaIndex + GPT-3 + BeautifulSoup | [Tutorial Video](https://youtu.be/k8G1EDZgF1E) | 51:08 |
| 8 | Building a queryable journal 💬 w/ OpenAI, markdown & LlamaIndex 🦙 | [Tutorial Video](https://youtu.be/OzDhJOR5IfQ) | 40:29 |

The full lesson playlist can be found [here](https://www.youtube.com/playlist?list=PLXsFtK46HZxUQERRbOmuGoqbMD-KWLkOS).

### Side Lessons (good supplements to the main series above)
- [OpenAI tutorial and video walkthrough](https://youtu.be/skw-togjY7Q)

### Quick Start
1. Clone this repo
2. Install requirements: `pip install -r requirements.txt`
3. Some sample data are provided to you in the `news` foldeer, but you can use your own data by replacing the content (or adding to it) with your own text files.
4. Create a `.env` file which contains your OpenAI API key. You can get one from [here](https://beta.openai.com/). `HUGGINGFACEHUB_API_TOKEN` and `PINECONE_API_KEY` are optional, but they are used in some of the lessons.

The `.env` file should look like this:
```
OPENAI_API_KEY=your_api_key_here

# optionals (not required for most of the series)
HUGGINGFACEHUB_API_TOKEN=your_api_token_here
PINECONE_API_KEY=your_api_key_here
```
HuggingFace and Pinecone are optional but is recommended if you want to use the Inference API and explore those models outside of the OpenAI ecosystem. This is demonstrated in Part 3 of the tutorial series. 
5. Run the examples in any order you want. For example, `python 6_team.py` will run the website Q&A example, which uses GPT-3 to answer questions about a company and the team of people working at Supertype.ai. Watch the corresponding video to follow along each of the examples.

### Dependencies
As LlamaIndex and LangChain are both very new projects, if you're using the latest version of these libraries, some of the code in this repo may need small adjustment. I will try to keep this repo up to date with the latest version of the libraries, but if you encounter any issues, please let me know. The code examples are tested on LlamaIndex 0.5.7 and LangChain 0.0.157.

