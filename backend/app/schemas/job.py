from pydantic import BaseModel


class JobCreate(BaseModel):

    company: str

    title: str

    location: str

    remote: bool

    salary: str | None = None

    description: str

    apply_url: str

    source: str

    posted_date: str
