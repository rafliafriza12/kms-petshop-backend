# KMS Petshop Backend API Documentation

## Overview
KMS Petshop Backend adalah RESTful API untuk aplikasi petshop yang dibangun menggunakan Flask dan MongoDB. API ini menyediakan layanan untuk manajemen pengguna, kucing, layanan grooming, keranjang belanja, pesanan, dan pembayaran.

**Base URL:** `https://your-domain.com/`  
**Version:** 1.0.0  
**Database:** MongoDB  

## Authentication
API menggunakan JWT (JSON Web Token) untuk autentikasi. Token harus disertakan dalam header request:
```
Authorization: Bearer <your-jwt-token>
```

## Response Format
Semua response menggunakan format JSON dengan struktur standar:
```json
{
  "status": 200,
  "data": {},
  "message": "Success message",
  "total": 10
}
```

## User Roles
- **USER**: Customer biasa yang dapat menggunakan layanan
- **ADMIN**: Administrator dengan akses penuh ke sistem

---

## Endpoints

### 1. Root Endpoints

#### GET /
Mendapatkan informasi dasar API
- **Method:** GET
- **Authentication:** Tidak diperlukan
- **Response:**
```json
{
  "message": "KMS Petshop Backend API",
  "version": "1.0.0",
  "status": "running",
  "endpoints": {
    "auth": "/api/auth",
    "users": "/api/user",
    "layanan": "/api/layanan",
    "kucing": "/api/kucing",
    "keranjang": "/api/keranjang",
    "pesanan": "/api/pesanan",
    "pembayaran": "/api/pembayaran",
    "admin": "/api/admin",
    "knowledge": "/api/knowledge"
  }
}
```

#### GET /health
Health check endpoint
- **Method:** GET
- **Authentication:** Tidak diperlukan
- **Response:**
```json
{
  "status": "ok",
  "message": "Server is healthy"
}
```

---

### 2. Authentication (/api/auth)

#### POST /api/auth/register
Registrasi user baru
- **Method:** POST
- **Authentication:** Tidak diperlukan
- **Request Body:**
```json
{
  "namaLengkap": "John Doe",
  "email": "john@example.com",
  "password": "password123",
  "role": "USER" // optional, default: USER
}
```
- **Response Success (201):**
```json
{
  "status": 201,
  "message": "Akun berhasil didaftarkan"
}
```
- **Response Error (400):**
```json
{
  "status": 400,
  "message": "Field namaLengkap, email, password wajib"
}
```
- **Response Error (409):**
```json
{
  "status": 409,
  "message": "Email sudah terdaftar"
}
```

#### POST /api/auth/login
Login user
- **Method:** POST
- **Authentication:** Tidak diperlukan
- **Request Body:**
```json
{
  "email": "john@example.com",
  "password": "password123"
}
```
- **Response Success (200):**
```json
{
  "status": 200,
  "data": {
    "_id": "user_id",
    "namaLengkap": "John Doe",
    "email": "john@example.com",
    "role": "USER",
    "token": "jwt_token_here",
    "createdAt": "2024-01-01T00:00:00Z",
    "updatedAt": "2024-01-01T00:00:00Z"
  },
  "message": "Login berhasil"
}
```

---

### 3. User Management (/api/user)

#### GET /api/user/
Mendapatkan semua user (Admin only)
- **Method:** GET
- **Authentication:** JWT (Admin only)
- **Response Success (200):**
```json
{
  "status": 200,
  "data": [
    {
      "_id": "user_id",
      "namaLengkap": "John Doe",
      "email": "john@example.com",
      "role": "USER",
      "createdAt": "2024-01-01T00:00:00Z"
    }
  ],
  "total": 1
}
```

#### POST /api/user/
Membuat user baru (Admin only)
- **Method:** POST
- **Authentication:** JWT (Admin only)
- **Request Body:**
```json
{
  "namaLengkap": "Jane Doe",
  "email": "jane@example.com",
  "password": "password123",
  "role": "USER"
}
```

#### GET /api/user/{user_id}
Mendapatkan detail user (Admin atau user sendiri)
- **Method:** GET
- **Authentication:** JWT
- **Parameters:** user_id (string)

#### PUT /api/user/{user_id}
Update user (Admin atau user sendiri)
- **Method:** PUT
- **Authentication:** JWT
- **Parameters:** user_id (string)
- **Request Body:**
```json
{
  "namaLengkap": "Updated Name",
  "email": "updated@example.com"
}
```

#### DELETE /api/user/{user_id}
Hapus user (Admin only)
- **Method:** DELETE
- **Authentication:** JWT (Admin only)
- **Parameters:** user_id (string)

#### PUT /api/user/{user_id}/change-password
Ubah password user
- **Method:** PUT
- **Authentication:** JWT
- **Parameters:** user_id (string)
- **Request Body:**
```json
{
  "oldPassword": "old_password", // tidak wajib untuk admin
  "newPassword": "new_password"
}
```

#### GET /api/user/profile/me
Mendapatkan profil user yang sedang login
- **Method:** GET
- **Authentication:** JWT

---

### 4. Layanan (/api/layanan)

#### GET /api/layanan
Mendapatkan semua layanan
- **Method:** GET
- **Authentication:** Tidak diperlukan

#### POST /api/layanan
Membuat layanan baru (Admin only)
- **Method:** POST
- **Authentication:** JWT (Admin only)
- **Request Body:**
```json
{
  "namaLayanan": "Grooming Basic",
  "deskripsi": "Layanan grooming dasar",
  "harga": 50000,
  "estimasiWaktu": 60,
  "kategori": "grooming"
}
```

#### GET /api/layanan/{id}
Mendapatkan detail layanan
- **Method:** GET
- **Authentication:** Tidak diperlukan
- **Parameters:** id (string)

#### PUT /api/layanan/{id}
Update layanan (Admin only)
- **Method:** PUT
- **Authentication:** JWT (Admin only)
- **Parameters:** id (string)

#### DELETE /api/layanan/{id}
Hapus layanan (Admin only)
- **Method:** DELETE
- **Authentication:** JWT (Admin only)
- **Parameters:** id (string)

#### GET /api/layanan/{id_kucing}/rekomendasi
Mendapatkan rekomendasi layanan berdasarkan kucing
- **Method:** GET
- **Authentication:** JWT
- **Parameters:** id_kucing (string)

---

### 5. Kucing (/api/kucing)

#### GET /api/kucing
Mendapatkan kucing milik user yang login
- **Method:** GET
- **Authentication:** JWT

#### GET /api/kucing/all
Mendapatkan semua kucing (Admin only)
- **Method:** GET
- **Authentication:** JWT (Admin only)

#### POST /api/kucing
Menambah kucing baru
- **Method:** POST
- **Authentication:** JWT
- **Request Body:**
```json
{
  "namaKucing": "Fluffy",
  "jenisKucing": "Persian",
  "umur": 2,
  "beratBadan": 3.5,
  "jenisKelamin": "jantan",
  "warnaBulu": "putih"
}
```

#### PUT /api/kucing/{id}
Update data kucing
- **Method:** PUT
- **Authentication:** JWT
- **Parameters:** id (string)

#### DELETE /api/kucing/{id}
Hapus data kucing
- **Method:** DELETE
- **Authentication:** JWT
- **Parameters:** id (string)

---

### 6. Keranjang (/api/keranjang)

#### GET /api/keranjang
Mendapatkan isi keranjang user
- **Method:** GET
- **Authentication:** JWT
- **Response Success (200):**
```json
{
  "status": 200,
  "data": [
    {
      "layananId": "layanan_id",
      "kucingId": "kucing_id",
      "harga": 50000,
      "jadwal": "2024-01-15T10:00:00Z"
    }
  ],
  "totalHarga": 50000,
  "message": "List item keranjang ditemukan"
}
```

#### POST /api/keranjang/items
Menambah item ke keranjang
- **Method:** POST
- **Authentication:** JWT
- **Request Body:**
```json
{
  "layananId": "layanan_id",
  "kucingId": "kucing_id",
  "jadwal": "2024-01-15T10:00:00Z"
}
```

#### DELETE /api/keranjang/items/{id}
Hapus satu item dari keranjang
- **Method:** DELETE
- **Authentication:** Tidak diperlukan (bug?)
- **Parameters:** id (string)

#### DELETE /api/keranjang/items
Kosongkan keranjang
- **Method:** DELETE
- **Authentication:** JWT

---

### 7. Pesanan (/api/pesanan)

#### POST /api/pesanan/checkout
Checkout keranjang menjadi pesanan
- **Method:** POST
- **Authentication:** JWT
- **Request Body:**
```json
{
  "metodePembayaran": "cash" // atau "transfer"
}
```

#### GET /api/pesanan/
Mendapatkan semua pesanan user
- **Method:** GET
- **Authentication:** JWT
- **Response:**
```json
{
  "status": 200,
  "data": [
    {
      "_id": "pesanan_id",
      "userId": "user_id",
      "items": [...],
      "totalHarga": 100000,
      "metodePembayaran": "cash",
      "createdAt": "2024-01-01T00:00:00Z"
    }
  ],
  "summary": {
    "pending": 2,
    "proses": 1,
    "selesai": 3,
    "total_transaksi": 500000
  }
}
```

#### GET /api/pesanan/{pesanan_id}
Mendapatkan detail pesanan
- **Method:** GET
- **Authentication:** JWT
- **Parameters:** pesanan_id (string)

#### PUT /api/pesanan/item/{pesanan_item_id}
Update status item pesanan
- **Method:** PUT
- **Authentication:** JWT
- **Parameters:** pesanan_item_id (string)
- **Request Body:**
```json
{
  "statusPesanan": "PROSES" // PENDING, PROSES, SELESAI
}
```

---

### 8. Pembayaran (/api/pembayaran)

#### POST /api/pembayaran
Membuat pembayaran
- **Method:** POST
- **Authentication:** JWT
- **Request Body:**
```json
{
  "metodePembayaran": "cash",
  "items": [
    {
      "layananId": "layanan_id",
      "kucingId": "kucing_id",
      "harga": 50000
    }
  ]
}
```

---

### 9. Dashboard Admin (/api/dashboard)

#### GET /api/dashboard
Mendapatkan data dashboard admin
- **Method:** GET
- **Authentication:** JWT (Admin only)
- **Response:**
```json
{
  "status": 200,
  "data": {
    "totalUsers": 100,
    "totalLayanan": 10,
    "totalPesanan": 50,
    "totalRevenue": 5000000,
    "recentOrders": [...],
    "popularServices": [...]
  }
}
```

---

### 10. Knowledge Management (/api/knowledge)

#### GET /api/knowledge/{layananId}
Mendapatkan knowledge data untuk layanan (Admin only)
- **Method:** GET
- **Authentication:** JWT (Admin only)
- **Parameters:** layananId (string)

#### POST /api/knowledge/{layanan_id}
Membuat/update knowledge data (Admin only)
- **Method:** POST
- **Authentication:** JWT (Admin only)
- **Parameters:** layanan_id (string)
- **Request Body:**
```json
{
  "informasi": "Informasi tentang layanan",
  "tips": ["Tip 1", "Tip 2"],
  "rekomendasi": "Rekomendasi khusus"
}
```

---

## Error Codes

| Status Code | Description |
|-------------|-------------|
| 200 | OK - Request berhasil |
| 201 | Created - Resource berhasil dibuat |
| 400 | Bad Request - Request tidak valid |
| 401 | Unauthorized - Token tidak valid/tidak ada |
| 403 | Forbidden - Akses ditolak |
| 404 | Not Found - Resource tidak ditemukan |
| 409 | Conflict - Data sudah ada |
| 500 | Internal Server Error - Error server |

## Authentication Flow

1. **Register:** POST `/api/auth/register` dengan data user
2. **Login:** POST `/api/auth/login` untuk mendapatkan JWT token
3. **Use Token:** Sertakan token dalam header `Authorization: Bearer <token>` untuk endpoint yang memerlukan autentikasi
4. **Token Expiry:** Token akan expire setelah waktu tertentu, user perlu login ulang

## Data Models

### User
```json
{
  "_id": "ObjectId",
  "namaLengkap": "string",
  "email": "string",
  "password": "hashed_string",
  "role": "USER|ADMIN",
  "createdAt": "datetime",
  "updatedAt": "datetime"
}
```

### Kucing
```json
{
  "_id": "ObjectId",
  "userId": "ObjectId",
  "namaKucing": "string",
  "jenisKucing": "string",
  "umur": "number",
  "beratBadan": "number",
  "jenisKelamin": "string",
  "warnaBulu": "string",
  "createdAt": "datetime"
}
```

### Layanan
```json
{
  "_id": "ObjectId",
  "namaLayanan": "string",
  "deskripsi": "string",
  "harga": "number",
  "estimasiWaktu": "number",
  "kategori": "string",
  "createdAt": "datetime"
}
```

### Pesanan
```json
{
  "_id": "ObjectId",
  "userId": "ObjectId",
  "items": [
    {
      "layananId": "ObjectId",
      "kucingId": "ObjectId",
      "harga": "number",
      "estimasiWaktu": "number",
      "jadwal": "datetime",
      "statusPesanan": "PENDING|PROSES|SELESAI"
    }
  ],
  "totalHarga": "number",
  "metodePembayaran": "string",
  "createdAt": "datetime"
}
```

---

## Development Notes

- API ini menggunakan Flask sebagai framework backend
- Database MongoDB untuk penyimpanan data
- JWT untuk sistem autentikasi
- CORS enabled untuk akses cross-origin
- Deploy menggunakan Vercel (serverless)

## Contact & Support

Untuk pertanyaan atau dukungan teknis, silakan hubungi tim development.
