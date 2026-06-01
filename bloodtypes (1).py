import pandas as pd
import streamlit as st

st.title("👍這是期末報告")
import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 網頁基本配置
st.set_page_config(page_title="全球各國血型大數據分析系統", layout="wide")

# 2. 智慧讀取、自動中文化與清洗數據
@st.cache_data
def load_and_process_data():
    # 智慧嘗試多種常見編碼讀取 CSV
    encodings = ['utf-8-sig', 'utf-8', 'big5', 'gbk']
    df = None
    for enc in encodings:
        try:
            df = pd.read_csv("bloodtypes.csv", encoding=enc)
            break
        except Exception:
            continue
            
    if df is None:
        st.error("❌ 無法讀取 `bloodtypes.csv`，請確認檔案是否存在且路徑正確。")
        st.stop()

    # 清除所有欄位名稱前後可能存在的空白或隱藏字元
    df.columns = df.columns.str.strip()
    
    # 智慧定位前三欄：
    # 如果你的 CSV 本來就內建「中文名稱」（前三欄分別是：中文名稱, Country, 人口）
    # 如果只有英文（前兩欄是：Country, 人口），程式會自動調適
    if '中文名稱' in df.columns:
        col_zh_name = '中文名稱'
        col_en_name = 'Country'
        col_pop_num = '人口'
    else:
        # 防呆：如果沒有自帶中文欄位，則自動透過英中字典生成
        col_en_name = df.columns[0]  # 第一欄：Country (英文)
        col_pop_num = df.columns[1]  # 第二欄：人口
        
        # 全球主要國家英中對照字典
        country_translation = {
            "Albania": "阿爾巴尼亞", "Algeria": "阿爾及利亞", "Argentina": "阿根廷", "Armenia": "亞美尼亞",
            "Australia": "澳洲", "Austria": "奧地利", "Azerbaijan": "亞塞拜然", "Bahrain": "巴林",
            "Bangladesh": "孟加拉", "Belarus": "白俄羅斯", "Belgium": "比利時", "Bhutan": "不丹",
            "Bolivia": "玻利維亞", "Bosnia and Herzegovina": "波士尼亞與赫塞哥維納", "Brazil": "巴西",
            "Bulgaria": "保加利亞", "Cambodia": "柬埔寨", "Cameroon": "喀麥隆", "Canada": "加拿大",
            "Chile": "智利", "China": "中國", "Colombia": "哥倫比亞", "Costa Rica": "哥斯大黎加",
            "Croatia": "克羅埃西亞", "Cuba": "古巴", "Cyprus": "塞浦路斯", "Czech Republic": "捷克",
            "Denmark": "丹麥", "Dominican Republic": "多明尼加", "Ecuador": "厄瓜多", "Egypt": "埃及",
            "El Salvador": "薩爾瓦多", "Estonia": "愛沙尼亞", "Ethiopia": "衣索比亞", "Fiji": "斐濟",
            "Finland": "芬蘭", "France": "法國", "Georgia": "喬治亞", "Germany": "德國",
            "Ghana": "迦納", "Greece": "希臘", "Guatemala": "瓜地馬拉", "Honduras": "宏都拉斯",
            "Hong Kong": "香港", "Hungary": "匈牙利", "Iceland": "冰島", "India": "印度",
            "Indonesia": "印尼", "Iran": "伊朗", "Iraq": "伊拉克", "Ireland": "愛爾蘭",
            "Israel": "以色列", "Italy": "義大利", "Jamaica": "牙買加", "Japan": "日本",
            "Jordan": "約旦", "Kazakhstan": "哈薩克", "Kenya": "肯亞", "Kuwait": "科威特",
            "Latvia": "拉脫維亞", "Lebanon": "黎巴嫩", "Libya": "利比亞", "Lithuania": "立陶宛",
            "Luxembourg": "盧裝堡", "Malaysia": "馬來西亞", "Mauritius": "模里西斯", "Mexico": "墨西哥",
            "Moldova": "摩爾多瓦", "Mongolia": "蒙古", "Montenegro": "蒙特內哥羅", "Morocco": "摩洛哥",
            "Myanmar": "緬甸", "Nepal": "尼泊爾", "Netherlands": "荷蘭", "New Zealand": "紐西蘭",
            "Nicaragua": "尼加拉瓜", "Nigeria": "奈及利亞", "North Korea": "北韓", "North Macedonia": "北馬其頓",
            "Norway": "挪威", "Oman": "阿曼", "Pakistan": "巴基斯坦", "Panama": "巴拿馬",
            "Papua New Guinea": "巴布亞紐幾內亞", "Paraguay": "巴拉圭", "Peru": "秘魯", "Philippines": "菲律賓",
            "Poland": "波蘭", "Portugal": "葡萄牙", "Puerto Rico": "波多黎各", "Qatar": "卡達",
            "Romania": "羅馬尼亞", "Russia": "俄羅斯", "Saudi Arabia": "沙烏地阿拉伯", "Serbia": "塞爾維亞",
            "Singapore": "新加坡", "Slovakia": "斯洛伐克", "Slovenia": "斯洛維尼亞", "Somalia": "索馬利亞",
            "South Africa": "南非", "South Korea": "南韓", "Spain": "西班牙", "Sri Lanka": "斯里蘭卡",
            "Sudan": "蘇丹", "Sweden": "瑞典", "Switzerland": "瑞士", "Syria": "敘利亞",
            "Taiwan": "台灣", "Thailand": "泰國", "Tunisia": "突尼西亞", "Turkey": "土耳其",
            "Uganda": "烏干達", "Ukraine": "烏克蘭", "United Arab Emirates": "阿拉伯聯合大公國",
            "United Kingdom": "英國", "United States": "美國", "Uruguay": "烏拉圭", "Uzbekistan": "烏茲別克",
            "Venezuela": "委內瑞拉", "Vietnam": "越南", "Yemen": "葉門", "Zambia": "尚比亞", "Zimbabwe": "辛巴威"
        }
        df['國家中文名稱'] = df[col_en_name].map(country_translation).fillna(df[col_en_name])
        col_zh_name = '國家中文名稱'

    # 其餘欄位定義為標準 8 種血型組合欄位
    standard_blood_cols = ['O+', 'A+', 'B+', 'AB+', 'O-', 'A-', 'B-', 'AB-']
    blood_cols = [c for c in standard_blood_cols if c in df.columns]
    
    # 安全地轉換數值型態
    df[col_pop_num] = pd.to_numeric(df[col_pop_num], errors='coerce').fillna(0).astype(int)
    for col in blood_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(float)
        
    # 寬表格轉長表格 (Melt)
    df_melted = pd.melt(
        df,
        id_vars=[col_zh_name, col_en_name, col_pop_num],
        value_vars=blood_cols,
        var_name='血型組合',
        value_name='比例(%)'
    )
    
    # 計算該血型的「估算實際人數」
    df_melted['估算人數'] = (df_melted[col_pop_num] * (df_melted['比例(%)'] / 100)).astype(int)
    
    # 在記憶體內將欄位正名，方便外部程式碼一致呼叫
    df_melted = df_melted.rename(columns={
        col_zh_name: '國家中文名稱',
        col_en_name: '國家英文名稱',
        col_pop_num: '總人口'
    })
    
    # 根據血型組合結尾字元，歸類 Rh 因子
    df_melted['Rh因子'] = df_melted['血型組合'].apply(lambda x: 'Rh 陽性 (+)' if '+' in x else 'Rh 陰性 (-)')
    
    return df_melted, blood_cols

# 載入資料
df_global, blood_cols = load_and_process_data()

# ================= 側邊欄篩選器 (Sidebar) =================
st.sidebar.header("🌎 全球數據控制面板")
st.sidebar.markdown("請選擇要觀測的血型組合，右側將即時切換全球地理分佈與排行榜：")

# 1. 核心單選器：選擇血型
target_blood = st.sidebar.selectbox("選擇觀測血型：", options=blood_cols, index=0)

# 2. 輔助多選器：國家過濾（全面切換為中文選單）
all_countries_list = sorted(df_global["國家中文名稱"].unique().tolist())
countries_filter = st.sidebar.multiselect(
    "篩選特定國家（預設為全選全球）：",
    options=all_countries_list,
    default=all_countries_list
)

# 執行過濾
filtered_data = df_global[
    (df_global["血型組合"] == target_blood) & 
    (df_global["國家中文名稱"].isin(countries_filter))
]

# ================= 主畫面呈現 (Main Page) =================
st.title("🌎 全球各國血型與 Rh 因子大數據地圖分析")
st.markdown(f"目前正在針對全球 **{len(filtered_data['國家中文名稱'].unique())}** 個國家進行 **{target_blood}** 血型的分布數據透視。")

if filtered_data.empty:
    st.warning("⚠️ 目前篩選條件下無數據，請調整左側控制面板。")
else:
    # 3. 關鍵指標摘要 (KPI 卡片)
    kpi1, kpi2, kpi3 = st.columns(3)
    global_sub = filtered_data.drop_duplicates(subset=["國家中文名稱"])
    total_global_pop = global_sub["總人口"].sum()
    total_blood_pop = filtered_data["估算人數"].sum()
    avg_percentage = filtered_data["比例(%)"].mean()

    kpi1.metric("涵蓋國家總人口", f"{total_global_pop:,} 人")
    kpi2.metric(f"全球 {target_blood} 預估總人數", f"{total_blood_pop:,} 人")
    kpi3.metric(f"各國平均 {target_blood} 比例", f"{avg_percentage:.2f}%")

    st.markdown("---")

    # 4. 全球總體 Rh 因子比例圓餅圖區塊
    st.subheader("🧬 全球 Rh 因子總體比例特徵 (Rh+ vs Rh-)")
    col_pie_left, col_pie_right = st.columns([1, 2])
    
    with col_pie_left:
        # 動態連動：依據使用者選取的國家，加總全部血型群體的 Rh+ 與 Rh- 的預估總人數
        rh_summary = df_global[df_global["國家中文名稱"].isin(countries_filter)].groupby("Rh因子")["估算人數"].sum().reset_index()
        
        # 繪製高質感中空圓餅圖 (Donut Chart)
        fig_rh_pie = px.pie(
            rh_summary,
            values="估算人數",
            names="Rh因子",
            hole=0.4,
            color="Rh因子",
            color_discrete_map={'Rh 陽性 (+)': '#d62728', 'Rh 陰性 (-)': '#aec7e8'}, # 陽性熱情紅，陰性冷冽藍
            title="當前篩選範圍內 Rh 因子總量佔比"
        )
        fig_rh_pie.update_traces(textinfo='percent+label', pull=[0, 0.1] if len(rh_summary)>1 else None)
        fig_rh_pie.update_layout(margin=dict(l=20, r=20, b=20, t=40))
        st.plotly_chart(fig_rh_pie, use_container_width=True)
        
    with col_pie_right:
        st.markdown("<br>", unsafe_allow_html=True)
        st.info("""
        **💡 Rh 因子大數據科學洞察：**
        * **Rh 陽性 (Rh+)**：在全球人口中佔絕對優勢，尤其在亞洲與非洲，其比例通常高達 99% 以上。
        * **Rh 陰性 (Rh-)**：即醫學上常說的「稀有血型」或「熊貓血」。它在歐美白種人社群中分佈最高（約佔 15%），但在亞洲族群中通常僅有 0.3% ~ 1% 的極低概率。
        * *提示：左側圓餅圖會隨您在側邊欄增刪國家時**即時動態重新計算**，方便您對比不同地理區域的 Rh 因子結構特徵。*
        """)

    st.markdown("---")

    # 5. 全球互動視覺化地圖（完美中英雙軌匹配）
    st.subheader(f"🗺️ 全球 {target_blood} 血型人口比例地理分佈")
    st.markdown("*顏色越深代表比例越高。滑鼠移過去提示框會顯示【中文名稱】與該血型的估算人數。*")
    
    fig_map = px.choropleth(
        filtered_data,
        locations="國家英文名稱",     # 核心：地圖演算法底層用英文精準匹配世界疆界
        locationmode="country names", 
        color="比例(%)",
        hover_name="國家中文名稱",   # 核心：滑鼠浮動標籤改成顯示中文
        hover_data={"國家英文名稱": False, "總人口": ":,", "估算人數": ":,"}, 
        color_continuous_scale=px.colors.sequential.YlOrRd,
        title=f"全球各國 {target_blood} 血型比例分佈圖"
    )
    fig_map.update_layout(
        geo=dict(showframe=False, showcoastlines=True, projection_type='equirectangular'),
        margin=dict(l=0, r=0, b=0, t=40)
    )
    st.plotly_chart(fig_map, use_container_width=True)

    st.markdown("---")

    # 6. 排行榜 (Top Rankings) 全面改用中文名稱顯示
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader(f"🏆 {target_blood} 比例最高前 15 名國家")
        top_pct = filtered_data.sort_values(by="比例(%)", ascending=False).head(15)
        
        fig_top_pct = px.bar(
            top_pct,
            x="比例(%)",
            y="國家中文名稱",
            orientation='h',
            color="比例(%)",
            color_continuous_scale=px.colors.sequential.YlOrRd,
            text="比例(%)"
        )
        fig_top_pct.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
        fig_top_pct.update_layout(yaxis=dict(autorange="reversed", title="國家"))
        st.plotly_chart(fig_top_pct, use_container_width=True)

    with col_right:
        st.subheader(f"📊 {target_blood} 估算人數最多前 15 名國家")
        top_num = filtered_data.sort_values(by="估算人數", ascending=False).head(15)
        
        fig_top_num = px.bar(
            top_num,
            x="估算人數",
            y="國家中文名稱",
            orientation='h',
            color="估算人數",
            color_continuous_scale=px.colors.sequential.Burg
        )
        fig_top_num.update_traces(texttemplate='%{text:,}', textposition='outside')
        fig_top_num.update_layout(yaxis=dict(autorange="reversed", title="國家"), xaxis_title="預估人數")
        st.plotly_chart(fig_top_num, use_container_width=True)

    # 7. 底部詳細數據明細矩陣
    st.markdown("---")
    st.subheader("📋 全球國家數據矩陣明細")
    
    raw_display = df_global[df_global["國家中文名稱"].isin(countries_filter)]
    pivot_display = raw_display.pivot(
        index="國家中文名稱", 
        columns="血型組合", 
        values="比例(%)"
    ).fillna(0)

    # 補回總人口對照
    pop_lookup = df_global.drop_duplicates(subset=["國家中文名稱"]).set_index("國家中文名稱")["總人口"]
    pivot_display.insert(0, "總人口", pop_lookup)

    st.dataframe(pivot_display.style.format({
        "總人口": "{:,}",
        "O+": "{:.2f}%", "A+": "{:.2f}%", "B+": "{:.2f}%", "AB+": "{:.2f}%",
        "O-": "{:.2f}%", "A-": "{:.2f}%", "B-": "{:.2f}%", "AB-": "{:.2f}%"
    }), use_container_width=True)