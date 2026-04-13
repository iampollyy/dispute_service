from database import SessionLocal
from models import Dispute


def seed_data():
    db = SessionLocal()
    try:
        if db.query(Dispute).first():
            print("[DisputeService] Данные уже существуют, пропускаем seed.")
            return

        disputes = [
            Dispute(
                artwork_id=1,
                bid_id=1,
                user_id=1,
                event_type="BidPlaced",
                status="open",
                is_resolved=False,
                description="Suspicious bidding pattern detected on artwork #1"
            ),
            Dispute(
                artwork_id=2,
                bid_id=3,
                user_id=3,
                event_type="SuspiciousBidDetected",
                status="investigating",
                is_resolved=False,
                description="Bid amount is unusually high for this category"
            ),
            Dispute(
                artwork_id=2,
                bid_id=4,
                user_id=1,
                event_type="AuctionCompleted",
                status="resolved",
                is_resolved=True,
                description="Dispute about auction completion timing",
                resolved_by="admin@artauction.com"
            ),
            Dispute(
                artwork_id=1,
                bid_id=2,
                user_id=2,
                event_type="BidPlaced",
                status="open",
                is_resolved=False,
                description="User claims bid was placed by mistake"
            ),
        ]
        db.add_all(disputes)
        db.commit()
        print("[DisputeService] Seed данные добавлены успешно!")
    except Exception as e:
        db.rollback()
        print(f"[DisputeService] Ошибка при seed: {e}")
    finally:
        db.close()