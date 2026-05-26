import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date

# دعم اللغة العربية
from arabic_reshaper import reshape
from bidi.algorithm import get_display

# =========================
# إعداد الصفحة
# =========================
st.set_page_config(
    page_title="محفظة الذكاء",
    page_icon="💰",
    layout="wide"
)

# =========================
# دالة تعديل النص العربي
# =========================
def arabic_text(text):
    reshaped = reshape(text)
    return get_display(reshaped)

# =========================
# عنوان التطبيق
# =========================
st.title("💰 محفظة الذكاء")
st.subheader("تطبيق إدارة المصروفات الشخصية")

# =========================
# تخزين البيانات
# =========================
if "expenses" not in st.session_state:
    st.session_state.expenses = pd.DataFrame(
        columns=["المبلغ", "الفئة", "التاريخ"]
    )

# =========================
# إدخال الميزانية
# =========================
st.sidebar.header("📌 إعداد الميزانية")

budget = st.sidebar.number_input(
    "أدخل الميزانية الشهرية",
    min_value=0.0,
    step=100.0
)

# =========================
# إدخال المصروفات
# =========================
st.header("➕ إضافة مصروف جديد")

col1, col2, col3 = st.columns(3)

with col1:
    amount = st.number_input(
        "المبلغ",
        min_value=0.0,
        step=10.0
    )

with col2:
    category = st.selectbox(
        "الفئة",
        [
            "طعام",
            "سكن",
            "مواصلات",
            "ترفيه",
            "تعليم",
            "فواتير",
            "أخرى"
        ]
    )

with col3:
    expense_date = st.date_input(
        "التاريخ",
        value=date.today()
    )

# =========================
# زر إضافة المصروف
# =========================
if st.button("إضافة المصروف"):
    
    if amount > 0:

        new_expense = pd.DataFrame({
            "المبلغ": [amount],
            "الفئة": [category],
            "التاريخ": [expense_date]
        })

        st.session_state.expenses = pd.concat(
            [st.session_state.expenses, new_expense],
            ignore_index=True
        )

        st.success("✅ تم إضافة المصروف بنجاح")

    else:
        st.warning("⚠️ أدخل مبلغ صحيح")

# =========================
# عرض جدول المصروفات
# =========================
st.header("📋 جدول المصروفات")

if not st.session_state.expenses.empty:

    st.dataframe(
        st.session_state.expenses,
        use_container_width=True
    )

    # =========================
    # الحسابات
    # =========================
    total_expenses = st.session_state.expenses["المبلغ"].sum()

    remaining = budget - total_expenses

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "💵 الميزانية",
            f"{budget:.2f}"
        )

    with col2:
        st.metric(
            "💸 إجمالي المصروفات",
            f"{total_expenses:.2f}"
        )

    with col3:
        st.metric(
            "💰 المتبقي",
            f"{remaining:.2f}"
        )

    # =========================
    # الرسم البياني
    # =========================
    st.header("📊 تحليل المصروفات حسب الفئة")

    category_summary = (
        st.session_state.expenses
        .groupby("الفئة")["المبلغ"]
        .sum()
    )

    # تعديل أسماء الفئات للعربية
    labels = [
        arabic_text(label)
        for label in category_summary.index
    ]

    chart_type = st.radio(
        "اختر نوع الرسم البياني",
        ["دائري", "شريطي"],
        horizontal=True
    )

    fig, ax = plt.subplots(figsize=(8, 5))

    if chart_type == "دائري":

        ax.pie(
            category_summary,
            labels=labels,
            autopct='%1.1f%%'
        )

        ax.set_title(
            arabic_text("نسبة المصروفات حسب الفئة")
        )

    else:

        ax.bar(
            labels,
            category_summary.values
        )

        ax.set_title(
            arabic_text("إجمالي المصروفات حسب الفئة")
        )

        ax.set_ylabel(
            arabic_text("المبلغ")
        )

    st.pyplot(fig)

else:
    st.info("لا توجد مصروفات مضافة بعد")

# =========================
# رسالة ختامية
# =========================
st.markdown("---")

st.caption(
    "تم تطوير تطبيق محفظة الذكاء باستخدام Python و Streamlit"
)
