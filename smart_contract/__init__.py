from __future__ import division  # Use floating point for math calculations


from flask import Blueprint

from CTFd.models import (
    ChallengeFiles,
    Challenges,
    Fails,
    Flags,
    Hints,
    Solves,
    Tags,
    db,
)
from CTFd.plugins import register_plugin_assets_directory
from CTFd.plugins.challenges import CHALLENGE_CLASSES, BaseChallenge
from CTFd.plugins.flags import get_flag_class
from CTFd.utils.uploads import delete_file
from CTFd.utils.user import get_ip


class SmartContractChallenge(BaseChallenge):
    id = "smart_contract"
    name = "smart_contract"
    templates = {
        "create": "/plugins/smart_contract/assets/create.html",
        "update": "/plugins/smart_contract/assets/update.html",
        "view": "/plugins/smart_contract/assets/view.html",
    }
    scripts = {
        "create": "/plugins/smart_contract/assets/create.js",
        "update": "/plugins/smart_contract/assets/update.js",
        "view": "/plugins/smart_contract/assets/view.js",
    }
    route = "/plugins/smart_contract/assets/"
    blueprint = Blueprint(
        "smart_contract", __name__, template_folder="templates", static_folder="assets"
    )

    @staticmethod
    def create(request):
        data = request.form or request.get_json()
        challenge = Challenges(**data)

        db.session.add(challenge)
        db.session.commit()

        return challenge

    @staticmethod
    def read(challenge):
        data = {
            "id": challenge.id,
            "name": challenge.name,
            "value": challenge.value,
            "description": challenge.description,
            "category": challenge.category,
            "state": challenge.state,
            "max_attempts": challenge.max_attempts,
            "type": challenge.type,
            "type_data": {
                "id": SmartContractChallenge.id,
                "name": SmartContractChallenge.name,
                "templates": SmartContractChallenge.templates,
                "scripts": SmartContractChallenge.scripts,
            },
        }
        return data

    @staticmethod
    def update(challenge, request):
        data = request.form or request.get_json()
        for attr, value in data.items():
            setattr(challenge, attr, value)

        db.session.commit()
        return challenge

    @staticmethod
    def delete(challenge):
        Fails.query.filter_by(challenge_id=challenge.id).delete()
        Solves.query.filter_by(challenge_id=challenge.id).delete()
        Flags.query.filter_by(challenge_id=challenge.id).delete()
        files = ChallengeFiles.query.filter_by(challenge_id=challenge.id).all()
        for f in files:
            delete_file(f.id)
        ChallengeFiles.query.filter_by(challenge_id=challenge.id).delete()
        Tags.query.filter_by(challenge_id=challenge.id).delete()
        Hints.query.filter_by(challenge_id=challenge.id).delete()
        Challenges.query.filter_by(id=challenge.id).delete()
        db.session.commit()

    @staticmethod
    def attempt(challenge, request):
        data = request.form or request.get_json()
        submission = data["submission"].strip()
        flags = Flags.query.filter_by(challenge_id=challenge.id).all()
        for flag in flags:
            if get_flag_class(flag.type).compare(flag, submission):
                return True, "Correct"
        return False, "Incorrect"

    @staticmethod
    def solve(user, team, challenge, request):
        data = request.form or request.get_json()
        submission = data["submission"].strip()
        solve = Solves(
            user_id=user.id,
            team_id=team.id if team else None,
            challenge_id=challenge.id,
            ip=get_ip(req=request),
            provided=submission,
        )
        db.session.add(solve)
        db.session.commit()
        db.session.close()

    @staticmethod
    def fail(user, team, challenge, request):
        data = request.form or request.get_json()
        submission = data["submission"].strip()
        wrong = Fails(
            user_id=user.id,
            team_id=team.id if team else None,
            challenge_id=challenge.id,
            ip=get_ip(request),
            provided=submission,
        )
        db.session.add(wrong)
        db.session.commit()
        db.session.close()

def load(app):
    CHALLENGE_CLASSES["smart_contract"] = SmartContractChallenge
    register_plugin_assets_directory(
        app, base_path="/plugins/smart_contract/assets/"
    )
