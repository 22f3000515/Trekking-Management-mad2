from datetime import datetime
from models import Trek, Booking


def generate_monthly_report():

    current_month = datetime.utcnow().month
    current_year = datetime.utcnow().year

    # Treks conducted this month
    treks = Trek.query.filter(
        Trek.status == "Completed"
    ).all()

    conducted_treks = []

    for trek in treks:
        if trek.end_date.year == current_year and trek.end_date.month == current_month:
            conducted_treks.append(trek)

    total_treks = len(conducted_treks)

    # Total participants
    total_participants = 0

    for trek in conducted_treks:
        total_participants += Booking.query.filter_by(
            trek_id=trek.id,
            status="Completed"
        ).count()

    # Popular treks
    popular_treks = []

    for trek in conducted_treks:

        participant_count = Booking.query.filter_by(
            trek_id=trek.id,
            status="Completed"
        ).count()

        popular_treks.append({
            "name": trek.name,
            "participants": participant_count
        })

    popular_treks.sort(
        key=lambda x: x["participants"],
        reverse=True
    )

    # HTML report
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Monthly Trekking Activity Report</title>

        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 40px;
            }}

            h1 {{
                text-align: center;
            }}

            .summary {{
                display: flex;
                gap: 20px;
                margin: 30px 0;
            }}

            .card {{
                border: 1px solid #ddd;
                padding: 20px;
                flex: 1;
                text-align: center;
            }}

            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
            }}

            th, td {{
                border: 1px solid #ddd;
                padding: 10px;
            }}

            th {{
                background-color: #f2f2f2;
            }}
        </style>
    </head>

    <body>

        <h1>Monthly Trekking Activity Report</h1>

        <p>
            Report Period:
            {current_month}/{current_year}
        </p>

        <div class="summary">

            <div class="card">
                <h2>{total_treks}</h2>
                <p>Treks Conducted</p>
            </div>

            <div class="card">
                <h2>{total_participants}</h2>
                <p>Total Participants</p>
            </div>

        </div>

        <h2>Popular Treks</h2>

        <table>

            <tr>
                <th>Rank</th>
                <th>Trek Name</th>
                <th>Participants</th>
            </tr>
    """

    for index, trek in enumerate(popular_treks, start=1):

        html += f"""
            <tr>
                <td>{index}</td>
                <td>{trek["name"]}</td>
                <td>{trek["participants"]}</td>
            </tr>
        """

    html += """
        </table>

    </body>
    </html>
    """

    return html