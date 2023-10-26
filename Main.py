import grammarly
import openai
import RhetoricalFunction
import streamlit as st
import wordchoice
from st_pages import Page, show_pages, add_page_title
from streamlit import session_state
from format import web_info

original_content = ""
if "show_topic" not in session_state:
    selected_image_url = " "
    session_state.show_topic = {
        "content": original_content,
        "image_url": selected_image_url,
    }

if "submit_revise_query" not in session_state:
    session_state.submit_revise_query = ""


def main():
    web_info()
    # Title
    col1, col2 = st.columns([4, 1])
    with col1:
        st.title("🦊 I'd Rather Be a CleverFox")
    with col2:
        # Change language of the website
        language = session_state.submit_revise_query = st.radio('Language', ["TN", "EN", "JP"], horizontal=True)

    # Import OpenAI API key
    input_key = st.secrets["api_key"]
    openai.api_key = input_key
    st.divider()

    # Main Body
    col1, col2 = st.columns([3, 1])
    default_article = "Water shortage has been a serious problem for many years and causes various crises. The land is crushing, overusing the underground water, and many people can’t get enough water, swarming the water cart like thirsty animals. All of these sounds horrible. Climate change, the biggest cause of environmental problems. Earth has become hotter and hotter these years, and the climate is getting extremely hot. No typhoons, less rain, both of them cause water shortages. All in all, the problem above is all because of yourself, and the only solution is also to attend to us. From now on, save water whenever possible, enhance education, and cherish our mother earth. I hope the world will be better."
    # Left page：article
    with col1:
        subcol1, subcol2 = st.columns([2, 1])
        with subcol1:
            write_area = {
                "EN": "Writing Area",
                "TN": "寫作區",
                "JP": "書き込みエリア",
            }
            st.subheader(write_area[language])

        with subcol2:
            # Exit Test Zone Button
            if session_state and (session_state.show_topic["content"] != original_content):
                if st.button("Exit Test Zone", on_click=run):
                    refresh_mainpage()

        # Writing area
        expander_msg = {
            "EN": "Tap to close or open",
            "TN": "點選以開啟或閉合",
            "JP": "押して開閉",
        }
        with st.expander(expander_msg[language], expanded=True):
            # Synchronize testZone content
            if session_state and (session_state.show_topic["content"] != original_content):
                st.write(session_state.show_topic["content"])
                if session_state.show_topic["image_url"] != " ":
                    st.image(
                        session_state.show_topic["image_url"],
                        # caption="歷屆考古試題",
                        use_column_width=True,
                    )
            else:
                # Input raw article
                st.write(original_content)

            # Upload PDF file
            upload_msg = {
                "EN": "Upload article（PDF file only）",
                "TN": "上傳 PDF 檔",
                "JP": "PDF ファイルをアップロードする",
            }
            uploaded_file = st.file_uploader(upload_msg[language], type="pdf", accept_multiple_files=True)
            for uploaded_file in uploaded_file:
                bytes_data = uploaded_file.read()
                # st.write("filename:", uploaded_file.name)
                # st.write(bytes_data)
            # Input article
            ori_essay = {
                "EN": "Article:",
                "TN": "原始文章：",
                "JP": "原始の書き込み",
            }
            text = st.text_area(ori_essay[language], default_article)

    with col2:
        revise = {
            "EN": "Revise for",
            "TN": "批改功能",
            "JP": "訂正機能",
        }
        st.subheader(revise[language])
        grammar = {
            "EN": "grammar",
            "TN": "文法",
            "JP": "文法",
        }
        word_level_up = {
            "EN": "word level up",
            "TN": "單詞等級提升",
            "JP": "単語レベルの向上",
        }
        rhetorical_analysis = {
            "EN": "rhetorical analysis",
            "TN": "轉折語分析",
            "JP": "転折句の分析",
        }
        revise_topic = st.radio("select one of them", [grammar[language], word_level_up[language], rhetorical_analysis[language]])

    # output edited article
    if not text:
        st.error('no article')
    else:
        if revise_topic == grammar[language]:
            grammarly.grammar(text)

        if revise_topic == word_level_up[language]:
            level = wordchoice.select_level()
            wordchoice.choice(text, level)

        if revise_topic == rhetorical_analysis[language]:
            RhetoricalFunction.process_article(text)


def run():
    st.session_state.run = True


def refresh_mainpage():
    # 清空 session_state.show_topic 前先檢查是否存在
    session_state.show_topic = {
        "content": "",
        "image_url": " ",
    }
    st.session_state.run = False
    # 使用 st.experimental_rerun() 重新運行整個應用程序
    st.experimental_rerun()


if __name__ == "__main__":
    main()
