from fastapi import  FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import func
from ..database import get_db
from .. import models, schemas, oauth2

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

    
# @router.get("/", response_model=List[schemas.Post])
@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), 
              limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # print(limit)
    
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # query de postgres = SELECT posts.*, COUNT(votes.post_id) as votes FROM posts LEFT JOIN votes ON posts.id = votes.post_id group by posts.id;
    
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).offset(skip).limit(limit).all()
    
    """ posts = []
    for post, votes_count in results:
        post_data = schemas.PostOut(
            id=post.id,
            title=post.title,
            content=post.content,
            owner_id=post.owner_id,
            votes=votes_count
        )
        posts.append(post_data)
    print(results) """
    
    return posts
    """ conn = get_database_connection()
    if conn:
        with conn.cursor() as cur: """
            # cur.execute("""SELECT * FROM posts""")
            # posts = cur.fetchall()
    """  else:
    return {"error": "No se pudo conectar a la base de datos"} """
   

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # print(current_user.email)
    new_post = models.Post(owner_id=current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post 
    
#    conn = get_database_connection()
#    if conn:
#        with conn.cursor() as cur:
#            cur.execute("""INSERT INTO posts (title, content, published)  VALUES (%s, %s, %s) RETURNING *""", (post.title, post.content, post.published))
#            new_post = cur.fetchone()
#            conn.commit()
#            return {"data": new_post} 
#    else:
#        return {"error": "No se pudo crear un nuevo post"}

@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # post = db.query(models.Post).filter(models.Post.id == id).first()

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"post with id: {id} was not found")
    return post
    
    # conn = get_database_connection()
    # if conn:
    #     with conn.cursor() as cur:
    #         cur.execute("""SELECT * FROM posts WHERE id = %s """, (str(id),))
    #         post = cur.fetchone()
    #         if not post:
    #                 raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
    #                         detail=f"post with id: {id} was not found")
    #         return {"post_detail": post}
    # else:
    #     return {"error": "no se pudo obtener el post"}
    

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    post = post_query.first()
    
    if post == None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"post with id: {id} does not exist")
                
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    post_query.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

    # deleting post
    # encontrar el indice dentro del arreglo que requiere ID.
    # my_posts.pop(index)
    # conn = get_database_connection()
    # if conn:
    #     with conn.cursor() as cur:
    #         cur.execute("""DELETE FROM posts WHERE ID = %s RETURNING*""", (str(id),))
    #         deleted_post = cur.fetchone()
    #         conn.commit()
    #         if deleted_post == None:
    #             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                         detail=f"post with id: {id} does not exist")
    
    # return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    existing_post = post_query.first()
    
    if existing_post == None:
               raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"post with id: {id} does not exist")
    
    if existing_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    post_data = updated_post.model_dump()           
    post_query.update(post_data, synchronize_session=False )
    
    db.commit()
    
    return post_query.first()
    # conn = get_database_connection()
    # if conn:
    #     with conn.cursor() as cur:
    #         cur.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))
    #         updated_post = cur.fetchone()
    #         conn.commit()
    #         if updated_post == None:
    #             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                         detail=f"post with id: {id} does not exist")
    #         return {"data": updated_post}