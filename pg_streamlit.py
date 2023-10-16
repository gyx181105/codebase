import streamlit as st
import psycopg2
import pandas as pd
import matplotlib.pyplot as plt

# PostgreSQL 连接信息
def connect_to_postgresql():
    # 如果用docker，需要实际的容器 IP 地址替换这里
    DB_HOST = "localhost"
    # 数据库端口号，通常是默认的 5432
    DB_PORT = "5432"
    # 数据库名称
    DB_NAME = "filecoin"
    # 数据库用户名
    DB_USER = "postgres"
    # 数据库密码
    DB_PASS = "901205"
    
    try:
        # 连接到 PostgreSQL 数据库
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASS
        )
        return conn
    except Exception as e:
        print(f"An error occurred while connecting to PostgreSQL: {str(e)}")
        return None

# 查询函数，这部分用于构建之后所有计算的基础dataframe
def query_data_from_postgresql(conn, table_name):
    try:
        # 构建 SQL 查询语句
        query_base = f"SELECT * FROM {table_name};"
        
        # 查询数据
        df = []
        df = pd.read_sql_query(query_base, conn)
        
        if table_name == "base_statistics":
            df = df.rename(columns={
                "time": "时间",
                "node_id": "节点号",
                "power": "算力PiB",
                "total_balance": "总余额Fil",
                "ini_pledge": "质押Fil",
                "lock_balance": "锁仓Fil",
                "ava_balance": "可提现Fil",
                "owner_balance": "owner余额Fil",
                "luck": "幸运值%"
            })
        elif table_name == "daily_statistics":
            df = df.rename(columns={
                "time": "时间",
                "node_id": "节点号",
                "power": "算力PiB",
                "total_balance": "总余额Fil",
                "day_total_change": "日余额增减",
                "day_total_rate": "日余额增减%",
                "ini_pledge": "质押Fil",
                "day_ini_change": "质押增减",
                "day_ini_rate": "质押增减%",
                "lock_balance": "锁仓Fil",
                "day_lock_change": "锁仓增减",
                "day_lock_rate": "锁仓余额%",
                "ava_balance": "可提现Fil",
                "day_ava_change": "可提现增减",
                "day_ava_rate": "可提现增减%",
                "owner_balance": "owner余额Fil",
                "day_owner_change": "owner余额增减",
                "day_owner_rate": "owner余额增减%",
                "day_luck": "日幸运值%",
                "day_luck_change": "日幸运值%增减",
                "day_luck_rate": "日幸运值%增减%"
            })
        return df
    except Exception as e:
        print(f"An error occurred while querying data: {str(e)}")
        return None

# 可视化数据
def visualize_data(df, column_name):
    if column_name in df.columns:
        st.subheader(f"{column_name}-数据展示")
        
        # 创建数据汇总统计表和柱状图
        if pd.api.types.is_numeric_dtype(df[column_name]):
            st.write(f"{column_name}-数据汇总:")
            st.write(df[column_name].describe())
            
            # 柱状图
            st.subheader(f"{column_name}-柱状图:")
            fig, ax = plt.subplots()
            df.set_index('时间')[column_name].plot(kind='bar', ax=ax)
            plt.xlabel('时间')
            plt.ylabel(column_name)
            st.pyplot(fig)
        else:
            st.write(f"{column_name} is not a numeric column and cannot be visualized.")

def main():
    st.title('F业务-PG数据库')

    # Connect to your database (replace with your actual connection method)
    conn = connect_to_postgresql()

    if conn is not None:
        # Show the entire table
        table_name = st.selectbox("请选择表单:", ["base_statistics", "daily_statistics"])
        df = query_data_from_postgresql(conn, table_name)

        if 'id' in df.columns:
            df = df.drop(['id'], axis=1)
        if 'index' in df.columns:
            df = df.drop(['index'], axis=1)

        node_ids = df['节点号'].unique()
        selected_node_id = st.selectbox("请选择节点号:", node_ids)

        st.dataframe(df[df['节点号'] == selected_node_id])

        # Choose a column for visualization
        st.subheader('对应表单的指定数据展示')
        selected_column = st.selectbox("选择指定数据:", df.columns)
        if st.button("数据统计及可视化"):
            visualize_data(df[df['节点号'] == selected_node_id], selected_column)

        # Close the database connection
        conn.close()

if __name__ == '__main__':
    main()
