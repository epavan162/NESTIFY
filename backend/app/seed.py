"""Seed data script for Nestify development — rich showcase data."""
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import date, datetime, time, timezone, timedelta
from app.database import SessionLocal, engine, Base
from app.models import (
    Society, Tower, Flat, User,
    MaintenanceInvoice, Payment, Complaint,
    Visitor, Notice, Booking, Poll, Vote,
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def seed():
    # Create all tables
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        # Check if data already exists
        if db.query(Society).first():
            print("[SEED] Data already exists, skipping.")
            return

        print("[SEED] Creating comprehensive showcase data...")

        # =================== SOCIETIES ===================
        society = Society(
            name="Emerald Heights",
            address="123 Park Avenue, Sector 42",
            city="Bangalore",
            state="Karnataka",
            pincode="560001",
        )
        society2 = Society(
            name="Royal Gardens",
            address="456 Lake View Road, Whitefield",
            city="Bangalore",
            state="Karnataka",
            pincode="560066",
        )
        db.add_all([society, society2])
        db.flush()

        # =================== TOWERS ===================
        tower_a = Tower(society_id=society.id, name="Tower A - Diamond", total_floors=15)
        tower_b = Tower(society_id=society.id, name="Tower B - Sapphire", total_floors=12)
        tower_c = Tower(society_id=society.id, name="Tower C - Ruby", total_floors=10)
        tower_r1 = Tower(society_id=society2.id, name="Block 1 - Lotus", total_floors=8)
        db.add_all([tower_a, tower_b, tower_c, tower_r1])
        db.flush()

        # =================== FLATS ===================
        flats = []
        # Tower A: 20 flats (floors 1-5, 4 units each)
        for floor in range(1, 6):
            for unit in range(1, 5):
                flat = Flat(
                    tower_id=tower_a.id,
                    flat_number=f"A-{floor}0{unit}",
                    floor=floor,
                    area_sqft=1200 + (unit * 100),
                    flat_type=["1BHK", "2BHK", "3BHK", "3BHK"][unit - 1],
                )
                flats.append(flat)
        # Tower B: 12 flats
        for floor in range(1, 5):
            for unit in range(1, 4):
                flat = Flat(
                    tower_id=tower_b.id,
                    flat_number=f"B-{floor}0{unit}",
                    floor=floor,
                    area_sqft=1100 + (unit * 150),
                    flat_type=["2BHK", "2BHK", "3BHK"][unit - 1],
                )
                flats.append(flat)
        # Tower C: 8 flats
        for floor in range(1, 3):
            for unit in range(1, 5):
                flat = Flat(
                    tower_id=tower_c.id,
                    flat_number=f"C-{floor}0{unit}",
                    floor=floor,
                    area_sqft=1500 + (unit * 200),
                    flat_type=["3BHK", "4BHK", "3BHK", "4BHK"][unit - 1],
                )
                flats.append(flat)
        db.add_all(flats)
        db.flush()

        # =================== USERS (10 users) ===================
        admin = User(
            name="Rajesh Kumar", email="admin@nestify.com", phone="9876543210",
            password_hash=pwd_context.hash("admin123"),
            role="admin", society_id=society.id, flat_id=flats[0].id,
            is_owner=True, moved_in_at=datetime(2023, 1, 15, tzinfo=timezone.utc),
        )
        resident1 = User(
            name="Priya Sharma", email="priya@nestify.com", phone="9876543211",
            password_hash=pwd_context.hash("resident123"),
            role="resident", society_id=society.id, flat_id=flats[1].id,
            is_owner=True, moved_in_at=datetime(2023, 3, 10, tzinfo=timezone.utc),
        )
        resident2 = User(
            name="Amit Patel", email="amit@nestify.com", phone="9876543212",
            password_hash=pwd_context.hash("resident123"),
            role="resident", society_id=society.id, flat_id=flats[2].id,
            is_owner=False, moved_in_at=datetime(2023, 6, 1, tzinfo=timezone.utc),
        )
        resident3 = User(
            name="Sneha Reddy", email="sneha@nestify.com", phone="9876543215",
            password_hash=pwd_context.hash("resident123"),
            role="resident", society_id=society.id, flat_id=flats[3].id,
            is_owner=True, moved_in_at=datetime(2023, 8, 20, tzinfo=timezone.utc),
        )
        resident4 = User(
            name="Vikram Singh", email="vikram@nestify.com", phone="9876543216",
            password_hash=pwd_context.hash("resident123"),
            role="resident", society_id=society.id, flat_id=flats[4].id,
            is_owner=True, moved_in_at=datetime(2024, 1, 5, tzinfo=timezone.utc),
        )
        resident5 = User(
            name="Ananya Iyer", email="ananya@nestify.com", phone="9876543217",
            password_hash=pwd_context.hash("resident123"),
            role="resident", society_id=society.id, flat_id=flats[20].id,
            is_owner=False, moved_in_at=datetime(2024, 4, 12, tzinfo=timezone.utc),
        )
        resident6 = User(
            name="Rohit Gupta", email="rohit@nestify.com", phone="9876543218",
            password_hash=pwd_context.hash("resident123"),
            role="resident", society_id=society.id, flat_id=flats[21].id,
            is_owner=True, moved_in_at=datetime(2024, 6, 1, tzinfo=timezone.utc),
        )
        security = User(
            name="Suresh Guard", email="security@nestify.com", phone="9876543213",
            password_hash=pwd_context.hash("security123"),
            role="security", society_id=society.id,
        )
        treasurer = User(
            name="Meena Finance", email="treasurer@nestify.com", phone="9876543214",
            password_hash=pwd_context.hash("treasurer123"),
            role="treasurer", society_id=society.id, flat_id=flats[5].id,
            is_owner=True, moved_in_at=datetime(2023, 2, 20, tzinfo=timezone.utc),
        )
        security2 = User(
            name="Ravi Watchman", email="ravi@nestify.com", phone="9876543219",
            password_hash=pwd_context.hash("security123"),
            role="security", society_id=society.id,
        )
        all_users = [admin, resident1, resident2, resident3, resident4, resident5, resident6, security, treasurer, security2]
        db.add_all(all_users)
        db.flush()

        all_residents = [admin, resident1, resident2, resident3, resident4, resident5, resident6, treasurer]

        # =================== MAINTENANCE INVOICES & PAYMENTS ===================
        today = date.today()
        # Create invoices from 5 months ago to current month for rich dashboard data
        invoice_months = []
        for i in range(5, -1, -1):
            m = today.month - i
            y = today.year
            while m <= 0:
                m += 12
                y -= 1
            invoice_months.append((m, y))

        for month_idx, (m, y) in enumerate(invoice_months):
            for idx, flat in enumerate(flats[:8]):
                amount = 5000.0 if flat.flat_type in ("2BHK", "1BHK") else 7500.0
                due = date(y, m, 10)

                # Last 4 months: paid, month before current: some overdue, current: pending
                if month_idx < len(invoice_months) - 2:
                    status = "paid"
                    late_fee = 0.0
                elif month_idx == len(invoice_months) - 2:
                    # Previous month: some paid, some overdue
                    if idx in (2, 5, 7):
                        status = "overdue"
                        late_fee = amount * 0.1
                    else:
                        status = "paid"
                        late_fee = 0.0
                else:
                    status = "pending"
                    late_fee = 0.0

                total = amount + late_fee

                inv = MaintenanceInvoice(
                    society_id=society.id, flat_id=flat.id,
                    amount=amount, total_amount=total, late_fee=late_fee,
                    due_date=due, month=m, year=y, status=status,
                )
                db.add(inv)
                db.flush()

                if status == "paid" and idx < len(all_residents):
                    user_for_payment = all_residents[idx]
                    payment = Payment(
                        invoice_id=inv.id, user_id=user_for_payment.id,
                        amount=amount, payment_method=["upi", "bank_transfer", "card", "cash"][idx % 4],
                        transaction_id=f"TXN-{y}{m:02d}-{flat.flat_number}",
                    )
                    db.add(payment)

        # =================== COMPLAINTS (8 complaints) ===================
        complaints_data = [
            {"user": resident1, "flat": flats[1], "title": "Water leakage in bathroom",
             "desc": "There is continuous water leakage from the ceiling in the master bathroom. Paint is peeling off.",
             "status": "open", "priority": "high"},
            {"user": resident2, "flat": flats[2], "title": "Lift not working",
             "desc": "Tower A lift #2 has been out of service since yesterday. Very inconvenient for elderly residents.",
             "status": "in_progress", "priority": "urgent", "assigned_to": admin.id},
            {"user": admin, "flat": flats[0], "title": "Street light broken",
             "desc": "The street light near parking lot B3 is not working. Safety concern at night.",
             "status": "resolved", "priority": "low"},
            {"user": resident3, "flat": flats[3], "title": "Noise from construction",
             "desc": "Ongoing construction work in adjacent flat is causing excessive noise during rest hours.",
             "status": "open", "priority": "medium"},
            {"user": resident4, "flat": flats[4], "title": "Parking space encroachment",
             "desc": "My assigned parking spot B-23 is frequently occupied by an unidentified vehicle.",
             "status": "open", "priority": "high"},
            {"user": resident5, "flat": flats[20], "title": "AC outdoor unit vibration",
             "desc": "The AC outdoor unit on the balcony is creating excessive vibration and noise.",
             "status": "in_progress", "priority": "medium", "assigned_to": admin.id},
            {"user": resident6, "flat": flats[21], "title": "Pest control needed",
             "desc": "Cockroach infestation in the kitchen area. Request immediate pest control service.",
             "status": "open", "priority": "high"},
            {"user": treasurer, "flat": flats[5], "title": "Garden maintenance overdue",
             "desc": "The common garden area has not been maintained for 3 weeks. Plants are dying.",
             "status": "resolved", "priority": "low"},
        ]
        for cd in complaints_data:
            complaint = Complaint(
                society_id=society.id, user_id=cd["user"].id, flat_id=cd["flat"].id,
                title=cd["title"], description=cd["desc"],
                status=cd["status"], priority=cd["priority"],
                assigned_to=cd.get("assigned_to"),
            )
            db.add(complaint)

        # =================== VISITORS (8 visitors) ===================
        visitors_data = [
            {"flat": flats[0], "name": "Delivery Agent - Amazon", "phone": "9000000001",
             "purpose": "Package delivery", "status": "approved", "approved_by": admin.id},
            {"flat": flats[1], "name": "Ramesh (Plumber)", "phone": "9000000002",
             "purpose": "Plumbing repair", "status": "pending"},
            {"flat": flats[2], "name": "Dr. Sunil Mehta", "phone": "9000000003",
             "purpose": "Medical visit", "status": "approved", "approved_by": resident2.id},
            {"flat": flats[3], "name": "Swiggy delivery", "phone": "9000000004",
             "purpose": "Food delivery", "status": "checked_out", "approved_by": security.id},
            {"flat": flats[0], "name": "Kabir (Friend)", "phone": "9000000005",
             "purpose": "Personal visit", "status": "approved", "approved_by": admin.id},
            {"flat": flats[4], "name": "Flipkart delivery", "phone": "9000000006",
             "purpose": "Package delivery", "status": "pending",
             "vehicle": "KA-01-AB-1234"},
            {"flat": flats[1], "name": "Electrician - Raju", "phone": "9000000007",
             "purpose": "Electrical repair", "status": "approved", "approved_by": resident1.id},
            {"flat": flats[20], "name": "Interior designer", "phone": "9000000008",
             "purpose": "Site inspection", "status": "pending",
             "vehicle": "KA-05-CD-5678"},
        ]
        for vd in visitors_data:
            visitor = Visitor(
                society_id=society.id, flat_id=vd["flat"].id,
                visitor_name=vd["name"], visitor_phone=vd["phone"],
                purpose=vd["purpose"], status=vd["status"],
                approved_by=vd.get("approved_by"),
                vehicle_number=vd.get("vehicle"),
            )
            db.add(visitor)

        # =================== NOTICES (5 notices) ===================
        notices_data = [
            {"title": "Annual General Meeting", "category": "event",
             "content": "The AGM will be held on March 15, 2026 at the Community Hall at 6:00 PM. All flat owners are requested to attend. Agenda: Budget approval, new committee election, and facility upgrades discussion."},
            {"title": "Water Supply Maintenance", "category": "maintenance",
             "content": "Water supply will be interrupted on Feb 22 from 10 AM to 2 PM for overhead tank cleaning and pipeline inspection. Please store water accordingly."},
            {"title": "Diwali Celebration", "category": "event",
             "content": "Grand Diwali celebration at the clubhouse on Oct 28. Cultural programs, rangoli competition, and community dinner. All families are welcome! RSVP by Oct 25."},
            {"title": "New Parking Rules", "category": "general",
             "content": "Starting March 1, all vehicles must display the society parking sticker. Unregistered vehicles will not be allowed entry after 10 PM. Register your vehicle at the security office."},
            {"title": "Emergency: Gas Leak Drill", "category": "emergency",
             "content": "A mock gas leak evacuation drill will be conducted on Feb 25 at 11 AM. All residents must participate. Assembly point: Garden Area near Tower A entrance."},
        ]
        for nd in notices_data:
            notice = Notice(
                society_id=society.id, title=nd["title"],
                content=nd["content"], category=nd["category"],
                created_by=admin.id,
            )
            db.add(notice)

        # =================== BOOKINGS (6 bookings) ===================
        tomorrow = today + timedelta(days=1)
        next_week = today + timedelta(days=7)
        bookings_data = [
            {"user": resident1, "facility": "Party Hall", "date": tomorrow,
             "start": time(18, 0), "end": time(22, 0), "status": "confirmed"},
            {"user": resident2, "facility": "Gym", "date": tomorrow,
             "start": time(6, 0), "end": time(7, 0), "status": "confirmed"},
            {"user": resident3, "facility": "Swimming Pool", "date": tomorrow,
             "start": time(7, 0), "end": time(8, 0), "status": "confirmed"},
            {"user": resident4, "facility": "Tennis Court", "date": next_week,
             "start": time(17, 0), "end": time(18, 30), "status": "confirmed"},
            {"user": admin, "facility": "Clubhouse", "date": next_week,
             "start": time(19, 0), "end": time(22, 0), "status": "confirmed"},
            {"user": resident5, "facility": "Gym", "date": today,
             "start": time(8, 0), "end": time(9, 0), "status": "confirmed"},
        ]
        for bd in bookings_data:
            booking = Booking(
                society_id=society.id, user_id=bd["user"].id,
                facility_name=bd["facility"], booking_date=bd["date"],
                start_time=bd["start"], end_time=bd["end"],
                status=bd["status"],
            )
            db.add(booking)

        # =================== POLLS (3 polls with votes) ===================
        poll1 = Poll(
            society_id=society.id,
            question="Should we install EV charging stations in the parking area?",
            options=["Yes, definitely", "No, not needed", "Yes, but later"],
            created_by=admin.id,
        )
        poll2 = Poll(
            society_id=society.id,
            question="What time should the swimming pool operate on weekends?",
            options=["6 AM - 9 PM", "7 AM - 10 PM", "5 AM - 8 PM", "Open 24 hours"],
            created_by=admin.id,
        )
        poll3 = Poll(
            society_id=society.id,
            question="Should we hire a full-time society manager?",
            options=["Yes, hire immediately", "No, current setup is fine", "Need more information"],
            created_by=admin.id,
        )
        db.add_all([poll1, poll2, poll3])
        db.flush()

        # Votes for poll 1
        poll1_votes = [
            Vote(poll_id=poll1.id, user_id=resident1.id, option_index=0),
            Vote(poll_id=poll1.id, user_id=resident2.id, option_index=0),
            Vote(poll_id=poll1.id, user_id=resident3.id, option_index=2),
            Vote(poll_id=poll1.id, user_id=resident4.id, option_index=0),
            Vote(poll_id=poll1.id, user_id=treasurer.id, option_index=2),
            Vote(poll_id=poll1.id, user_id=resident5.id, option_index=1),
        ]
        # Votes for poll 2
        poll2_votes = [
            Vote(poll_id=poll2.id, user_id=resident1.id, option_index=1),
            Vote(poll_id=poll2.id, user_id=resident2.id, option_index=0),
            Vote(poll_id=poll2.id, user_id=resident4.id, option_index=1),
            Vote(poll_id=poll2.id, user_id=resident6.id, option_index=3),
        ]
        # Votes for poll 3
        poll3_votes = [
            Vote(poll_id=poll3.id, user_id=resident1.id, option_index=0),
            Vote(poll_id=poll3.id, user_id=resident3.id, option_index=2),
            Vote(poll_id=poll3.id, user_id=treasurer.id, option_index=0),
        ]
        db.add_all(poll1_votes + poll2_votes + poll3_votes)

        db.commit()
        print("[SEED] Comprehensive showcase data created successfully!")
        print("[SEED] ==========================================")
        print("[SEED] 2 Societies, 4 Towers, 40 Flats")
        print("[SEED] 10 Users across all roles")
        print("[SEED] Maintenance invoices for all months")
        print("[SEED] 8 Complaints, 8 Visitors, 5 Notices")
        print("[SEED] 6 Facility Bookings, 3 Polls with votes")
        print("[SEED] ==========================================")
        print("[SEED] Login credentials:")
        print("       Admin:      admin@nestify.com / admin123")
        print("       Resident 1: priya@nestify.com / resident123")
        print("       Resident 2: amit@nestify.com / resident123")
        print("       Resident 3: sneha@nestify.com / resident123")
        print("       Resident 4: vikram@nestify.com / resident123")
        print("       Resident 5: ananya@nestify.com / resident123")
        print("       Resident 6: rohit@nestify.com / resident123")
        print("       Security:   security@nestify.com / security123")
        print("       Treasurer:  treasurer@nestify.com / treasurer123")

    except Exception as e:
        db.rollback()
        print(f"[SEED] Error: {e}")
        import traceback
        traceback.print_exc()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
