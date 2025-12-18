import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from scipy.optimize import curve_fit

# -------------------------- 核心功能函数 --------------------------
def load_data(file_path):
    """加载Excel/CSV数据"""
    try:
        if file_path.endswith('.xlsx'):
            return pd.read_excel(file_path)
        elif file_path.endswith('.csv'):
            return pd.read_csv(file_path)
        else:
            print("❌ 仅支持.xlsx或.csv格式")
            return None
    except Exception as e:
        print(f"❌ 加载失败：{str(e)}")
        return None

def clean_data(df):
    """自动删除所有Unnamed列(通用数据清洗)"""
    cleaned_df = df.drop(columns=[col for col in df.columns if 'Unnamed' in col], errors='ignore')
    print(f"✅ 已删除{len(df.columns)-len(cleaned_df.columns)}个无用列")
    return cleaned_df

def add_custom_column(df):
    """根据用户输入新增列"""
    col_name = input("请输入新列名：")
    formula = input(f"请输入{col_name}的计算规则（如x+y、x*2等，用列名表示）：")
    try:
        df[col_name] = df.eval(formula)
        print(f"✅ 已新增列：{col_name}")
        return df
    except Exception as e:
        print(f"❌ 公式错误：{str(e)}")
        return df

def filter_data_by_condition(df):
    """根据用户输入条件筛选数据"""
    condition = input("请输入筛选条件（如x>3 and y<5）：")
    try:
        filtered_df = df.query(condition)
        print(f"✅ 筛选出{len(filtered_df)}行数据")
        return filtered_df
    except Exception as e:
        print(f"❌ 条件错误：{str(e)}")
        return df

def calculate_statistics(df):
    """计算基本统计量（均值、方差、相关系数）"""
    stats_dict = {}
    for col in df.select_dtypes(include=[np.number]).columns:
        stats_dict[col] = {
            '均值': np.mean(df[col]),
            '方差': np.var(df[col])
        }
    # 计算相关系数矩阵
    corr_matrix = df.select_dtypes(include=[np.number]).corr()
    return stats_dict, corr_matrix

def hypothesis_test(df):
    """执行假设检验（t检验/卡方检验）"""
    test_type = input("请选择检验类型（1.t检验 2.卡方检验）：")
    if test_type == '1':
        col1 = input("输入第一列名：")
        col2 = input("输入第二列名：")
        t_stat, p_value = stats.ttest_ind(df[col1], df[col2])
        print(f"t统计量：{t_stat:.4f}，p值：{p_value:.4f}")
        print("结论：" + ("拒绝原假设" if p_value < 0.05 else "接受原假设"))
    elif test_type == '2':
        col1 = input("输入分类列1：")
        col2 = input("输入分类列2：")
        contingency_table = pd.crosstab(df[col1], df[col2])
        chi2, p_value, _, _ = stats.chi2_contingency(contingency_table)
        print(f"卡方统计量：{chi2:.4f}，p值：{p_value:.4f}")
        print("结论：" + ("拒绝原假设（存在关联）" if p_value < 0.05 else "接受原假设（无关联）"))

def visualize_data(df):
    """多类型可视化模块"""
    plot_type = input("请选择图表类型（1.散点图 2.直方图 3.拟合曲线）：")
    if plot_type == '1':
        x_col = input("输入X轴列名：")
        y_col = input("输入Y轴列名：")
        plt.scatter(df[x_col], df[y_col], alpha=0.6)
        plt.title(f"{x_col} vs {y_col} 散点图")
        plt.xlabel(x_col)
        plt.ylabel(y_col)
        plt.show()
    elif plot_type == '2':
        col = input("输入列名：")
        plt.hist(df[col], bins=10, alpha=0.7)
        plt.title(f"{col} 直方图")
        plt.xlabel(col)
        plt.ylabel("频数")
        plt.show()
    elif plot_type == '3':
        x_col = input("输入X轴列名：")
        y_col = input("输入Y轴列名：")
        model_type = input("请选择拟合模型（1.线性 2.二次 3.指数 4.幂函数）：")
        
        # 定义拟合函数
        def linear(x, a, b): return a*x + b
        def quadratic(x, a, b, c): return a*x**2 + b*x + c
        def exponential(x, a, b): return a * np.exp(b*x)
        def power(x, a, b): return a * x**b
        
        x_data = df[x_col].values
        y_data = df[y_col].values
        popt, _ = curve_fit(linear if model_type=='1' else quadratic if model_type=='2' else exponential if model_type=='3' else power, x_data, y_data)
        
        # 绘制拟合曲线
        x_fit = np.linspace(min(x_data), max(x_data), 100)
        y_fit = linear(x_fit, *popt) if model_type=='1' else quadratic(x_fit, *popt) if model_type=='2' else exponential(x_fit, *popt) if model_type=='3' else power(x_fit, *popt)
        
        plt.scatter(x_data, y_data, label='原始数据')
        plt.plot(x_fit, y_fit, 'r-', label=f'拟合曲线（R²={stats.pearsonr(y_data, linear(x_data, *popt) if model_type=="1" else quadratic(x_data, *popt) if model_type=="2" else exponential(x_data, *popt) if model_type=="3" else power(x_data, *popt))[0]**2:.4f}）')
        plt.legend()
        plt.title(f"{y_col} vs {x_col} 拟合曲线")
        plt.show()

# -------------------------- 主交互流程 --------------------------
def main():
    print("📊 交互式数据分析计算器")
    file_path = input("请输入文件路径(data.xlsx):")
    df = load_data(file_path)
    if df is None:
        return
    
    while True:
        print("\n" + "="*30)
        print("功能菜单：")
        print("1. 自动清洗数据(删除Unnamed列)")
        print("2. 新增自定义列")
        print("3. 条件筛选数据")
        print("4. 计算统计量（均值/方差/相关系数）")
        print("5. 假设检验(t检验/卡方检验）")
        print("6. 数据可视化")
        print("7. 显示当前数据")
        print("0. 退出程序")
        choice = input("请输入功能编号：")
        
        if choice == '1':
            df = clean_data(df)
            print(df)
        elif choice == '2':
            df = add_custom_column(df)
            print(df)
        elif choice == '3':
            filtered_df = filter_data_by_condition(df)
            print(filtered_df.head())
        elif choice == '4':
            stats_dict, corr_matrix = calculate_statistics(df)
            print("\n📈 统计结果：")
            for col, stats in stats_dict.items():
                print(f"- {col}：均值{stats['均值']:.4f}，方差{stats['方差']:.4f}")
            print("\n🔗 相关系数矩阵：")
            print(corr_matrix.round(4))
        elif choice == '5':
            hypothesis_test(df)
        elif choice == '6':
            visualize_data(df)
        elif choice == '7':
            print("\n当前数据预览:")
            print(df.head())
        elif choice == '0':
            print("👋 程序结束")
            break
        else:
            print("❌ 无效输入，请重新选择")

if __name__ == "__main__":
    main()
