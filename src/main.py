from typing import List
from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import RedirectResponse, FileResponse
from sqlalchemy.orm import Session
from .models import LinkCreate, LinkSchema, Link, Base
from .database import engine
from .dependencies import get_db

app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.get('/')
def index(db: Session = Depends(get_db)):
    """Get the web interface."""
    return FileResponse('src/html/index.html')


@app.get('/all', response_model=List[LinkSchema])
def get_all_links(db: Session = Depends(get_db)):
    """Get all of the links saved in the database."""
    return db.query(Link).all()


@app.get('/{link_id}', responses={404: {}})
def get_link(link_id: int, db: Session = Depends(get_db)):
    """Redirect to the link with given ID."""
    link = db.query(Link).where(Link.id == link_id).first()
    if not link:
        raise HTTPException(404, detail='Link not found.')
    link.uses += 1
    db.commit()
    return RedirectResponse(link.url)


@app.get('/{link_id}/info', response_model=LinkSchema, responses={404: {}})
def get_link_info(link_id: int, db: Session = Depends(get_db)):
    """Get information related to a link by given ID"""
    link = db.query(Link).where(Link.id == link_id).first()
    if not link:
        raise HTTPException(404, detail='Link not found.')
    return link


@app.post('/create', response_model=LinkSchema)
def create_link(new_link: LinkCreate, db: Session = Depends(get_db)):
    """
    Create a new link.
    If the URL already exists in the database it will be returned
    rather than creating a new link with the given URL.
    """
    link = db.query(Link).where(Link.url == new_link.url).first()
    if link:
        # URL already exists, return the link for it.
        return link

    # Make sure the given link starts with http or https so it doesn't break the FastAPI RedirectResponse.
    if not new_link.url.startswith('http://') and not new_link.url.startswith('https://'):
        new_link.url = 'http://' + new_link.url
    link = Link(**new_link.dict())
    db.add(link)
    db.commit()
    db.refresh(link)
    return link
