"""
定时任务服务 - APScheduler
每分钟检查是否有课程超时未签到，触发通知
"""

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

# 延迟导入避免循环引用
scheduler = BackgroundScheduler()


def check_missed_classes(app):
    """检查超时未签到的课程，发送通知"""
    with app.app_context():
        from app import Schedule, CheckIn, GuardianLink, User
        from services.notification import notify_guardian_missed

        now = datetime.now()
        today_dow = now.weekday()  # 0=周一

        # 找到今天所有待签到的课程
        schedules = Schedule.query.filter_by(day_of_week=today_dow).all()

        for schedule in schedules:
            # 计算超时时间（课程开始 + 告警延迟）
            class_start = datetime.combine(now.date(), schedule.start_time)
            student = schedule.student

            # 查找所有监护人绑定
            links = GuardianLink.query.filter_by(
                student_id=student.id,
                is_active=True
            ).all()

            for link in links:
                guardian = link.guardian
                delay = link.alert_delay_minutes
                deadline = class_start + timedelta(minutes=delay)

                # 检查是否超时
                if now >= deadline:
                    # 检查今天是否已有签到记录
                    existing = CheckIn.query.filter_by(
                        student_id=student.id,
                        schedule_id=schedule.id
                    ).filter(
                        __import__('app').db.func.date(CheckIn.checkin_time) == now.date()
                    ).first()

                    if not existing:
                        # 获取监护人配置（这里简化处理，实际应从用户设置读取）
                        guardian_email = guardian.email
                        sckey = None  # 从 guardian 设置中读取

                        logger.info(
                            f"[旷课检测] {student.username} 未签到 "
                            f"{schedule.course_name}，通知 {guardian.username}"
                        )

                        notify_guardian_missed(
                            guardian_email=guardian_email,
                            guardian_sckey=sckey,
                            student_name=student.username,
                            course_name=schedule.course_name,
                            start_time=schedule.start_time.strftime('%H:%M'),
                            location=schedule.location or ''
                        )


def init_scheduler(app):
    """启动定时任务调度器"""
    scheduler.add_job(
        func=lambda: check_missed_classes(app),
        trigger=IntervalTrigger(minutes=1),
        id='check_missed_classes',
        name='检查超时未签到',
        replace_existing=True
    )
    scheduler.start()
    logger.info("[调度器] 已启动，每分钟检查旷课情况")


def stop_scheduler():
    """停止调度器"""
    if scheduler.running:
        scheduler.shutdown()
        logger.info("[调度器] 已停止")
