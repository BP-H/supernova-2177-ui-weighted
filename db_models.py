# STRICTLY A SOCIAL MEDIA PLATFORM
# Intellectual Property & Artistic Inspiration
# Legal & Ethical Safeguards
# --- MODULE: db_models.py ---
# Database setup from FastAPI files
import os  # Added for DATABASE_URL environment variable
import uuid
import hashlib
import logging
try:
    from sqlalchemy import (
        create_engine,
        Column,
        Integer,
        String,
        Text,
        Boolean,
        DateTime,
        ForeignKey,
        UniqueConstraint,
        Table,
        Float,
        JSON,
        text,
    )
    from sqlalchemy.orm import (
        sessionmaker,
        relationship,
        Session,
        declarative_base,
    )
except Exception:  # pragma: no cover - optional dependency
    try:
        from stubs.sqlalchemy_stub import (
            create_engine,
            Column,
            Integer,
            String,
            Text,
            Boolean,
            DateTime,
            ForeignKey,
            Table,
            Float,
            JSON,
            text,
            sessionmaker,
            relationship,
            Session,
            declarative_base,
        )
    except Exception:  # pragma: no cover - package may be relative
        from .stubs.sqlalchemy_stub import (
            create_engine,
            Column,
            Integer,
            String,
            Text,
            Boolean,
            DateTime,
            ForeignKey,
            Table,
            Float,
            JSON,
            text,
            sessionmaker,
            relationship,
            Session,
            declarative_base,
        )

    def UniqueConstraint(*_a, **_kw):
        return None

    class DeclarativeBase:
        metadata = type(
            "Meta",
            (),
            {"create_all": lambda *a, **k: None, "drop_all": lambda *a, **k: None},
        )()
from typing import TYPE_CHECKING
import datetime # Ensure datetime is imported for default values

# NOTE: In a real project, DATABASE_URL and SessionLocal would typically be imported from a central config/db module.
# For this extraction, we'll keep it self-contained for clarity, assuming it would be integrated.
# DATABASE_URL = "postgresql+asyncpg://<username>:<password>@<hostname>/<database>"  # Example format
DB_MODE = os.getenv("DB_MODE", "local")
UNIVERSE_ID = os.getenv("UNIVERSE_ID", str(uuid.uuid4()))

if DB_MODE == "central":
    DATABASE_URL = os.getenv("DATABASE_URL", "")
    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL must be set in central mode")
else:
    DATABASE_URL = os.getenv(
        "DATABASE_URL", f"sqlite:///universe_{UNIVERSE_ID}.db"
    )

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {},
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Base class for all ORM models
Base = declarative_base()

# Association Tables from FastAPI files
harmonizer_follows = Table(
    "harmonizer_follows",
    Base.metadata,
    Column("follower_id", Integer, ForeignKey("harmonizers.id"), primary_key=True),
    Column("followed_id", Integer, ForeignKey("harmonizers.id"), primary_key=True),
)
vibenode_likes = Table(
    "vibenode_likes",
    Base.metadata,
    Column("harmonizer_id", Integer, ForeignKey("harmonizers.id"), primary_key=True),
    Column("vibenode_id", Integer, ForeignKey("vibenodes.id"), primary_key=True),
)
group_members = Table(
    "group_members",
    Base.metadata,
    Column("harmonizer_id", Integer, ForeignKey("harmonizers.id"), primary_key=True),
    Column("group_id", Integer, ForeignKey("groups.id"), primary_key=True),
)
event_attendees = Table(
    "event_attendees",
    Base.metadata,
    Column("harmonizer_id", Integer, ForeignKey("harmonizers.id"), primary_key=True),
    Column("event_id", Integer, ForeignKey("events.id"), primary_key=True),
)
comment_mentions = Table(
    "comment_mentions",
    Base.metadata,
    Column("comment_id", Integer, ForeignKey("comments.id"), primary_key=True),
    Column("harmonizer_id", Integer, ForeignKey("harmonizers.id"), primary_key=True),
)
vibenode_entanglements = Table(
    "vibenode_entanglements",
    Base.metadata,
    Column("source_id", Integer, ForeignKey("vibenodes.id"), primary_key=True),
    Column("target_id", Integer, ForeignKey("vibenodes.id"), primary_key=True),
    Column("strength", Float, default=1.0),
)
proposal_votes = Table(
    "proposal_votes",
    Base.metadata,
    Column("harmonizer_id", Integer, ForeignKey("harmonizers.id"), primary_key=True),
    Column("proposal_id", Integer, ForeignKey("proposals.id"), primary_key=True),
    Column("vote", String, nullable=False),
)


# ORM Models from all files
class Harmonizer(Base):
    __tablename__ = "harmonizers"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    bio = Column(Text, default="")
    profile_pic = Column(String, default="default.jpg")
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    species = Column(String, default="human", nullable=False)
    harmony_score = Column(String, default="100.0")
    creative_spark = Column(String, default="1000000.0")
    is_genesis = Column(Boolean, default=False)
    consent_given = Column(Boolean, default=True)
    cultural_preferences = Column(JSON, default=list)
    engagement_streaks = Column(JSON, default=dict)
    network_centrality = Column(Float, default=0.0)
    karma_score = Column(Float, default=0.0)
    last_passive_aura_timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    vibenodes = relationship(
        "VibeNode", back_populates="author", cascade="all, delete-orphan"
    )
    comments = relationship(
        "Comment", back_populates="author", cascade="all, delete-orphan"
    )
    notifications = relationship(
        "Notification", back_populates="harmonizer", cascade="all, delete-orphan"
    )
    mentioned_in_comments = relationship(
        "Comment",
        secondary=comment_mentions,
        back_populates="mentions",
    )
    messages_sent = relationship(
        "Message",
        foreign_keys="[Message.sender_id]",
        back_populates="sender",
        cascade="all, delete-orphan",
    )
    messages_received = relationship(
        "Message",
        foreign_keys="[Message.receiver_id]",
        back_populates="receiver",
        cascade="all, delete-orphan",
    )
    groups = relationship("Group", secondary=group_members, back_populates="members")
    events = relationship("Event", secondary=event_attendees, back_populates="attendees")
    following = relationship(
        "Harmonizer",
        secondary=harmonizer_follows,
        primaryjoin=(harmonizer_follows.c.follower_id == id),
        secondaryjoin=(harmonizer_follows.c.followed_id == id),
        backref="followers",
    )
    node_companies = relationship("CreativeGuild", back_populates="owner")
    simulations = relationship(
        "SimulationLog", back_populates="harmonizer", cascade="all, delete-orphan"
    )

    def set_password(self, password: str) -> None:
        """Hash ``password`` and store it on the model."""
        self.hashed_password = hashlib.sha256(password.encode()).hexdigest()

    def verify_password(self, password: str) -> bool:
        """Return ``True`` if ``password`` matches the stored hash."""
        return (
            hashlib.sha256(password.encode()).hexdigest() == self.hashed_password
        )


class VibeNode(Base):
    __tablename__ = "vibenodes"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(Text)
    author_id = Column(Integer, ForeignKey("harmonizers.id"), nullable=False)
    parent_vibenode_id = Column(Integer, ForeignKey("vibenodes.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    media_type = Column(String, default="text")
    media_url = Column(String, nullable=True)
    fractal_depth = Column(Integer, default=0)
    echo = Column(String, default="0.0")
    engagement_catalyst = Column(String, default="0.0")
    negentropy_score = Column(String, default="0.0")
    tags = Column(JSON, default=list)
    patron_saint_id = Column(Integer, ForeignKey("ai_personas.id"), nullable=True)
    author = relationship("Harmonizer", back_populates="vibenodes")
    sub_nodes = relationship(
        "VibeNode",
        backref="parent_vibenode",
        remote_side=[id],
        cascade="all, delete-orphan",
        single_parent=True,
    )
    comments = relationship(
        "Comment", back_populates="vibenode", cascade="all, delete-orphan"
    )
    likes = relationship(
        "Harmonizer", secondary=vibenode_likes, backref="liked_vibenodes"
    )
    entangled_with = relationship(
        "VibeNode",
        secondary=vibenode_entanglements,
        primaryjoin=(vibenode_entanglements.c.source_id == id),
        secondaryjoin=(vibenode_entanglements.c.target_id == id),
        backref="entangled_from",
    )
    creative_guild = relationship(
        "CreativeGuild", back_populates="vibenode", uselist=False
    )
    patron_saint = relationship("AIPersona", back_populates="vibenodes")


class CreativeGuild(Base):
    __tablename__ = "creative_guilds"
    id = Column(Integer, primary_key=True, index=True)
    vibenode_id = Column(
        Integer, ForeignKey("vibenodes.id"), unique=True, nullable=False
    )
    owner_id = Column(Integer, ForeignKey("harmonizers.id"), nullable=False)
    legal_name = Column(String, nullable=False)
    guild_type = Column(String, default="art_collective")
    registration_timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    vibenode = relationship("VibeNode", back_populates="creative_guild")
    owner = relationship("Harmonizer", back_populates="node_companies")


class GuinnessClaim(Base):
    __tablename__ = "guinness_claims"
    id = Column(Integer, primary_key=True, index=True)
    claimant_id = Column(Integer, ForeignKey("harmonizers.id"), nullable=False)
    claim_type = Column(String, nullable=False)
    evidence_details = Column(Text)
    status = Column(String, default="pending")
    submission_timestamp = Column(DateTime, default=datetime.datetime.utcnow)


class AIPersona(Base):
    __tablename__ = "ai_personas"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(Text)
    base_personas = Column(JSON, default=list)
    is_emergent = Column(Boolean, default=False)
    vibenodes = relationship("VibeNode", back_populates="patron_saint")


class Group(Base):
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    members = relationship(
        "Harmonizer", secondary=group_members, back_populates="groups"
    )
    events = relationship("Event", back_populates="group", cascade="all, delete-orphan")
    proposals = relationship(
        "Proposal", back_populates="group", cascade="all, delete-orphan"
    )


class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    author_id = Column(Integer, ForeignKey("harmonizers.id"), nullable=False)
    vibenode_id = Column(
        Integer, ForeignKey("vibenodes.id"), nullable=False, index=True
    )
    parent_comment_id = Column(
        Integer, ForeignKey("comments.id"), nullable=True, index=True
    )
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    author = relationship("Harmonizer", back_populates="comments")
    vibenode = relationship("VibeNode", back_populates="comments")
    replies = relationship(
        "Comment",
        backref="parent_comment",
        remote_side=[id],
        cascade="all, delete-orphan",
        single_parent=True,
    )
    mentions = relationship(
        "Harmonizer",
        secondary=comment_mentions,
        back_populates="mentioned_in_comments",
    )


class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    description = Column(Text)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False, index=True)
    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True), nullable=True)
    synchronization_potential = Column(Float, default=0.0)
    organizer_id = Column(Integer, ForeignKey("harmonizers.id"), nullable=False)
    group = relationship("Group", back_populates="events")
    attendees = relationship(
        "Harmonizer", secondary=event_attendees, back_populates="events"
    )


class Proposal(Base):
    __tablename__ = "proposals"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=True, index=True)
    author_id = Column(Integer, ForeignKey("harmonizers.id"), nullable=False)
    status = Column(String, default="open", index=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    voting_deadline = Column(DateTime(timezone=True), nullable=False)
    payload = Column(JSON, nullable=True)
    group = relationship("Group", back_populates="proposals")
    votes = relationship(
        "ProposalVote", back_populates="proposal", cascade="all, delete-orphan"
    )


class ProposalVote(Base):
    __tablename__ = "proposal_votes_records"
    id = Column(Integer, primary_key=True, index=True)
    proposal_id = Column(
        Integer, ForeignKey("proposals.id"), nullable=False, index=True
    )
    harmonizer_id = Column(Integer, ForeignKey("harmonizers.id"), nullable=False)
    vote = Column(String, nullable=False)
    proposal = relationship("Proposal", back_populates="votes")


class Notification(Base):
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True, index=True)
    harmonizer_id = Column(
        Integer, ForeignKey("harmonizers.id"), nullable=False, index=True
    )
    message = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False, index=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    harmonizer = relationship("Harmonizer", back_populates="notifications")


class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(
        Integer, ForeignKey("harmonizers.id"), nullable=False, index=True
    )
    receiver_id = Column(
        Integer, ForeignKey("harmonizers.id"), nullable=False, index=True
    )
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    sender = relationship(
        "Harmonizer", foreign_keys=[sender_id], back_populates="messages_sent"
    )
    receiver = relationship(
        "Harmonizer", foreign_keys=[receiver_id], back_populates="messages_received"
    )


class SimulationLog(Base):
    __tablename__ = "simulation_logs"
    id = Column(Integer, primary_key=True, index=True)
    harmonizer_id = Column(Integer, ForeignKey("harmonizers.id"), nullable=False)
    sim_type = Column(String, nullable=False, index=True)
    parameters = Column(JSON)
    results = Column(JSON)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    harmonizer = relationship("Harmonizer", back_populates="simulations")


class LogEntry(Base):
    __tablename__ = "log_chain"
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    event_type = Column(String, nullable=False)
    payload = Column(Text)
    previous_hash = Column(String, nullable=False)
    current_hash = Column(String, unique=True, nullable=False)

    def chain_of_remix(self, db: Session) -> list[str]:
        """Return lineage of remix hashes leading to this entry."""
        chain = []
        prev = self.previous_hash
        while prev:
            entry = db.query(LogEntry).filter_by(current_hash=prev).first()
            if not entry:
                logging.error("Broken remix chain at %s", prev)
                raise ValueError(f"Missing log entry for hash {prev}")
            chain.append(entry.current_hash)
            prev = entry.previous_hash
        return chain

    def compute_hash(self) -> str:
        """Return SHA-256 hash for this entry."""
        data = f"{self.timestamp.isoformat()}|{self.event_type}|{self.payload}|{self.previous_hash}"
        return hashlib.sha256(data.encode("utf-8")).hexdigest()


class SystemState(Base):
    __tablename__ = "system_state"
    id = Column(Integer, primary_key=True)
    key = Column(String, unique=True, nullable=False)
    value = Column(String, nullable=False)


class ValidatorReputation(Base):
    """Stores reputation scores for validators."""

    __tablename__ = "validator_reputations"

    validator_id = Column(String, primary_key=True)
    reputation = Column(Float, nullable=False, default=0.0)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow,
                        onupdate=datetime.datetime.utcnow)


class ValidatorProfile(Base):
    """Stores specialty and affiliation metadata for validators."""

    __tablename__ = "validator_profiles"

    validator_id = Column(String, primary_key=True)
    specialty = Column(String, nullable=True)
    affiliation = Column(String, nullable=True)


# Add this below the SystemState class but before Coin to maintain ordering:
class HypothesisRecord(Base):
    """
    Represents a scientific hypothesis tracked by the system.
    Includes metadata, audit history, and evaluation stats.
    """
    __tablename__ = "hypotheses"

    id = Column(String, primary_key=True)  # e.g., HYP_1721495734_a1b2c3d4
    title = Column(String, nullable=True)
    description = Column(Text, nullable=True)

    status = Column(String, default="open", index=True)  # open / validated / falsified / merged / inconclusive / etc.
    score = Column(Float, default=0.0)
    entropy_change = Column(Float, default=0.0) # From associated audit metadata
    confidence_interval = Column(String, default="") # From hypothesis_reasoner
    metadata_json = Column(JSON, default=lambda: {})

    validation_log_ids = Column(JSON, default=lambda: [])  # LogEntry.id references
    audit_sources = Column(JSON, default=lambda: [])
    # causal_trigger.py, audit_bridge.py etc. refs (SystemState keys)

    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    tags = Column(JSON, default=lambda: []) #
    notes = Column(Text, default="") # Summary of events/updates

    # Full history of evaluations / edits
    history = Column(JSON, default=lambda: []) # Detailed timestamped history of score/status changes

    # Relationships (Optional, for future direct linking)
    # E.g., validation_logs = relationship("LogEntry", secondary=hypothesis_validation_logs_table)

    def __repr__(self):
        return f"<HypothesisRecord(id={self.id}, status={self.status}, score={self.score})>"


# FUSED: Integrated additional models from v01_grok15.py, renamed for clarity
class SymbolicToken(Base):
    """Purely symbolic artifact used for gameplay mechanics."""

    __tablename__ = "symbolic_tokens"

    token_id = Column(String, primary_key=True, index=True)
    creator = Column(String, nullable=False)
    owner = Column(String, nullable=False)
    symbolic_value = Column(String, default="0.0")
    is_root = Column(Boolean, default=False)
    universe_id = Column(String, default="main")
    is_remix = Column(Boolean, default=False)
    references = Column(JSON, default=list)
    improvement = Column(Text, default="")
    fractional_pct = Column(String, default="0.0")
    ancestors = Column(JSON, default=list)
    content = Column(Text, default="")
    reaction_reserve = Column(String, default="0.0")
    reactions = Column(JSON, default=list)

    # compatibility aliases
    @property
    def coin_id(self) -> str:  # pragma: no cover - legacy support
        return self.token_id

    @coin_id.setter
    def coin_id(self, value: str) -> None:  # pragma: no cover - legacy support
        self.token_id = value

    @property
    def value(self) -> str:  # pragma: no cover - legacy support
        return self.symbolic_value

    @value.setter
    def value(self, v: str) -> None:  # pragma: no cover - legacy support
        self.symbolic_value = v

    @property
    def reactor_escrow(self) -> str:  # pragma: no cover - legacy support
        return self.reaction_reserve

    @reactor_escrow.setter
    def reactor_escrow(self, v: str) -> None:  # pragma: no cover - legacy support
        self.reaction_reserve = v

# Backwards compatibility for existing code references
Coin = SymbolicToken


class UniverseBranch(Base):
    """Record representing a forked universe branch."""

    __tablename__ = "universe_branches"

    id = Column(String, primary_key=True)
    creator_id = Column(ForeignKey("harmonizers.id"))
    karma_at_fork = Column(Float)
    config = Column(JSON)
    timestamp = Column(DateTime)
    status = Column(String)
    entropy_divergence = Column(Float, default=0.0)
    consensus = Column(Float, default=0.0)
    vote_count = Column(Integer, default=0)
    yes_count = Column(Integer, default=0)


# Backwards compatibility alias for earlier RFCs
UniverseFork = UniverseBranch


class BranchVote(Base):
    """Vote for or against a universe branch."""

    __tablename__ = "branch_votes"

    id = Column(Integer, primary_key=True)
    branch_id = Column(ForeignKey("universe_branches.id"), nullable=False)
    voter_id = Column(ForeignKey("harmonizers.id"), nullable=False)
    vote = Column(Boolean, nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

    __table_args__ = (
        UniqueConstraint("branch_id", "voter_id", name="unique_branch_voter"),
    )


class TokenListing(Base):
    """Listing for trading symbolic tokens within gameplay."""

    __tablename__ = "token_listings"

    listing_id = Column(String, primary_key=True)
    token_id = Column(String, nullable=False)
    seller = Column(String, nullable=False)
    listing_value = Column(String, nullable=False)
    timestamp = Column(String, nullable=False)

    # compatibility aliases
    @property
    def coin_id(self) -> str:  # pragma: no cover - legacy support
        return self.token_id

    @coin_id.setter
    def coin_id(self, value: str) -> None:  # pragma: no cover - legacy support
        self.token_id = value

    @property
    def price(self) -> str:  # pragma: no cover - legacy support
        return self.listing_value

    @price.setter
    def price(self, v: str) -> None:  # pragma: no cover - legacy support
        self.listing_value = v

# Backwards compatibility alias
MarketplaceListing = TokenListing


class FlaggedItem(Base):
    """Content flagged for moderation review."""

    __tablename__ = "flagged_items"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    reason = Column(String, nullable=False)
    status = Column(String, default="pending", index=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


def init_db(db_url: str | None = None) -> None:
    """Create all tables and ensure minimal raw schema exists.

    Parameters
    ----------
    db_url:
        Optional database URL used to (re)configure the engine. When provided
        the module level ``engine`` and ``SessionLocal`` will be rebound to the
        new connection.
    """

    global engine, SessionLocal

    if db_url:
        engine = create_engine(
            db_url,
            connect_args={"check_same_thread": False} if "sqlite" in db_url else {},
        )
        SessionLocal.configure(bind=engine)

    with engine.begin() as conn:
        conn.execute(
            text(
                """
                CREATE TABLE IF NOT EXISTS harmonizers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    hashed_password VARCHAR(255) NOT NULL,
                    bio TEXT,
                    profile_pic VARCHAR(255),
                    followers INTEGER DEFAULT 0,
                    following INTEGER DEFAULT 0,
                    is_active BOOLEAN DEFAULT 1,
                    is_admin BOOLEAN DEFAULT 0,
                    is_genesis BOOLEAN DEFAULT 0,
                    consent_given BOOLEAN DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_passive_aura_timestamp TIMESTAMP,
                    species VARCHAR(50) DEFAULT 'human',
                    cultural_preferences TEXT,
                    harmony_score FLOAT DEFAULT 0.0,
                    creative_spark FLOAT DEFAULT 0.0,
                    network_centrality FLOAT DEFAULT 0.0,
                    karma_score FLOAT DEFAULT 0.0,
                    engagement_streaks INTEGER DEFAULT 0
                );
                """
            )
        )

        res = conn.execute(text("SELECT COUNT(*) FROM harmonizers"))
        count = res.scalar() or 0
        if count == 0:
            conn.execute(
                text(
                    """
                    INSERT INTO harmonizers
                        (username, email, hashed_password, bio,
                         is_active, is_admin, is_genesis, consent_given, species)
                    VALUES ('admin','admin@supernova.dev','hashed_password_here',
                            'Default admin user for superNova_2177',1,1,1,1,'human');
                    """
                )
            )

    Base.metadata.create_all(bind=engine)


def seed_default_users() -> None:
    """Create default Harmonizer accounts if they don't exist."""
    session = SessionLocal()
    try:
        # Accounts we always want in a fresh DB
        defaults = ["guest", "demo_user"]

        for username in defaults:
            # Skip if the user already exists
            if session.query(Harmonizer).filter_by(username=username).first():
                continue

            # Very small “hash” for demo purposes only – **not** production-secure
            hashed = hashlib.sha256(username.encode()).hexdigest()

            # Branded e-mail addresses
            email = f"{username}@supernova.dev"
            if username == "demo_user":
                email = "demo@supernova.dev"

            session.add(
                Harmonizer(
                    username=username,
                    email=email,
                    hashed_password=hashed,
                    bio="Default user",
                )
            )

        session.commit()
    finally:
        session.close()



