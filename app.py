"""
旷了吗 - 学生安全签到工具
Flask 主应用入口
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta, time as dt_time
import os

# ==================== App 初始化 ====================
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'kuangle-secret-key-2026')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///kuangle.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# ==================== 数据库模型 ====================

class User(UserMixin, db.Model):
    """用户模型（学生/家长共用）"""
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(10), default='student')  # student / guardian
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 关联
    schedules = db.relationship('Schedule', backref='student', lazy='dynamic')
    guardian_links = db.relationship('GuardianLink', foreign_keys='GuardianLink.student_id', backref='student', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Schedule(db.Model):
    """课程表"""
    __tablename__ = 'schedules'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    day_of_week = db.Column(db.Integer, nullable=False)  # 0=周一, 6=周日
    course_name = db.Column(db.String(100), nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    location = db.Column(db.String(100))
    checkin_code = db.Column(db.String(6))  # 随机验证码（可选）
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class CheckIn(db.Model):
    """签到记录"""
    __tablename__ = 'checkins'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    schedule_id = db.Column(db.Integer, db.ForeignKey('schedules.id'), nullable=False)
    status = db.Column(db.String(10), default='checked_in')  # checked_in / missed / late
    checkin_time = db.Column(db.DateTime, default=datetime.utcnow)
    schedule = db.relationship('Schedule', backref='checkins')

    student = db.relationship('User', backref='checkins')


class GuardianLink(db.Model):
    """监护人绑定关系"""
    __tablename__ = 'guardian_links'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    guardian_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    guardian = db.relationship('User', foreign_keys=[guardian_id])
    alert_delay_minutes = db.Column(db.Integer, default=15)  # 超过多少分钟未签到才提醒
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# ==================== 登录管理器 ====================

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ==================== 路由：首页 & 认证 ====================

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        role = data.get('role', 'student')

        if User.query.filter_by(username=username).first():
            return jsonify({'success': False, 'message': '用户名已存在'}), 400
        if User.query.filter_by(email=email).first():
            return jsonify({'success': False, 'message': '邮箱已被注册'}), 400

        user = User(username=username, email=email, role=role)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        login_user(user)
        return jsonify({'success': True, 'message': '注册成功', 'redirect': url_for('dashboard')})

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        user = User.query.filter_by(username=data.get('username')).first()

        if user and user.check_password(data.get('password')):
            login_user(user)
            return jsonify({'success': True, 'message': '登录成功', 'redirect': url_for('dashboard')})
        return jsonify({'success': False, 'message': '用户名或密码错误'}), 401

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


# ==================== 路由：控制台 ====================

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'student':
        return render_template('student_dashboard.html')
    else:
        return render_template('guardian_dashboard.html')


# ==================== 路由：课程表管理 ====================

@app.route('/api/schedules', methods=['GET', 'POST'])
@login_required
def api_schedules():
    if current_user.role != 'student':
        return jsonify({'error': '只有学生可以管理课程表'}), 403

    if request.method == 'POST':
        data = request.get_json()
        schedule = Schedule(
            student_id=current_user.id,
            day_of_week=int(data['day_of_week']),
            course_name=data['course_name'],
            start_time=datetime.strptime(data['start_time'], '%H:%M').time(),
            end_time=datetime.strptime(data['end_time'], '%H:%M').time(),
            location=data.get('location', '')
        )
        db.session.add(schedule)
        db.session.commit()
        return jsonify({'success': True, 'schedule_id': schedule.id})

    # GET: 获取本周课程
    schedules = Schedule.query.filter_by(student_id=current_user.id).all()
    return jsonify([{
        'id': s.id,
        'day_of_week': s.day_of_week,
        'course_name': s.course_name,
        'start_time': s.start_time.strftime('%H:%M'),
        'end_time': s.end_time.strftime('%H:%M'),
        'location': s.location
    } for s in schedules])


@app.route('/api/schedules/<int:schedule_id>', methods=['DELETE'])
@login_required
def delete_schedule(schedule_id):
    schedule = Schedule.query.filter_by(id=schedule_id, student_id=current_user.id).first()
    if not schedule:
        return jsonify({'error': '未找到该课程'}), 404
    db.session.delete(schedule)
    db.session.commit()
    return jsonify({'success': True})


# ==================== 路由：签到 ====================

@app.route('/api/today-schedules')
@login_required
def today_schedules():
    """获取今日课程"""
    today = datetime.now().weekday()
    schedules = Schedule.query.filter_by(student_id=current_user.id, day_of_week=today).order_by(Schedule.start_time).all()
    result = []
    for s in schedules:
        # 查找本次课的签到记录
        checkin = CheckIn.query.filter_by(
            student_id=current_user.id,
            schedule_id=s.id
        ).filter(
            db.func.date(CheckIn.checkin_time) == datetime.now().date()
        ).first()

        # 判断是否超时
        now = datetime.now()
        class_start = datetime.combine(datetime.now().date(), s.start_time)
        status = 'pending'
        if checkin:
            status = checkin.status
        elif now > class_start + timedelta(minutes=10):
            status = 'missed'

        result.append({
            'id': s.id,
            'course_name': s.course_name,
            'start_time': s.start_time.strftime('%H:%M'),
            'end_time': s.end_time.strftime('%H:%M'),
            'location': s.location,
            'status': status,
            'checked_in': checkin is not None
        })
    return jsonify(result)


@app.route('/api/checkin/<int:schedule_id>', methods=['POST'])
@login_required
def checkin(schedule_id):
    """签到"""
    schedule = Schedule.query.filter_by(id=schedule_id, student_id=current_user.id).first()
    if not schedule:
        return jsonify({'error': '未找到该课程'}), 404

    # 检查今天是否已签到
    existing = CheckIn.query.filter_by(
        student_id=current_user.id,
        schedule_id=schedule_id
    ).filter(
        db.func.date(CheckIn.checkin_time) == datetime.now().date()
    ).first()

    if existing:
        return jsonify({'error': '今日已签到'}), 400

    # 判断是否迟到（超过课程开始10分钟）
    now = datetime.now()
    class_start = datetime.combine(datetime.now().date(), schedule.start_time)
    is_late = now > class_start + timedelta(minutes=10)

    checkin = CheckIn(
        student_id=current_user.id,
        schedule_id=schedule_id,
        status='late' if is_late else 'checked_in'
    )
    db.session.add(checkin)
    db.session.commit()

    return jsonify({
        'success': True,
        'status': checkin.status,
        'checkin_time': checkin.checkin_time.strftime('%H:%M:%S')
    })


# ==================== 路由：监护人 ====================

@app.route('/api/guardian/bind', methods=['POST'])
@login_required
def bind_guardian():
    """学生绑定监护人"""
    data = request.get_json()
    guardian_username = data.get('guardian_username')
    alert_delay = int(data.get('alert_delay_minutes', 15))

    guardian = User.query.filter_by(username=guardian_username, role='guardian').first()
    if not guardian:
        return jsonify({'success': False, 'message': '未找到该监护人账号'}), 404

    # 检查是否已绑定
    existing = GuardianLink.query.filter_by(
        student_id=current_user.id,
        guardian_id=guardian.id
    ).first()
    if existing:
        return jsonify({'success': False, 'message': '已绑定该监护人'}), 400

    link = GuardianLink(
        student_id=current_user.id,
        guardian_id=guardian.id,
        alert_delay_minutes=alert_delay
    )
    db.session.add(link)
    db.session.commit()
    return jsonify({'success': True, 'message': f'已绑定监护人 {guardian_username}'})


@app.route('/api/guardian/students')
@login_required
def guardian_students():
    """监护人查看已绑定的学生"""
    links = GuardianLink.query.filter_by(guardian_id=current_user.id, is_active=True).all()
    result = []
    for link in links:
        student = link.student
        today = datetime.now().weekday()
        today_schedules = Schedule.query.filter_by(
            student_id=student.id, day_of_week=today
        ).order_by(Schedule.start_time).all()

        schedules_data = []
        for s in today_schedules:
            checkin = CheckIn.query.filter_by(
                student_id=student.id,
                schedule_id=s.id
            ).filter(
                db.func.date(CheckIn.checkin_time) == datetime.now().date()
            ).first()
            schedules_data.append({
                'course_name': s.course_name,
                'start_time': s.start_time.strftime('%H:%M'),
                'status': checkin.status if checkin else 'not_checked_in',
                'checked_in': checkin is not None
            })

        result.append({
            'student_id': student.id,
            'student_name': student.username,
            'alert_delay': link.alert_delay_minutes,
            'today_schedules': schedules_data
        })
    return jsonify(result)


# ==================== 路由：统计报表 ====================

@app.route('/api/stats/weekly')
@login_required
def weekly_stats():
    """本周签到统计"""
    start_of_week = datetime.now() - timedelta(days=datetime.now().weekday())
    end_of_week = start_of_week + timedelta(days=7)

    checkins = CheckIn.query.filter(
        CheckIn.student_id == current_user.id,
        CheckIn.checkin_time >= start_of_week,
        CheckIn.checkin_time < end_of_week
    ).all()

    total = len(checkins)
    on_time = sum(1 for c in checkins if c.status == 'checked_in')
    late = sum(1 for c in checkins if c.status == 'late')
    missed = CheckIn.query.filter(
        CheckIn.student_id == current_user.id,
        CheckIn.schedule_id.in_([s.id for s in current_user.schedules]),
        CheckIn.status == 'missed',
        CheckIn.checkin_time >= start_of_week,
        CheckIn.checkin_time < end_of_week
    ).count()

    return jsonify({
        'total': total,
        'on_time': on_time,
        'late': late,
        'missed': missed,
        'rate': round((on_time / total * 100) if total > 0 else 100, 1)
    })


# ==================== 启动 ====================

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
