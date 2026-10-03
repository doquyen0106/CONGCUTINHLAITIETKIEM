import streamlit as st
st.image("logo.jpg")
# =========================
# CẤU HÌNH TRANG
# =========================
st.set_page_config(
    page_title="Tính lãi gửi tiết kiệm",
    page_icon="💰",
    layout="centered"
)

# =========================
# TIÊU ĐỀ
# =========================
st.title("💰 APP TÍNH LÃI GỬI TIẾT KIỆM của Lê Thị Đỗ Quyên")
st.write("Nhập thông tin khoản tiền gửi để tính tiền lãi.")

st.divider()

# =========================
# HÀM ĐỊNH DẠNG TIỀN
# =========================
def format_money(value):
    return f"{value:,.0f} VNĐ".replace(",", ".")


# =========================
# NHẬP THÔNG TIN
# =========================
st.subheader("📋 Thông tin tiền gửi")

col1, col2 = st.columns(2)

with col1:
    tien_gui = st.number_input(
        "💵 Số tiền gửi (VNĐ)",
        min_value=0.0,
        value=100_000_000.0,
        step=1_000_000.0,
        format="%.0f"
    )

    ky_han = st.number_input(
        "📅 Kỳ hạn (tháng)",
        min_value=1,
        max_value=120,
        value=12,
        step=1
    )

with col2:
    lai_suat = st.number_input(
        "📈 Lãi suất (%/năm)",
        min_value=0.0,
        max_value=100.0,
        value=5.0,
        step=0.1,
        format="%.2f"
    )

    hinh_thuc_nhan_lai = st.selectbox(
        "💳 Hình thức nhận lãi",
        [
            "Cuối kỳ",
            "Hàng tháng",
            "Hàng quý"
        ]
    )

loai_lai = st.radio(
    "🔄 Phương thức tính lãi",
    [
        "Lãi đơn",
        "Lãi kép"
    ],
    horizontal=True
)

st.divider()

# =========================
# NÚT TÍNH
# =========================
if st.button("🧮 TÍNH TIỀN LÃI", use_container_width=True):

    if tien_gui <= 0:
        st.error("Vui lòng nhập số tiền gửi lớn hơn 0.")
        st.stop()

    if lai_suat < 0:
        st.error("Lãi suất không được nhỏ hơn 0.")
        st.stop()

    # ---------------------------------
    # CHUYỂN ĐỔI THỜI GIAN
    # ---------------------------------
    thoi_gian_nam = ky_han / 12

    lai_suat_nam = lai_suat / 100

    # ---------------------------------
    # XÁC ĐỊNH SỐ KỲ NHẬN LÃI
    # ---------------------------------
    if hinh_thuc_nhan_lai == "Hàng tháng":
        so_ky = ky_han
        lai_suat_ky = lai_suat_nam / 12

    elif hinh_thuc_nhan_lai == "Hàng quý":
        so_ky = ky_han / 3
        lai_suat_ky = lai_suat_nam / 4

    else:
        # Cuối kỳ
        so_ky = 1
        lai_suat_ky = lai_suat_nam * thoi_gian_nam

    # =========================
    # TÍNH LÃI ĐƠN
    # =========================
    if loai_lai == "Lãi đơn":

        tong_lai = tien_gui * lai_suat_nam * thoi_gian_nam

        tong_tien = tien_gui + tong_lai

        # Tiền lãi theo kỳ nhận
        if hinh_thuc_nhan_lai == "Cuối kỳ":
            lai_dinh_ky = tong_lai

        elif hinh_thuc_nhan_lai == "Hàng tháng":
            lai_dinh_ky = tong_lai / ky_han

        else:
            lai_dinh_ky = tong_lai / (ky_han / 3)

    # =========================
    # TÍNH LÃI KÉP
    # =========================
    else:

        if hinh_thuc_nhan_lai == "Cuối kỳ":

            # Lãi kép cuối kỳ:
            # Toàn bộ lãi được cộng vào gốc vào cuối kỳ
            tong_tien = tien_gui * (
                1 + lai_suat_nam
            ) ** thoi_gian_nam

            tong_lai = tong_tien - tien_gui

            lai_dinh_ky = tong_lai

        elif hinh_thuc_nhan_lai == "Hàng tháng":

            # Lãi kép theo tháng
            lai_suat_thang = lai_suat_nam / 12

            tong_tien = tien_gui * (
                1 + lai_suat_thang
            ) ** ky_han

            tong_lai = tong_tien - tien_gui

            # Lãi của kỳ đầu tiên
            lai_dinh_ky = tien_gui * lai_suat_thang

        else:

            # Lãi kép theo quý
            lai_suat_quy = lai_suat_nam / 4

            so_quy = ky_han / 3

            tong_tien = tien_gui * (
                1 + lai_suat_quy
            ) ** so_quy

            tong_lai = tong_tien - tien_gui

            # Lãi của quý đầu tiên
            lai_dinh_ky = tien_gui * lai_suat_quy

    # =========================
    # HIỂN THỊ KẾT QUẢ
    # =========================
    st.success("✅ Tính toán thành công!")

    st.subheader("📊 Kết quả")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "💵 Tiền gốc",
            format_money(tien_gui)
        )

    with col2:
        st.metric(
            "📈 Tổng tiền lãi",
            format_money(tong_lai)
        )

    with col3:
        st.metric(
            "💰 Gốc + Lãi",
            format_money(tong_tien)
        )

    st.divider()

    st.write("### 💳 Tiền lãi định kỳ")

    if hinh_thuc_nhan_lai == "Cuối kỳ":
        st.info(
            f"Bạn nhận được **{format_money(lai_dinh_ky)}** "
            f"tiền lãi vào cuối kỳ."
        )

    elif hinh_thuc_nhan_lai == "Hàng tháng":
        st.info(
            f"Tiền lãi bình quân mỗi tháng: "
            f"**{format_money(lai_dinh_ky)}**"
        )

    else:
        st.info(
            f"Tiền lãi bình quân mỗi quý: "
            f"**{format_money(lai_dinh_ky)}**"
        )

    # =========================
    # CHI TIẾT KHOẢN GỬI
    # =========================
    st.divider()

    st.subheader("📝 Chi tiết khoản gửi")

    st.write(f"**Số tiền gửi:** {format_money(tien_gui)}")
    st.write(f"**Kỳ hạn:** {ky_han} tháng")
    st.write(f"**Lãi suất:** {lai_suat:.2f}%/năm")
    st.write(f"**Hình thức nhận lãi:** {hinh_thuc_nhan_lai}")
    st.write(f"**Phương thức:** {loai_lai}")
    st.write(f"**Tổng tiền lãi:** {format_money(tong_lai)}")
    st.write(f"**Tổng tiền nhận:** {format_money(tong_tien)}")
