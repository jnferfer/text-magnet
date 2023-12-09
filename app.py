import streamlit as st
import pandas as pd
from ast import literal_eval
from styles import *
from st_click_detector import click_detector
from streamlit_agraph import agraph, Node, Edge, Config
from about import *


def filter_links(dist_threshold, links_dict):
    """
    In data, each sentence may come with related links, but not all are useful.
    This function discards links whose relations' names are incorrect and
    similarity dist. (between sent. and linked sent.) is above the threshold.

    :param dist_threshold: Max. similarity dist. allowed between sent. and linked sent.
    :param links_dict: Dictionary with links
    :return:
    """

    allowed_rels = ["FOR_EXAMPLE", "THE_OPPOSITE_IS", "CONSEQUENCE_IS", "INTERVENTION_IS", "ADDITIONALLY", "CAUSE_IS",
                    "EQUIVALENT", "SIMILARLY"]
    filtered = {}
    for rel, links in links_dict.items():
        if rel in allowed_rels:
            remaining_links = [link for link in links if link["dist"] <= dist_threshold]
            if remaining_links:
                filtered[rel] = remaining_links

    return filtered


@st.cache_data(show_spinner=False)
def load_data_and_titles(dist_threshold=0.99, df_path="data/demo_df.csv"):
    """
    Read 'data/demo_df.csv' and return a dataframe with selected data
    a list with all titles.

    :param dist_threshold: Max. similarity dist. allowed between sent. and linked sent. from data.
    :param df_path: Source data path
    :return: Tuple with dataframe and a list of titles
    """

    data = pd.read_csv(df_path)
    data = data[["doc_id", "title", "sent_id", "sent", "links"]]
    data.fillna("", inplace=True)

    data["links"] = data["links"].apply(lambda x: literal_eval(x))
    data["links"] = data["links"].apply(lambda links: filter_links(dist_threshold, links))

    titles = sorted(set(data["title"]))

    return data, titles


def build_text(data, doc_id, clicked_sent_id):
    """
    Generate the text sentence by sentence, and apply the appropriate styles to it.

    :param data: data source to fetch sentences from
    :param doc_id: id of the doc to fetch sentences from
    :param clicked_sent_id: if True, highlight this sentence
    :return: the generated text string
    """

    if clicked_sent_id:
        clicked_sent_id = int(clicked_sent_id.split("|")[1])

    filtered = data[data["doc_id"] == doc_id]

    title = f"<h2>{filtered['title'].iloc[0]}</h2>"
    text = f"<p style='{TEXT}'>"

    zipped = list(zip(filtered["sent_id"], filtered["sent"], filtered["links"]))
    for i, (sent_id, sent, links) in enumerate(zipped):

        # Add a line break if sent. belongs to a dotted list
        if sent.startswith("- "):
            sent = f"<br>{sent}"
            if i+1 < len(zipped) and not zipped[i+1][1].startswith("- "):
                sent += "<br>"  # line break to the end if last element from dotted list

        # Add style of sent. to highlight
        if sent_id == clicked_sent_id:
            if sent.startswith("<br>"):
                sent = f"<br><mark style='{HIGHLIGHTED_SENT}'>{sent.lstrip('<br>')}</mark>"
            else:
                sent = f"<mark style='{HIGHLIGHTED_SENT}'>{sent}</mark>"

        # Add style of hyperlinks
        if not links:
            text += f"{sent} "
        else:
            text += f"<a style='{TEXT_HYPERLINK}' href='#' id='{doc_id}|{sent_id}'>{sent}</a> "

    text = title + text + "</p>"

    return text


def build_goal_text(data, doc_id, link_sent_id, color, node_label):
    """
    Generate the goal text excerpt, and apply the appropriate styles to it.

    :param data: data source to fetch sentences from
    :param doc_id: id of the doc to fetch sentences from
    :param link_sent_id: id of the sent to highlight
    :param color: color code of the dot
    :param node_label: name of the node label
    :return: the generated goal text excerpt
    """

    filtered = data[data["doc_id"] == doc_id]

    # Only an excerpt from doc is show (a context of 2 preceding sents.)
    start_sent_id = link_sent_id-2 if link_sent_id-2 >= 0 else 0
    filtered = filtered.iloc[start_sent_id:link_sent_id+1]

    title = filtered["title"].iloc[0]

    goal_text = f"<p style='{GOAL_TEXT}'><span style='{GOAL_DOT.format(color)}'>●</span> <b>{node_label}</b><br> «"

    for sent_id, sent in zip(filtered["sent_id"], filtered["sent"]):
        sent = sent.lstrip("<br>")
        if sent_id == link_sent_id:
            goal_text += f"<mark style='{HIGHLIGHTED_SENT}'>{sent}</mark> "
        else:
            goal_text += f"{sent} "

    goal_text = goal_text.rstrip() + f"» → <a href='#' id='{doc_id}'>{title}</a></p>"

    return goal_text


def add_line_breaks(text, words_num_per_line=4):
    """
    Add line breaks if text is longer than 4 words.

    :param text: Text to edit
    :param words_num_per_line: Max. num of words per line
    :return: Edited text
    """

    words = text.split()
    for i in range(0, len(words), words_num_per_line)[1:]:
        words[i] = f"{words[i]}\n"
    words[-1] = words[-1].rstrip("\n")

    return " ".join(words)


class Graph:

    def __init__(self, data):
        self.data = data
        self.config = Config(from_json="graph_config.json")

    def build(self, doc_id_sent_id):
        """
        Build the links' graph using the 'doc_id_sent_id' variable (id of the doc and id of the sent
        to fetch links from).

        :param doc_id_sent_id: id of the doc and id of the sent to fetch links from
        :return: id of the clicked node
        """

        nodes = []
        edges = []

        doc_id, sent_id = doc_id_sent_id.split("|")
        sent_id = int(sent_id)

        filtered = self.data[(self.data["doc_id"] == doc_id) & (self.data["sent_id"] == sent_id)]
        links = filtered["links"].iloc[0]
        sent = filtered["sent"].iloc[0]

        # Center node
        nodes.append(
            Node(
                id=0,
                label="",
                title=sent,
                size=NODE["size"],
                color=NODE["color"]["central"]
            )
        )

        for relation, rel_links in links.items():
            if rel_links is not None:

                # Intermediate node (node with the name of the relation)
                dists = [link["dist"] for link in rel_links]
                nodes.append(
                    Node(
                        id=relation,
                        label=NODE["relation_label"][relation],
                        title=round(sum(dists)/len(dists), 2),
                        size=NODE["size"],
                        color=NODE["color"]["intermediate"][relation]
                    )
                )

                # Join center to intermediate node
                edges.append(
                    Edge(
                        source=0,
                        target=relation
                    )
                )

                # End nodes
                end_node_labels = []
                for link in rel_links:
                    end_node_label = add_line_breaks(text=link["linked_keywords"])
                    end_node_labels.append(end_node_label)
                    end_node_label_count = end_node_labels.count(end_node_label)
                    if end_node_label_count > 1:  # add suffix for duplicated node labels
                        end_node_label = f"{end_node_label} - {end_node_label_count}"  # e.g. 'flu - 2'
                    nodes.append(
                        Node(
                            id=f"{link['linked_doc_id']}|{link['linked_sent_id']}|{NODE['color']['end'][relation]}|"
                               f"{end_node_label}",
                            label=end_node_label,
                            title=link["dist"],
                            size=NODE["size"],
                            color=NODE["color"]["end"][relation]
                        )
                    )

                    # Join intermediate to end node
                    edges.append(
                        Edge(
                            source=relation,
                            target=f"{link['linked_doc_id']}|{link['linked_sent_id']}|{NODE['color']['end'][relation]}"
                                   f"|{end_node_label}"
                        )
                    )

        # 'selected_link' stores the id of the clicked node in the graph
        selected_link = agraph(nodes=nodes, edges=edges, config=self.config)  # render graph

        return selected_link


def add_to_history(title, max_length=10):
    """
    Append a selected title to history log
    """

    st.session_state["history"].append(title)

    # Max. 'max_length' titles saved
    if len(st.session_state["history"]) > max_length:
        st.session_state["history"].pop(0)


def define_text_input_from_title_selectbox():
    """
    Callback func. to assign title from titles selectbox to st.session_state["text_input"]
    """

    st.session_state["text_input"] = data[data["title"] == st.session_state["titles_input"]]["doc_id"].iloc[0]
    add_to_history(title=st.session_state["titles_input"])
    st.session_state["clicked_sent_id"] = None  # reset
    st.session_state["titles_input"] = None  # reset


def define_text_input_from_history_selectbox():
    """
    Callback func. to assign title from history selectbox to st.session_state["text_input"]
    """
    st.session_state["text_input"] = data[data["title"] == st.session_state["history_input"]]["doc_id"].iloc[0]
    st.session_state["clicked_sent_id"] = None  # reset
    st.session_state["history_input"] = None  # reset


st.set_page_config(layout="wide")
st.set_page_config(initial_sidebar_state="expanded")


# Initialize session state's variables

for variable in ["text_input", "clicked_sent_id", "end_of_script"]:
    if variable not in st.session_state:
        st.session_state[variable] = None

if "history" not in st.session_state:
    st.session_state["history"] = []

if st.session_state["end_of_script"] == "end":
    st.session_state["clicked_sent_id"] = None  # reset
    st.session_state["end_of_script"] = None  # reset


# Load demo data

with st.spinner(text="Reading demo data"):
    data, titles = load_data_and_titles()


# Build sidebar

with st.sidebar:
    st.markdown(SIDEBAR_LOGO, unsafe_allow_html=True)
    st.image("logo.png")
    st.markdown(
        SIDEBAR_TEXT.format(
            "TextMagnet 1.0",
            "Discover hidden connections among different texts. \
            Demo with <a href='https://paperswithcode.com/dataset/medquad' target='_blank'>MedQuAD</a>"),
        unsafe_allow_html=True
    )
    st.selectbox(
        label="title",
        options=titles,
        index=None,
        on_change=define_text_input_from_title_selectbox,
        key="titles_input",
        placeholder="Titles",
        label_visibility="collapsed"
    )


# Build Explorer and About layout

explorer, about = st.tabs(["Explorer", "What is it?"])

with explorer:
    left, right = st.columns([0.5, 0.5], gap="large")
    with left:
        text = st.empty()
        goal = st.empty()
    with right:
        history = st.empty()
        graph = st.empty()

with about:
    _left, _center, _right = st.columns([0.2, 0.6, 0.2])
    with _center:
        st.markdown(SIDEBAR_LOGO, unsafe_allow_html=True)
        # st.image("iman (1).png")
        st.markdown(text1)
        st.markdown(text2)
        st.image("1.png")
        st.markdown(text3)
        st.image("2.png")
        st.markdown(text4)
        st.image("3.png")
        st.markdown(text5)
        st.markdown(text6)
        st.image("4.png")
        st.markdown(text7)
        st.image("5.png")
        st.markdown(text8)




# Build history selectbox

with history:
    st.selectbox(
        label="history",
        options=st.session_state["history"][::-1],
        index=None,
        on_change=define_text_input_from_history_selectbox,
        key="history_input",
        placeholder="↺ History",
        disabled=True if len(st.session_state["history"]) < 2 else False,
        label_visibility="collapsed"
    )


# Build text

if st.session_state["text_input"]:
    with text:
        text_output = click_detector(
            html_content=build_text(data=data, doc_id=st.session_state["text_input"],
                                    clicked_sent_id=st.session_state["clicked_sent_id"]),
            key="clicked_sent_id"
        )

    # Build graph

    if text_output:
        with graph:
            g = Graph(data=data)
            graph_output = g.build(doc_id_sent_id=text_output)

        # Build goal text

        if graph_output and "|" in graph_output:
            with goal:
                link_doc_id, link_sent_id, color, node_label = graph_output.split("|")
                goal_output = click_detector(
                    html_content=build_goal_text(data=data, doc_id=link_doc_id,
                                                 link_sent_id=int(link_sent_id), color=color, node_label=node_label),
                    key="clicked_goal"
                )

                # Build text from goal

                if goal_output:
                    st.session_state["text_input"] = goal_output
                    add_to_history(title=data[data["doc_id"] == goal_output]["title"].iloc[0])
                    del st.session_state["clicked_goal"]
                    st.session_state["end_of_script"] = "end"
                    st.rerun()
