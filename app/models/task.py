from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from app.db.database import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)

    status = Column(String, default="Pending")

    assignee = Column(String, nullable=True)
    due_date = Column(DateTime, nullable=True)

    project_id = Column(Integer, ForeignKey("projects.id"))
    owner_id = Column(Integer, ForeignKey("users.id"))

    project = relationship("Project", back_populates="tasks")
    owner = relationship("User")

    notifications = relationship(
    "Notification",
    back_populates="task",
    cascade="all, delete-orphan"
    )