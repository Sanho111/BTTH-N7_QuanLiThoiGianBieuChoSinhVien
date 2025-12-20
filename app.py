from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'your_strong_secret_key_here'

class User:
    def __init__(self, email, password):
        self._email = email
        self._password_hash = self._hash_password(password)
        
    def _hash_password(self, password):
        return f"hashed_{password}" 

    def get_email(self):
        return self._email
        
    def check_password(self, raw_password):
        return self._password_hash == self._hash_password(raw_password)

    def set_password(self, new_password):
        self._password_hash = self._hash_password(new_password)

MOCK_DATABASE = {
    "student@email.com": User("student@email.com", "password123")
}

OTP_MAU = "123456"

@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user_in_db = MOCK_DATABASE.get(email)
        
        if user_in_db and user_in_db.check_password(password):
            flash(f"Đăng nhập thành công! Chào mừng {user_in_db.get_email()}", 'success')
            return redirect(url_for('schedule'))
        else:
            flash("Email hoặc Mật khẩu không đúng.", 'error')
            
    return render_template('login.html')

@app.route('/reset-password', methods=['POST'])
def reset_password():
    email = request.form.get('reset_email')
    new_pass = request.form.get('new_password')
    otp_input = request.form.get('otp')

    print(f"----------------------------------------")
    print(f"DEBUG: Đang xử lý đổi mật khẩu cho: {email}")
    print(f"DEBUG: OTP Nhận được từ form: '{otp_input}'")
    print(f"DEBUG: OTP Mẫu quy định:      '{OTP_MAU}'")
    print(f"----------------------------------------")

    if not otp_input or otp_input.strip() != OTP_MAU:
        flash("Mã OTP không chính xác! Vui lòng kiểm tra lại.", "error")
        print("-> KẾT QUẢ: Thất bại do sai OTP") 
        return redirect(url_for('login'))

    user = MOCK_DATABASE.get(email)
    
    if user:
        user.set_password(new_pass)
        print("-> KẾT QUẢ: Đã cập nhật mật khẩu cho user cũ.")
    else:
        new_user = User(email, new_pass)
        MOCK_DATABASE[email] = new_user
        print("-> KẾT QUẢ: Đã tạo tài khoản mới từ email lạ.")
        
    flash(f"Thành công! Mật khẩu cho '{email}' đã được cập nhật.", "success")
    return redirect(url_for('login'))

@app.route('/schedule')
def schedule():
    return render_template('schedule.html')

@app.route('/register', methods=['POST'])
def register():
    email = request.form.get('reg_email')
    password = request.form.get('reg_password')
    confirm_password = request.form.get('reg_confirm_password')

    if not email or not password or not confirm_password:
        flash("Vui lòng nhập đầy đủ thông tin!", "error")
        return redirect(url_for('login'))

    if password != confirm_password:
        flash("Mật khẩu xác nhận không khớp!", "error")
        return redirect(url_for('login'))

    if email in MOCK_DATABASE:
        flash("Tài khoản này đã tồn tại!", "error")
        return redirect(url_for('login'))

    new_user = User(email, password)
    MOCK_DATABASE[email] = new_user

    flash(f"Đăng ký thành công! Chào mừng '{email}'. Hãy đăng nhập ngay.", "success")
    return redirect(url_for('login'))
    
if __name__ == '__main__':
    app.run(debug=True)