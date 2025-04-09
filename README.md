# Text-to-Quiz

## Archives
### Data Preparation
- Train Data Prep Notebook [here](https://colab.research.google.com/drive/1HwlbcbdjzEymt5MgefRxW4Z6IpZyiuJ8?usp=sharing)
- Test Data Prep Notebook [here](https://colab.research.google.com/drive/1TFpSzV18Rb3mVjujvgSrJU2XWXpvlx8B?usp=sharing)

### Model Finetuning
- Mistral 7B notebook [here](https://colab.research.google.com/drive/1rORkY4v0-8t-hH6YyUIhq8UUess5TTXJ?usp=sharing) => `best one`
- Llama-3.2-3B notebook [here](https://colab.research.google.com/drive/1wZYCED2pJINhy5FERi571o3kea1TM0u2?usp=sharing)

### Inference Through API
Example with Gradio Interface [here](https://colab.research.google.com/drive/1heGZ7SxbnQB8EgsD1NIX3qave4m6tktn?usp=sharing)

## How to Run it
1. **Deploy Model API from Colab T4 GPU**: Run all the cells in the notebook provided in the *Inference Through API* section above
2. Copy the public URL given by gradio
3. Open the file named `main.py`
4. Paste the URL as new value for the `url` variable
5. `pip install -r requirements.txt`
6. Launch the app: `streamlit run main.py`
7. Enjoy

*Note that on T4 GPU generation takes approximately 12s per question*
