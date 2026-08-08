from celery import Celery
from celery.schedules import crontab
from datetime import date, timedelta

celery = Celery(
    "trekora",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

### Test Task
@celery.task
def test_task():
    return "Celery is working!"

### Daily Trek Reminder Task
@celery.task
def daily_trek_reminder():

    from app import app
    from models import Trek, Booking
    from flask_mail import Message
    from extensions import mail

    with app.app_context():

        tomorrow = date.today() + timedelta(days=1)

        treks = Trek.query.filter(
            Trek.start_date == tomorrow,
            Trek.status == "Open"
        ).all()

        sent_count = 0

        for trek in treks:

            bookings = Booking.query.filter_by(
                trek_id=trek.id,
                status="Booked"
            ).all()

            for booking in bookings:
                if not booking.user.email:
                    continue
                msg = Message(
                    subject=f"TrekOra Reminder - {trek.name}",
                    sender=app.config["MAIL_USERNAME"],
                    recipients=[booking.user.email]
                )
                msg.body = f"""
Hello {booking.user.name},

This is a reminder from TrekOra.

Your trek is scheduled for tomorrow.

Trek: {trek.name}
Location: {trek.location}
Difficulty: {trek.difficulty}
Start Date: {trek.start_date}
End Date: {trek.end_date}

Please be ready for your trek.

Thank you,
TrekOra Team
"""

                mail.send(msg)
                sent_count += 1 
                print(
                    f"EMAIL SENT → {booking.user.email} " # Debugging print statement
                    f"for trek '{trek.name}'"
                )

        print(
            f"Daily reminder completed. "
            f"{sent_count} email(s) sent."
        )

        return sent_count


celery.conf.beat_schedule = {
    "daily-trek-reminder": {
        "task": "celery_app.daily_trek_reminder",
        "schedule": crontab(hour=9, minute=0),
    },
}

celery.conf.timezone = "Asia/Kolkata"

### Monthly Trekking Report Task
@celery.task
def monthly_trekking_report():

    from app import app
    from reports import generate_monthly_report
    from models import User
    from flask_mail import Message
    from extensions import mail

    with app.app_context():

        html_report = generate_monthly_report()

        with open("monthly_trekking_report.html", "w", encoding="utf-8") as file:
            file.write(html_report)

        admin = User.query.filter_by(role="admin").first()

        if admin and admin.email:

            msg = Message(
                subject="TrekOra - Monthly Trekking Activity Report",
                sender=app.config["MAIL_USERNAME"],
                recipients=[admin.email]
            )

            msg.html = html_report

            mail.send(msg)

            print(f"Monthly report emailed to admin -> {admin.email}")

        print("Monthly trekking activity report generated successfully.")

        return "Monthly report generated successfully"

### Export Booking History Task
@celery.task
def export_booking_history_task(user_id):

    from app import app
    from models import Booking
    from extensions import mail
    from flask_mail import Message
    import csv
    import os

    with app.app_context():

        bookings = Booking.query.filter_by(
            user_id=user_id
        ).all()

        filename = f"booking_history_user_{user_id}.csv"

        filepath = os.path.join(
            app.root_path,
            filename
        )

        with open(
            filepath,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.writer(file)

            writer.writerow([
                "Booking ID",
                "Trek Name",
                "Location",
                "Difficulty",
                "Booking Date",
                "Booking Status",
                "Trek Status",
                "Start Date",
                "End Date"
            ])

            for booking in bookings:

                writer.writerow([
                    booking.id,
                    booking.trek.name,
                    booking.trek.location,
                    booking.trek.difficulty,
                    booking.booking_date,
                    booking.status,
                    booking.trek.status,
                    booking.trek.start_date,
                    booking.trek.end_date
                ])

        # Send completion email
        user = bookings[0].user if bookings else None

        if user and user.email:

            msg = Message(
                subject="TrekOra - CSV Export Completed",
                sender=app.config["MAIL_USERNAME"],
                recipients=[user.email]
            )

            msg.body = f"""
Hello {user.name},

Your TrekOra trekking history CSV export has been completed successfully.

File name:
{filename}

Your complete trekking booking history has been exported.

Thank you,
TrekOra Team
"""

            mail.send(msg)

            print(
                f"EXPORT EMAIL SENT → {user.email}"
            )

        print(
            f"CSV export completed for user {user_id}: {filename}"
        )

        return filename