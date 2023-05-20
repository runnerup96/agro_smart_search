import pandas as pd
import streamlit as st
import json
from finder_class import Finder, sample_object


with open("data/featureset.json", "rb") as file:
    input_data = json.load(file)

display_dict = json.load(open('data/display_dict.json', 'r'))
feature_dict = json.load(open('data/full_features_dict.json', 'r'))
finder_instance = Finder(feature_dict, display_dict)
st.header("Поисковик по лекарственным растениям")
st.subheader("👨‍🌾 Сформируйте запрос")
st.markdown("Преставленное решение разработано командой cls_token, в рамках кейса **ООО «СОЛЮШН»** хакатона \"Цифровой прорыв. Сезон: ИИ\"")

options = st.multiselect(
    "Расположение (GEO)",
    input_data["location_feature"],
    [], max_selections=5)

options1 = st.selectbox(
    'Климат',
    input_data["climate_feature"],
    )
options2 = st.selectbox(
    'Почва',
    input_data["pochva_feature"],
    )
options3 = st.multiselect(
    'Химическое вещество в растении',
    input_data["chemicals_feature"],
    [], max_selections=5)
options4 = st.checkbox('Охраняется красной книгой')

find_button = st.button("Найти")



entity_attribures = {"location_feature": list(options),
                     "climate_feature": list(options1),
                     "red_book_feature": "1" if options4 else  [],
                     "chemicals_feature": list(options3),
                     "pochva_feature": list(options2)}
st.divider()
if find_button:
    st.subheader("📈 Результат")
    result = finder_instance.search(entity_attribures)

    for x in result:
        with st.expander(x["original_name"]):
            st.write("Атрибуты документа")

            col1, col2, col3, col4, col5 = st.columns(5)

            with col1:
                st.table(pd.DataFrame(x["entity_attributes"]["location_feature"],columns=["location_feature"]))
            with col2:
                st.table(pd.DataFrame(x["entity_attributes"]["climate_feature"], columns=["climate_feature"]))
            with col3:
                st.table(pd.DataFrame(x["entity_attributes"]["pochva_feature"], columns=["pochva_feature"]))
            with col4:
                st.table(pd.DataFrame(x["entity_attributes"]["chemicals_feature"], columns=["chemicals_feature"]))
            with col5:
                st.table( pd.DataFrame(x["entity_attributes"]["red_book_feature"], columns=["red_book_feature"]))
            st.caption(x["entity_definition"])
else:
    st.write("Чтобы начать поиск, нажмите \"Найти\"")



st.caption("Powered by cls_token")


