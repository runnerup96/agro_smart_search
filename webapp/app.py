import pandas as pd
import streamlit as st
import json
from finder_class import Finder


input_data = json.load(open("/app/argo_smart_search/webapp/data/featureset.json", "rb"))
display_dict = json.load(open('/app/argo_smart_search/webapp/data/display_dict.json', 'r'))
feature_dict = json.load(open('/app/argo_smart_search/webapp/data/full_features_dict.json', 'r'))
popularity_dict = json.load(open('/app/argo_smart_search/webapp/data/popularity_dict.json', 'r'))
finder_instance = Finder(feature_dict, display_dict, popularity_dict)
original_title = '<h2 style="color:#165A02;">Agrosearch: поисковик по лекарственным растениям</h2>'
st.markdown(original_title, unsafe_allow_html=True)
st.markdown("Преставленное решение разработано командой cls_token, в рамках кейса **ООО «СОЛЮШН»** хакатона \"Цифровой прорыв. Сезон: ИИ\"")
st.subheader("👨‍🌾 Сформируйте запрос")

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



entity_attribures = {"location_feature": list(location_feature),
                     "climate_feature": list(climate_feature),
                     "red_book_feature": "1" if red_book_feature else [],
                     "chemicals_feature": list(chemicals_feature),
                     "soil": list(soil),
                     "source_type": list(source_type),
                     "calendar_month": list(calendar_month),
                     "max_type": list(max_type)}
st.divider()
if find_button:
    st.subheader("📈 Результат")
    result = finder_instance.search(entity_attribures)

    for x in result:
        with st.expander(x["original_name"]):
            st.write("Атрибуты документа")
            st.markdown("**Метрика схожести документа и запроса:  " + str(round(x["search_score"], 2))+"**")

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
else:
    st.write("Чтобы начать поиск, нажмите \"Найти\"")

st.caption("Powered by cls_token")


