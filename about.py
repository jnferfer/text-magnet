text1 = """
These three sentences are similar:
1. *Olive oil has omega-3.*
2. *Canola oil has vitamin E.*
3. *The omega-3 in olive oil reduces cholesterol.*

**TextMagnet** is an algorithm based on Natural Language Processing that not only recognizes the similarity between these three sentences but also **identifies which similarity is relevant**. In other words, the algorithm identifies which ideas are more strongly attracted to each other. In this case, it discerns the relevant connection between the first and third sentences, suggesting the conclusion that *olive oil reduces cholesterol*.

This is a tool for **exploring hidden connections within a set of texts**. Version 1.0 serves as a demo using simple medical texts to showcase the functionality of our TextMagnet reasoning engine. TextMagnet automatically identified relationships within a set of approximately 1000 texts. In Version 2.0, users will be able to upload their own text files to investigate how different ideas can relate to each other, addressing use cases such as **knowledge discovery** or **fact checking**.

Our goal is to build a generic engine that facilitates contrasting ideas in large datasets **to combat misinformation or exponentially increase knowledge on a specific topic**.
"""

text2 = """
### Usage Instructions
- Select the title of a document from the left dropdown menu. Sentences underscored in the selected text have links to other sentences in different texts expressing similar ideas. Click on any of these sentences to reveal a graph of related ideas.
- Related ideas are logically grouped in the knowledge graph, using a label that describes the type of relationship between the compared ideas.
- Click on each node in the graph to go to an excerpt of the related text.
- Hover the mouse over each node to see a measure of distance (cosine distance) between the two compared sentences. The comparison is more reliable with a smaller distance.
"""

text3 = """
### Warning
This app is not optimized for mobile devices. The information provided should not be used for medical purposes.
&nbsp;
&nbsp;
### About the Author
You can contact me via LinkedIn for any suggestions regarding the development of this application on my [profile](https://es.linkedin.com/in/juanff)
"""