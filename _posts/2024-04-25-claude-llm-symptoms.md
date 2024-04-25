---
title:  "Symptom Diagnosis with Claude LLM"
date:   2024-04-25 15:18:25 -0500
categories:
- ai
- ml
- llm
- python
- claude
- sklearn
author: steven
---

# Symptom Diagnosis with Claude LLM
_Building an Interactive Diagnostic Tool with Claude's LLM API and Jupyter Widgets_

![](https://raw.githubusercontent.com/git-steven/git-steven.github.io/master/assets/images/claude-diagnose-md.png)

## Introduction
In the field of healthcare, early and accurate diagnosis plays a crucial role in providing effective treatment to patients. With the advancements in artificial intelligence (AI) and natural language processing (NLP), it is now possible to create intelligent diagnostic tools that can assist medical professionals and empower patients. In this article, we will explore how to build a _basic_ interactive diagnostic tool using Claude's LLM API, the Python Anthropic package, and Jupyter Widgets.

## Prerequisites

### Claude account and API key
Go to the [Anthropic Console](https://console.anthropic.com/settings/keys) to create your key.  If you haven't created a [Claude](https://claude.ai/) account yet, do it when prompted to; it's easy!

### Python Packages
To get started, make sure you have Python and Jupyter Notebook installed on your machine. You will also need the Anthropic package, which provides a convenient way to interact with Claude's LLM API.  We'll also need jupyter widgets.  They can all be installed via:

```bash
pip install anthropic jupyterlab jupyterlab-widgets ipywidgets
```

## Jupyter notebook 
Start jupyter lab and create a new Jupyter Notebook:
```bash
  jupyter lab
```

Create a new cell (as below) to:
* Import necessary code from modules
* Create the [anthropic](https://pypi.org/project/anthropic/) `Client` with your `API_KEY`.  In this example, it is stored in an environment variable so it is not published with this example.  
* Create the basic `diagnose` function, which accepts a string of symptoms, which can be separated by commas.  This function uses the [anthropic](https://pypi.org/project/anthropic/) `Client` to communicate with the Claude API to obtain a basic diagnosis.  


```python
import os

import anthropic
from ipywidgets import widgets
from IPython.display import display

client = anthropic.Client(api_key=os.getenv('CLAUDE_API_SECRET'))

PROMPT = """
Given the following symptoms: "{}", what are the possible diagnoses?
"""
def diagnose(symptoms):
    prompt = PROMPT.format(symptoms)
    message = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return message.content
```

## User Interface
_Creating the User Interface with Jupyter Widgets_
Now, let's create an interactive user interface using Jupyter Widgets to accept symptoms from the user and display the possible diagnoses.

In the cell below, we create a simple UI with 3 components:
* a text area widget for entering symptoms
* a submit widget for triggering the diagnosis via the local `on_submit_click` function.
* an output widget for displaying the results


```python
DISCLAIMER_MSG = "Please note that this is not a definitive"
DISCLAIMER_MSG += " diagnosis. Always consult a healthcare"
DISCLAIMER_MSG += " a healthcare professional for proper evaluation"
DISCLAIMER_MSG += " and treatment."
SYMPTOM_LBL = "Describe your symptoms, separated by commas..."

def symptom_checker_widget():
    """
    An interactive interface, created with Jupyter widgets
    """

    caption = widgets.HTML("<h3>Diagnostics via Claude</h3>")
    
    symptom_input = widgets.Textarea(
        description='Symptoms',
        placeholder=SYMPTOM_LBL,
        layout={'width':'80%', 'height':'80px'}
    )
    
    diagnose_button = widgets.Button(description="Diagnose")
    output = widgets.Output(layout={
        'border': '1px solid black',
        'min_height':'80px',
    })
    output.append_stdout('Diagnosis will appear here.')

    def on_submit_click(b):
        with output:
            output.clear_output()
            print('Diagnosing...')
            symptoms = symptom_input.value
            diagnosis = diagnose(symptoms)
            possible_conditions = [m.text for m in diagnosis]            
            for condition in possible_conditions:
                print(f"- {condition}")
            print(f"\n\nDISCLAIMER_MSG")
            

    diagnose_button.on_click(on_submit_click)

    display(caption, symptom_input, diagnose_button, output)
```

# Running the tool
To run the interactive diagnostic tool, execute the following cell, which simply calls the `symptom_checker_widget` function defined above. The user interface will appear, allowing users to enter their symptoms and click the "Diagnose" button to receive possible diagnoses based on the symptoms provided.


```python
symptom_checker_widget()
```

```bash
    HTML(value='<h3>Diagnostics via Claude</h3>')



    Textarea(value='', description='Symptoms', layout=Layout(height='80px', width='80%'), placeholder='Describe yo…



    Button(description='Diagnose', style=ButtonStyle())



    Output(layout=Layout(border_bottom='1px solid black', border_left='1px solid black', border_right='1px solid b…
```

## Conclusion
In this article, we explored how to build an interactive diagnostic tool using Claude's LLM [API](https://docs.anthropic.com/claude/reference/client-sdks), the Python [Anthropic](https://pypi.org/project/anthropic/) package, and [Jupyter Widgets](https://ipywidgets.readthedocs.io/). By leveraging the power of AI and NLP, we created a simple interface that accepts symptoms and provides possible diagnoses.

This diagnostic tool can serve as a valuable resource for both medical professionals and patients, aiding in the early identification of potential health issues. However, it is essential to note that this tool is not a substitute for professional medical advice and should be used in conjunction with proper medical evaluation and treatment.  
  
It is also by no means a complete diagnostics tool.  As you continue to develop and refine the diagnostic tool, consider incorporating additional features such as symptom validation, medical terminology recognition, and integration with medical knowledge bases to enhance its accuracy and usability.  You might also consider tracking the diagnostic session, so it can be conversational and used to refine a diagnosis.  Another feature that might be useful is suggesting other symptoms that might appear along with the submitted ones.  This is useful for a patient who doesn't remember all the symptoms, or might think they aren't worth mentioning.  

Remember to handle user input securely, ensure the privacy of sensitive health information, and provide appropriate disclaimers regarding the limitations and intended use of the diagnostic tool.

By combining the power of Claude's LLM API, Python, and Jupyter Widgets, you can create innovative healthcare applications that have the potential to revolutionize patient care and empower individuals to take a more active role in managing their health.
