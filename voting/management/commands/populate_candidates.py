from django.core.management.base import BaseCommand
from voting.models import Position, Candidate

class Command(BaseCommand):
    help = 'Populate the database with sample university positions and candidates'

    def handle(self, *args, **kwargs):
        # Define positions and candidates
        election_data = [
            {"position": "Student Government President", "max_vote": 1, "candidates": [
                {"fullname": "Malcom Omollo", "bio": "Committed to student welfare and academic excellence"},
                {"fullname": "Benjamin Gitonga", "bio": "Focused on transparency and campus development"},
                {"fullname": "Brenda Njeri", "bio": "Advocate for inclusivity and student engagement"},
            ]},
            {"position": "Vice President", "max_vote": 1, "candidates": [
                {"fullname": "David Kimani", "bio": "Dedicated to student leadership and innovation"},
                {"fullname": "Joy Maraka", "bio": "Focused on campus events and student representation"},
            ]},
            {"position": "Secretary", "max_vote": 1, "candidates": [
                {"fullname": "Mercy Njoroge", "bio": "Organized and reliable for smooth administration"},
                {"fullname": "Sosnes Dan", "bio": "Transparent record keeping and communication"},
            ]},
            {"position": "Treasurer", "max_vote": 1, "candidates": [
                {"fullname": "Hannah Akinyi", "bio": "Financial planning for student activities"},
                {"fullname": "Ian Shida", "bio": "Ensuring responsible allocation of student funds"},
            ]},
            {"position": "Social & Cultural Coordinator", "max_vote": 2, "candidates": [
                {"fullname": "Jack Mahui", "bio": "Events that promote culture and community"},
                {"fullname": "Adams Brown", "bio": "Student engagement and creative initiatives"},
                {"fullname": "Anwar Twahir", "bio": "Inclusive and fun campus programs"},
            ]},
            {"position": "Sports Coordinator", "max_vote": 2, "candidates": [
                {"fullname": "Laura Mutua", "bio": "Encouraging active participation in all sports"},
                {"fullname": "John Mark", "bio": "Improving sports facilities and training programs"},
                {"fullname": "Lydia Okibero", "bio": "Organizing tournaments and student competitions"},
            ]},
            {"position": "Welfare Officer", "max_vote": 1, "candidates": [
                {"fullname": "Peter Okello", "bio": "Support for mental health and student welfare"},
                {"fullname": "Davis Isaac", "bio": "Creating awareness on student resources and rights"},
            ]},
        ]

        # Populate positions and candidates
        for data in election_data:
            position, created = Position.objects.get_or_create(
                name=data["position"],
                defaults={"max_vote": data["max_vote"], "priority": 0}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created position: {position.name}"))

            for cand in data["candidates"]:
                candidate, c_created = Candidate.objects.get_or_create(
                    fullname=cand["fullname"],
                    position=position,
                    defaults={"bio": cand["bio"]}
                )
                if c_created:
                    self.stdout.write(self.style.SUCCESS(f"  Added candidate: {candidate.fullname}"))

        self.stdout.write(self.style.SUCCESS("Election data populated successfully!"))