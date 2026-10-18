import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from src.auth import normalize_email
from src.catalog import DEFAULT_SKILLS, RESOURCES
from src.config import LOCAL_DB_PATH, MONGODB_DB, MONGODB_URI


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _learner_key(learner: dict[str, Any]) -> str:
    email = normalize_email(str(learner.get("email") or ""))
    if email:
        return email
    return str(learner.get("name") or "").strip()


def _public_user(doc: dict[str, Any] | None) -> dict[str, Any] | None:
    if not doc:
        return None
    return {
        "email": doc.get("email"),
        "name": doc.get("name"),
        "created_at": doc.get("created_at"),
    }


class Store:
    backend = "none"

    def ping(self) -> bool:
        return True

    def seed_resources(self) -> None:
        raise NotImplementedError

    def list_resources(self) -> list[dict[str, Any]]:
        raise NotImplementedError

    def create_user(self, email: str, name: str, password_hash: str) -> dict[str, Any]:
        raise NotImplementedError

    def get_user(self, email: str) -> dict[str, Any] | None:
        raise NotImplementedError

    def upsert_learner(self, learner: dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedError

    def get_learner(self, key: str) -> dict[str, Any] | None:
        raise NotImplementedError

    def save_progress(self, key: str, completed_ids: list[str], skills: dict[str, int]) -> None:
        raise NotImplementedError

    def add_feedback(self, key: str, rating: str, note: str = "") -> None:
        raise NotImplementedError


class MongoStore(Store):
    backend = "mongodb"

    def __init__(self, uri: str, db_name: str = MONGODB_DB):
        from pymongo import MongoClient

        self.client = MongoClient(uri, serverSelectionTimeoutMS=4000)
        self.client.admin.command("ping")
        self.db = self.client[db_name]
        self.resources = self.db.resources
        self.users = self.db.users
        self.learners = self.db.learners
        self.feedback = self.db.feedback
        self.users.create_index("email", unique=True)

    def seed_resources(self) -> None:
        for resource in RESOURCES:
            doc = {**resource, "_id": resource["id"], "updated_at": _now()}
            self.resources.replace_one({"_id": resource["id"]}, doc, upsert=True)

    def list_resources(self) -> list[dict[str, Any]]:
        docs = list(self.resources.find({}, {"_id": 0}))
        return docs or list(RESOURCES)

    def create_user(self, email: str, name: str, password_hash: str) -> dict[str, Any]:
        key = normalize_email(email)
        if self.users.find_one({"email": key}):
            raise ValueError("An account already exists for that email.")
        payload = {
            "email": key,
            "name": name.strip(),
            "password_hash": password_hash,
            "created_at": _now(),
        }
        self.users.insert_one(payload)
        return _public_user(payload) or payload

    def get_user(self, email: str) -> dict[str, Any] | None:
        return self.users.find_one({"email": normalize_email(email)}, {"_id": 0})

    def upsert_learner(self, learner: dict[str, Any]) -> dict[str, Any]:
        key = _learner_key(learner)
        payload = {**learner, "updated_at": _now()}
        if learner.get("email"):
            payload["email"] = normalize_email(str(learner["email"]))
        existing = self.learners.find_one({"$or": [{"email": key}, {"name": key}]})
        if existing:
            self.learners.update_one({"_id": existing["_id"]}, {"$set": payload})
        else:
            payload["created_at"] = _now()
            self.learners.insert_one(payload)
        return self.get_learner(key) or payload

    def get_learner(self, key: str) -> dict[str, Any] | None:
        lookup = key.strip()
        email = normalize_email(lookup)
        doc = self.learners.find_one({"email": email}, {"_id": 0}) if email else None
        if not doc:
            doc = self.learners.find_one({"name": lookup}, {"_id": 0})
        return doc

    def save_progress(self, key: str, completed_ids: list[str], skills: dict[str, int]) -> None:
        lookup = key.strip()
        email = normalize_email(lookup)
        fields = {
            "email": email or lookup,
            "completed_ids": completed_ids,
            "skills": skills,
            "updated_at": _now(),
        }
        existing = self.learners.find_one({"$or": [{"email": email}, {"name": lookup}]})
        if existing:
            self.learners.update_one({"_id": existing["_id"]}, {"$set": fields})
        else:
            self.learners.insert_one({**fields, "created_at": _now()})

    def add_feedback(self, key: str, rating: str, note: str = "") -> None:
        self.feedback.insert_one(
            {
                "email": normalize_email(key) or key.strip(),
                "rating": rating,
                "note": note,
                "created_at": _now(),
            }
        )


class LocalStore(Store):
    backend = "local-json"

    def __init__(self, path: Path = LOCAL_DB_PATH):
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self._write({"resources": [], "users": {}, "learners": {}, "feedback": []})

    def _read(self) -> dict[str, Any]:
        data = json.loads(self.path.read_text())
        data.setdefault("users", {})
        data.setdefault("learners", {})
        data.setdefault("feedback", [])
        data.setdefault("resources", [])
        return data

    def _write(self, data: dict[str, Any]) -> None:
        self.path.write_text(json.dumps(data, indent=2))

    def seed_resources(self) -> None:
        data = self._read()
        data["resources"] = list(RESOURCES)
        self._write(data)

    def list_resources(self) -> list[dict[str, Any]]:
        resources = self._read().get("resources") or []
        return resources or list(RESOURCES)

    def create_user(self, email: str, name: str, password_hash: str) -> dict[str, Any]:
        data = self._read()
        key = normalize_email(email)
        if data["users"].get(key):
            raise ValueError("An account already exists for that email.")
        payload = {
            "email": key,
            "name": name.strip(),
            "password_hash": password_hash,
            "created_at": _now(),
        }
        data["users"][key] = payload
        self._write(data)
        return _public_user(payload) or payload

    def get_user(self, email: str) -> dict[str, Any] | None:
        return self._read().get("users", {}).get(normalize_email(email))

    def upsert_learner(self, learner: dict[str, Any]) -> dict[str, Any]:
        data = self._read()
        key = _learner_key(learner)
        existing = data["learners"].get(key, {})
        payload = {
            **existing,
            **learner,
            "skills": learner.get("skills") or existing.get("skills") or dict(DEFAULT_SKILLS),
            "completed_ids": learner.get("completed_ids", existing.get("completed_ids", [])),
            "updated_at": _now(),
        }
        if learner.get("email"):
            payload["email"] = normalize_email(str(learner["email"]))
        if "created_at" not in existing:
            payload["created_at"] = _now()
        data["learners"][key] = payload
        self._write(data)
        return payload

    def get_learner(self, key: str) -> dict[str, Any] | None:
        learners = self._read().get("learners", {})
        lookup = key.strip()
        email = normalize_email(lookup)
        if email in learners:
            return learners[email]
        return learners.get(lookup)

    def save_progress(self, key: str, completed_ids: list[str], skills: dict[str, int]) -> None:
        data = self._read()
        lookup = normalize_email(key) or key.strip()
        learner = data["learners"].get(lookup, {"email": lookup, "name": lookup})
        learner["completed_ids"] = completed_ids
        learner["skills"] = skills
        learner["updated_at"] = _now()
        data["learners"][lookup] = learner
        self._write(data)

    def add_feedback(self, key: str, rating: str, note: str = "") -> None:
        data = self._read()
        data.setdefault("feedback", []).append(
            {
                "email": normalize_email(key) or key.strip(),
                "rating": rating,
                "note": note,
                "created_at": _now(),
            }
        )
        self._write(data)


def connect_store(uri: str | None = None) -> Store:
    resolved = (uri or MONGODB_URI or "").strip()
    if resolved:
        try:
            store = MongoStore(resolved)
            store.seed_resources()
            return store
        except Exception:
            store = LocalStore()
            store.seed_resources()
            store.backend = "local-json (mongodb unavailable)"
            return store

    store = LocalStore()
    store.seed_resources()
    return store
