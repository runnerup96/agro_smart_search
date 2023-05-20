import pandas as pd
import streamlit as st
import json
from finder_class import Finder
from PIL import Image

st.set_page_config(page_title="Agrosearch", page_icon="👨‍🌾")

def load_json_data(file_path: str) -> dict:
    """Load JSON data from a file."""
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data


def display_search_results(result: dict) -> None:
    """Display search results in the Streamlit app."""
    st.subheader("📈 Результат")

    for x in result:
        with st.expander(x["original_name"]):
            st.write("Атрибуты документа")
            st.markdown("**Метрика схожести документа и запроса:  " + str(round(x["search_score"], 2)) + "**")

            col1, col2, col3, col4, col5 = st.columns(5)
            col6, col7, col8 = st.columns(3)

            with col1:
                input_to_table = x["entity_attributes"]["location_feature"]
                st.table(pd.DataFrame(input_to_table[:min(len(input_to_table), 10)], columns=["location_feature"]))
            with col2:
                st.table(pd.DataFrame(x["entity_attributes"]["climate_feature"], columns=["climate_feature"]))
            with col3:
                st.table(pd.DataFrame(x["entity_attributes"]["soil"], columns=["soil"]))
            with col4:
                input_to_table = x["entity_attributes"]["chemicals_feature"]
                st.table(pd.DataFrame(input_to_table[:min(len(input_to_table), 10)], columns=["chemicals_feature"]))
            with col5:
                st.table(pd.DataFrame(x["entity_attributes"]["red_book_feature"], columns=["red_book_feature"]))
            with col6:
                st.table(pd.DataFrame(x["entity_attributes"]["calendar_month"], columns=["calendar_month"]))
            with col7:
                st.table(pd.DataFrame(x["entity_attributes"]["max_type"], columns=["max_type"]))
            with col8:
                st.table(pd.DataFrame(x["entity_attributes"]["calendar_month"], columns=["calendar_month"]))

            st.caption(x["entity_definition"])


@st.cache_data
def initialize_finder(root_path: str = "") -> Finder:
    """Initialize the Finder instance."""

    feature_dict = load_json_data(root_path + 'data/full_features_dict.json')
    display_dict = load_json_data(root_path + 'data/display_dict.json')
    popularity_dict = load_json_data(root_path + 'data/popularity_dict.json')
    return Finder(feature_dict, display_dict, popularity_dict)



ROOT_PATH = "/app/argo_smart_search/webapp/data/"
# Load input data
input_data = load_json_data(ROOT_PATH + "data/featureset.json")

# Initialize Finder instance
finder_instance = initialize_finder(ROOT_PATH)

col, col1 = st.columns([1, 5])
# Attach image
image = Image.open(ROOT_PATH + 'images/test.png')
col.image(image)

# Set up Streamlit UI

original_title = '<h2 style="color:#165A02;">Agrosearch: поисковик по лекарственным растениям</h2>'
col1.markdown(original_title, unsafe_allow_html=True)
st.markdown(
    "Преставленное решение разработано командой cls_token, в рамках кейса **ООО «СОЛЮШН»** хакатона \"Цифровой прорыв. Сезон: ИИ\" 🦖.")
st.subheader("👨‍🌾 Сформируйте запрос")

# Get user input
location_feature = st.multiselect(
    "Расположение (GEO)",
    input_data["location_feature"],
    [], max_selections=5)
climate_feature = st.multiselect(
    'Климат',
    input_data["climate_feature"],
    [], max_selections=5)
soil = st.multiselect(
    'Почва',
    input_data["soil"],
    [], max_selections=5)
chemicals_feature = st.multiselect(
    'Химическое вещество в растении',
    input_data["chemicals_feature"],
    [], max_selections=5)
source_type = st.multiselect(
    'Вид сырья',
    input_data["source_type"],
    [], max_selections=5)
calendar_month = st.multiselect(
    'Календарь сбора, мес.',
    input_data["calendar_month"],
    [], max_selections=5)
max_type = st.multiselect(
    'Максимальный срок хранения, год',
    input_data["max_type"],
    [], max_selections=5)
red_book_feature = st.checkbox('Охраняется красной книгой')

find_button = st.button("Найти")

entity_attributes = {
    "location_feature": list(location_feature),
    "climate_feature": list(climate_feature),
    "red_book_feature": "1" if red_book_feature else [],
    "chemicals_feature": list(chemicals_feature),
    "soil": list(soil),
    "source_type": list(source_type),
    "calendar_month": list(calendar_month),
    "max_type": list(max_type)
}

st.divider()

if find_button:
    result = finder_instance.search(entity_attributes)
    display_search_results(result)
else:
    st.write("Чтобы начать поиск, нажмите \"Найти\"")

st.caption("Powered by cls_token")
