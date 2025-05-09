# 💼 Hệ Thống Quản Lý Nhân Viên (Employee Management System)

Đây là một chương trình quản lý nhân viên viết bằng ngôn ngữ **Python**, hỗ trợ các chức năng thêm, sửa, xóa, tìm kiếm và thống kê lương của nhân viên theo các loại: **Toàn thời gian**, **Bán thời gian** và **Quản lý**.

---

## 🧩 Các chức năng chính

- 👤 Thêm/sửa/xóa nhân viên
- 🔍 Tìm kiếm nhân viên theo mã, tên hoặc số điện thoại
- 🧾 Thống kê lương tổng và theo loại nhân viên
- 👥 Quản lý đội nhóm cho nhân viên quản lý
- 💾 Lưu và đọc dữ liệu từ file `employees_data.txt`
- 🧪 Khởi tạo dữ liệu mẫu để dùng thử nhanh

---

## 🛠️ Cài đặt & chạy chương trình

### 1. Clone dự án
```bash
git clone https://github.com/ban-ten-repo/employee-management.git
cd employee-management
```

### 2. Chạy chương trình (Python 3)
```bash
python updated_employee_management_system.py
```

---

## 🖥️ Yêu cầu hệ thống

- Python 3.7 trở lên
- Không sử dụng thư viện ngoài (chỉ cần `os`, `re`, `sys`)

---

## 📁 Cấu trúc dự án

```
employee-management/
├── employees_data.txt            # File lưu dữ liệu nhân viên
├── updated_employee_management_system.py  # File chính
└── README.md                     # File hướng dẫn
```

---

## 🧪 Khởi tạo dữ liệu mẫu

Chạy chương trình, chọn:
```
8. Khởi tạo dữ liệu mẫu
```
=> Tự động thêm 6 nhân viên (2 full-time, 2 part-time, 2 quản lý) kèm phân nhóm.

---

## 📸 Giao diện dòng lệnh

```
===== HỆ THỐNG QUẢN LÝ NHÂN VIÊN =====
1. Xem danh sách nhân viên
2. Thêm nhân viên mới
3. Cập nhật thông tin nhân viên
4. Xóa nhân viên
5. Tìm kiếm nhân viên
6. Quản lý đội nhóm
7. Thống kê lương
8. Khởi tạo dữ liệu mẫu
0. Thoát chương trình
```

---

## 👨‍💻 Tác giả

- **Tên**: Nguyễn Minh Hách 
- **Email**: hachminh456@gmail.com

---

## 📄 Giấy phép

Phân phối theo giấy phép MIT.

---

## 📌 Ghi chú

> Chương trình sử dụng file `.txt` để lưu dữ liệu – không cần cơ sở dữ liệu phức tạp. Phù hợp cho bài tập lớn hoặc các ứng dụng quản lý đơn giản.
