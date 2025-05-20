# 🏥 Healthcare Microservices System

Hệ thống quản lý bệnh viện được xây dựng theo kiến trúc **microservices**, mỗi service đảm nhiệm một chức năng riêng biệt.

---

## 📦 Microservices Đã Xây Dựng

### 1. 🔐 Auth Service

- Chức năng xác thực và phân quyền người dùng.
- Endpoint chính:
  - `GET /user-info/`: Trả về thông tin người dùng dựa trên JWT Token.
- Dùng bởi các services khác để xác định thông tin user từ token.

---

### 2. 🧑‍⚕️ Patient Service

- **Chức năng**:
  - update sau

---

### 3. 📅 Appointment Service

- **Chức năng**:

  - `GET /appointments/`: Danh sách lịch hẹn.
  - `POST /appointments/`: Tạo lịch hẹn mới (cần `patient_id`, `doctor_id`, `appointment_time`).
  - Lấy danh sách hẹn theo id doctor, patient

- **Trường trạng thái**:
  - `pending`, `confirmed`, `cancelled`, `completed`.

### 4. 🧾 Medical Service

- **Chức năng**:

  - `POST /medical-records/`: Tạo hồ sơ bệnh án cho bệnh nhân (do bác sĩ tạo).

  - `POST /prescriptions/`: Tạo đơn thuốc gắn với một hồ sơ bệnh án.

  - lấy danh sách hồ sơ bệnh án, đơn thuốc theo id bệnh nhân, id bác sĩ.

### 5. 🧑‍⚕️ Doctor Service

- **Chức năng**:
  - update sau

### 6. Note

- Tải thư viện bản mới nhất
- xóa hết migration và tạo lại db
