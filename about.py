import streamlit as st


about_this_demo_subheading = "About this demo"
about_this_demo_1_2 = """
**TextMagnet** is a reasoning engine, based on Natural Language Processing (NLP), that searches through various text sources looking for connections between related ideas. This is a small app that demonstrates how this engine works with a selection of simple medical texts.

But first of all, **what do we mean by related ideas**? If one text on *cataracts* explains that *a cataract is a clouding of the lens in your eye*, and another text on *surgery* says that *surgery helps you see clearly again*, then the second idea is related to the first, and there is a (hidden) connection of ideas between both texts."""

about_this_demo_2_2 = """
The current version 1.0 is a demo in which related ideas have been identified in more than 1100 simple generic medical texts. The result is a **knowledge graph** that interlinks these ideas, which can be checked in this demo.

Version 2.0 will allow users to upload a set of texts of their choice on specific topics, so they can explore related ideas among them, discover hidden connections, and draw conclusions that they would not be able to obtain with a linear reading of the texts, one by one.
"""

possible_use_cases_subheading = "Possible use cases"
possible_use_cases = """
Our goal is to build a generic reasoning engine based on language comprehension, that makes it easier to contrast information in large data volumes. TextMagnet aims to be a useful tool in **fact-checking** and **knowledge discovery**, as specific use cases.

It is also a support for **Retrieval Augmented Generation** (RAG) systems, which use information retrieval as a bridge between an external information source and the applications of large language models (LLMs). This combination is necessary for LLMs to be useful tools that help us increase our knowledge on a specific topic, and to critically evaluate new information we receive.
"""

architecture_subheading = "The architecture"
architecture_1 = """
TextMagnet is an NLP engine that reasons about the **similarity of two sentences** (their semantic proximity). Specifically, it identifies whether there is a coherence relationship between two close-in-meaning sentences.

Let's say we want to find text similar to the following snippet, which is our query:

> *Panic disorder is a type of anxiety disorder*

Current search systems encode text as numbers (vectors or [embeddings](https://theinformationlab.nl/2023/03/22/an-introduction-to-embeddings/)) to locate nearby texts within a context area. Here are some examples of contextually close snippets related to our query, which can be retrieved by these systems:

> *Schizophrenia is one type of psychotic disorder*  

> *Panic disorder is more common in women than men*  

> *Obsessive-compulsive disorder is a type of anxiety disorder*  

> *It causes panic attacks*  

> *Insomnia is a common sleep disorder*  

> *For some people, fear takes over their lives and they cannot leave their homes*  

> *Stress caused by anxiety can also make it hard for you to breathe*  

> *Sometimes it starts when a person is under a lot of stress*  

> *Medicines can also help*  

&nbsp;  
As we will see, TextMagnet first utilizes a contextualization module to avoid ambiguities (as in *Medicines can also help*) and enhance the search for similar texts. It locates, among all these examples, those that maintain coherence with the query. For this to happen, there must be a logical and relevant connection between the compared pair, as the *Logical relation* column shows.
&nbsp;  
&nbsp;  
&nbsp;  
| Text (unambiguous) | Cosine dist. | Logical relation |
|-----------|-----------|-----------|
| Schizophrenia is one type of psychotic disorder | 0.58 | :x: |
| Panic disorder is more common in women than men | 0.36 | :white_check_mark: |
| Obsessive-compulsive disorder is a type of anxiety disorder | 0.31 | :white_check_mark: |
| Panic disorder causes panic attacks | 0.44 | :white_check_mark: |
| Insomnia is a common sleep disorder | 0.65 | :x: |
| For some people, fear of panic attacks takes over their lives and they cannot leave their homes | 0.49 | :x: |
| Stress caused by anxiety can make it hard for you to breathe | 0.59 | :x: |
| Panic disorder sometimes starts when a person is under a lot of stress | 0.41 | :white_check_mark: |
| Medicines can help with panic disorder | 0.43 | :white_check_mark: |

&nbsp;  
&nbsp;  
NLP systems that look for similar text use word embeddings to calculate the distance between two texts (using, for example, cosine distance). This approach allows us to find texts that share vector spaces, in other words, that occur in very similar contexts. For this reason, *Insomnia is a common sleep disorder* is similar to *Panic disorder is a type of anxiety disorder*. Both occur in common contexts.
"""

architecture_2 = """
However, the sum of both snippets is not coherent; the meaning of one does not add anything relevant to the other. For this to happen, there must be a coherence relationship between compared texts. That is, both meanings must complement each other and follow a line of reasoning. This combination of meanings is exactly what TextMagnet looks for - coherence relationships between texts where the distance between their embeddings is close. 

In our example, if *panic disorder is a type of anxiety*, then
- the cause can be *a person is under a lot of stress*;
- the consequence is *panic attacks*;
- one form of treatment is *medicines*;
- and similarly, *obsessive-compulsive disorder* is another type of anxiety disorder.

These are all **logical relations** between the query and some of the semantically close texts.

To achieve this, we have worked on two fronts: **context** and **relationships**. Each constitutes an original module of the engine (Contextualizer and Relation Reasoner), supported by a vector database that transforms the text into embeddings. For this, we have based our work on a foundational model (GPT 3.5 by OpenAI) that is fine-tuned for several tasks and trained with specific knowledge.
"""

architecture_3 = """
**The Contextualizer**

The first front concerns context, which is a major obstacle in systems that look for similar text. Looking at the sentences from our previous examples, we can see that many are out of context. For example: *Sometimes it starts when a person is under a lot of stress* (what does *it* refer to?), *Medicines can also help* (what do they help with?).

We need to transform these sentences into **standalone units of meaning**, that can be understood on their own:

> *Sometimes __it__ starts when a person is under a lot of stress* → *Sometimes __panic disorder__ starts when a person is under a lot of stress*  

> *Medicines can also help* → *Medicines can also help __with panic disorder__*

This way, the comparison makes sense; otherwise, we might be connecting snippets from different contexts, for example related to asthma but not anxiety or panic disorders. This is something we have tried to solve by teaching LLMs like GPT 3.5 to convert context-dependent sentences to context-independent sentences.

**The Reasoner**

The second front involves identifying the **type of logical relationship** between two close texts. For this, we have based our work on training a foundational model (GPT 3.5 by OpenAI) to recognize coherence relationships, and textual entailment relevance. The study of these relationships is not new; in Linguistics, they are known as coherence relations.

Therefore, TextMagnet consists of two fundamental modules to search for related ideas: one module capable of **isolating a sentence from its context and transforming it into an independent unit of meaning**, and another module that **connects this idea with others with which it may maintain a coherence relationship**.
"""

graphs_subheading = "About the graphs"
graphs_1 = """
Coherence relations describe the connection two sentences maintain. If this connection is logical, then it makes sense for the sentences to appear together. One complements the other; they seem to attract each other. For systems like ours, based on statistics and not on the common sense emanating from experience, it is not always easy to deduce this connection. In this sense, TextMagnet is an experiment on the capacity of such statistical models to relate ideas.

The 1.0 version displays intuitive graphs showing the current performance of the engine. As you can see in the demo, the nodes of related ideas are organized around an initial set of relationships that currently are: *__Example__*, *__Cause__*, *__Consequence__*, *__Similarity__*, *__Explanation__* (i.e. added information), *__Opposite__*, *__Equivalence__*, *__Intervention__* (i.e. treatment). Improving the engine involves training it in different contexts (not just medical or health) and seeing how this set expands to more relationships. There is not an infinite set of relationships anyway, as linguistic theory ([Rhetorical Structure Theory](https://www.sfu.ca/rst/01intro/intro.html)) has already demonstrated.
"""
graphs_2 = """
On the other hand, each of these relationships can play a role depending on the use case. In a medical context, for example, you can check with *Intervention* how different ideas are connected to a query (and extract different forms of treatment for a medical condition). Or in fact-checking, it is useful to see how one idea can be the opposite of another, or diverge substantially to identify cases of misinformation.

When browsing through the graph, hovering the mouse over each node displays a distance metric between the vectors of the original and compared sentences. The engine tends to be more reliable the smaller the distance between them (cosine distance).
"""

future_work_subheading = "Future work"
future_work = """
The current demo allows navigating a simple knowledge graph of related ideas. We intend to **keep improving the engine** and make it more generic so that it can be adapted with little effort (training) in other fields and for different use cases. We also want to learn about new and specific use cases that could benefit from systems like ours. The related ideas graph is based on simple health texts extracted from a set of informative texts for non-experts, and therefore the "discoveries" are very trivial because they are based on very basic knowledge (for example, that surgery cures cataracts). But it will be interesting to see what we can find by crossing more specific texts, with new and original content, like research articles for instance.
"""

warning_subheading = "Warning"
warning = """
This app is not optimized for mobile devices. The information provided should not be used for medical purposes.
"""

author_subheading = "About the author"
author = """
The code for the demo (not the engine's training models, which are currently kept private) can be found on [this GitHub profile](https://github.com/jnferfer/text-magnet).

You can contact me for any suggestions regarding the development of this application on my [LinkedIn profile](https://www.linkedin.com/in/juanff/) or by [e-mail](mailto:jnferfer@gmail.com).

Juan Fernández, 2023
"""


def build_about():
    st.subheader(about_this_demo_subheading, anchor="1")
    st.markdown(about_this_demo_1_2)
    st.image("imgs/related_ideas.svg", width=550)
    st.markdown(about_this_demo_2_2)
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader(possible_use_cases_subheading, anchor="2")
    st.markdown(possible_use_cases)
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader(architecture_subheading)
    st.markdown(architecture_1)
    st.image("imgs/vector_space.svg", width=590)
    st.markdown(architecture_2)
    st.image("imgs/architecture.svg", width=590)
    st.markdown(architecture_3)
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader(graphs_subheading)
    st.markdown(graphs_1)
    st.image("imgs/graph.svg", width=520)
    st.markdown(graphs_2)
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader(future_work_subheading)
    st.markdown(future_work)
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader(warning_subheading)
    st.markdown(warning)
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader(author_subheading)
    st.markdown(author)
