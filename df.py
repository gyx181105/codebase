import streamlit as st
import pandas as pd
import numpy as np



# 第一部分：数据汇总部分
st.title('F-业务数据汇总')

col1, col2, col3 = st.columns(3)
col1.metric("总量", "888888 个", "1.2 °F")
col2.metric("增长量", "6666 个", "-8%")
col3.metric("增长率", "16%", "4%")


# 第二部分：图标展示
#2.1  幸运值柱状图
st.title('幸运值柱状图')
chart_data = pd.DataFrame(
    np.random.randn(10, 3),
    columns = ["f001", "f002", "f003"])
st.bar_chart(chart_data)



#2.2  各个节点算力图
st.title('各个节点算力图')
chart_data = pd.DataFrame(
    np.random.randn(10, 3),
    columns = ["f001", "f002", "f003"])
st.bar_chart(chart_data)



#2.3  各个节点的总额柱状图
st.title('各个节点的总额柱状图')
chart_data = pd.DataFrame(
    np.random.randn(10, 3),
    columns = ["f001", "f002", "f003"])
st.bar_chart(chart_data)


#第三部分数据详单
st.title('日统计数据详单')
df = pd.DataFrame(
    np.random.randn(10, 10),
    columns=('第%d列' % (i+1) for i in range(10))
)

st.table(df)

df = pd.DataFrame(
    np.random.randn(10, 5),
    columns=('第%d列' % (i+1) for i in range(5))
)

st.dataframe(df.style.highlight_max(axis=0))

