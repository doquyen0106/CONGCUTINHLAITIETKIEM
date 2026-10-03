import streamlit as st

# =========================
# CẤU HÌNH TRANG
# =========================
st.set_page_config(
    page_title="Tính lãi gửi tiết kiệm",
    page_icon="💰",
    layout="centered"
)

# =========================
# HÀM ĐỊNH DẠNG TIỀN
# =========================
def format_money(amount):
    return f"{amount:,.0f} VNĐ".replace(",", ".")


# =========================
# TIÊU ĐỀ
# =========================
st.title("💰 TÍNH LÃI GỬI TIẾT KIỆM")
st.write(
    "Nhập thông tin khoản tiền gửi để tính tiền lãi định kỳ, "
    "tổng tiền lãi và tổng số tiền nhận được."
)

st.divider()


# =========================
# NHẬP THÔNG TIN
# =========================
st.subheader("📋 Thông tin tiền gửi")

col1, col2 = st.columns(2)

with col1:
    so_tien_gui = st.number_input(
        "Số tiền gửi (VNĐ)",
        min_value=0.0,
        value=100_000_000.0,
        step=1_000_000.0,
        format="%.0f"
    )

with col2:
    ky_han = st.number_input(
        "Kỳ hạn (tháng)",
        min_value=1,
        max_value=120,
        value=12,
        step=1
    )

col3, col4 = st.columns(2)

with col3:
    lai_suat = st.number_input(
        "Lãi suất (%/năm)",
        min_value=0.0,
        max_value=100.0,
        value=5.0,
        step=0.1,
        format="%.2f"
    )

with col4:
    hinh_thuc_nhan_lai = st.selectbox(
        "Hình thức nhận lãi",
        [
            "Cuối kỳ",
            "Hàng tháng",
            "Hàng quý"
        ]
    )

loai_lai = st.radio(
    "Loại lãi suất",
    [
        "Lãi đơn",
        "Lãi kép"
    ],
    horizontal=True
)

st.divider()


# =========================
# TÍNH TOÁN
# =========================
if st.button("🧮 TÍNH TIỀN LÃI", use_container_width=True):

    if so_tien_gui <= 0:
        st.error("Vui lòng nhập số tiền gửi lớn hơn 0.")
        st.stop()

    if lai_suat < 0:
        st.error("Lãi suất không được nhỏ hơn 0.")
        st.stop()

    # Chuyển lãi suất % sang số thập phân
    lai_suat_nam = lai_suat / 100

    # Thời gian tính theo năm
    so_nam = ky_han / 12

    # ==========================================
    # XÁC ĐỊNH SỐ KỲ NHẬN LÃI
    # ==========================================
    if hinh_thuc_nhan_lai == "Hàng tháng":
        so_ky = ky_han
        lai_suat_ky = lai_suat_nam / 12
        ten_ky = "tháng"

    elif hinh_thuc_nhan_lai == "Hàng quý":
        # Kỳ hạn phải được quy đổi theo quý
        so_ky = ky_han / 3
        lai_suat_ky = lai_suat_nam / 4
        ten_ky = "quý"

    else:
        # Cuối kỳ: chỉ có một lần nhận lãi
        so_ky = 1
        lai_suat_ky = lai_suat_nam * so_nam
        ten_ky = "cuối kỳ"

    # ==========================================
    # LÃI ĐƠN
    # ==========================================
    if loai_lai == "Lãi đơn":

        # Tổng tiền lãi
        tong_lai = so_tien_gui * lai_suat_nam * so_nam

        # Tiền lãi mỗi kỳ
        if hinh_thuc_nhan_lai == "Cuối kỳ":
            lai_dinh_ky = tong_lai
        else:
            lai_dinh_ky = tong_lai / so_ky

        tong_tien = so_tien_gui + tong_lai

    # ==========================================
    # LÃI KÉP
    # ==========================================
    else:

        # Nếu nhận lãi hàng tháng/quý,
        # lãi được nhập vào gốc và tiếp tục sinh lãi.
        if hinh_thuc_nhan_lai == "Hàng tháng":

            so_ky_lai = ky_han
            lai_suat_ky = lai_suat_nam / 12

            tong_tien = (
                so_tien_gui
                * (1 + lai_suat_ky) ** so_ky_lai
            )

            tong_lai = tong_tien - so_tien_gui

            # Lãi của kỳ đầu tiên
            lai_dinh_ky = so_tien_gui * lai_suat_ky

        elif hinh_thuc_nhan_lai == "Hàng quý":

            so_ky_lai = ky_han / 3
            lai_suat_ky = lai_suat_nam / 4

            # Nếu kỳ hạn không chia hết cho 3,
            # phần tháng lẻ được tính theo thời gian thực tế.
            so_quy_day_du = int(ky_han // 3)
            thang_le = ky_han % 3

            tong_tien = (
                so_tien_gui
                * (1 + lai_suat_ky) ** so_quy_day_du
            )

            # Tính phần tháng lẻ theo lãi suất tháng
            if thang_le > 0:
                lai_suat_thang = lai_suat_nam / 12
                tong_tien *= (1 + lai_suat_thang) ** thang_le

            tong_lai = tong_tien - so_tien_gui

            # Lãi quý đầu tiên
            lai_dinh_ky = so_tien_gui * lai_suat_ky

        else:
            # Cuối kỳ: lãi kép theo tháng
            # để phản ánh việc lãi được nhập gốc trong kỳ.
            so_ky_lai = ky_han
            lai_suat_thang = lai_suat_nam / 12

            tong_tien = (
                so_tien_gui
                * (1 + lai_suat_thang) ** so_ky_lai
            )

            tong_lai = tong_tien - so_tien_gui

            lai_dinh_ky = tong_lai

    # =========================
    # HIỂN THỊ KẾT QUẢ
    # =========================
    st.success("✅ Đã tính toán thành công!")

    st.subheader("📊 Kết quả")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "💵 Tiền lãi định kỳ",
            format_money(lai_dinh_ky)
        )

    with col2:
        st.metric(
            "📈 Tổng tiền lãi",
            format_money(tong_lai)
        )

    st.metric(
        "💰 Tổng gốc + lãi",
        format_money(tong_tien)
    )

    st.divider()

    # =========================
    # THÔNG TIN CHI TIẾT
    # =========================
    st.subheader("📝 Chi tiết khoản tiền gửi")

    st.write(f"**Số tiền gửi:** {format_money(so_tien_gui)}")
    st.write(f"**Kỳ hạn:** {ky_han} tháng")
    st.write(f"**Lãi suất:** {lai_suat:.2f}%/năm")
    st.write(f"**Hình thức nhận lãi:** {hinh_thuc_nhan_lai}")
    st.write(f"**Loại lãi:** {loai_lai}")

    # =========================
    # CẢNH BÁO / GIẢ ĐỊNH
    # =========================
    if loai_lai == "Lãi kép":
        st.info(
            "💡 Với lãi kép, tiền lãi được nhập vào vốn để tiếp tục "
            "sinh lãi ở các kỳ tiếp theo."
        )

    if hinh_thuc_nhan_lai == "Cuối kỳ":
        st.info(
            "💡 Hình thức cuối kỳ nghĩa là toàn bộ tiền lãi "
            "được tính và nhận vào cuối kỳ hạn."
        )
