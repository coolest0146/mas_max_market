from typing import List
from fastapi import APIRouter ,Depends,HTTPException,status
import schemas ,models ,oath2,auth
from database_conn import  get_db

USERS=APIRouter(tags=["users"])

@USERS.post("/login",response_model=schemas.Token)
def login(user_data:schemas.UserLogin,db=Depends(get_db)):
    user=db.query(models.User).filter(user_data.email == models.User.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid Credentials")
    if not auth.password_verify(user_data.password,user.password_hash):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN ,detail="Invalid Credentials")
    token=oath2.create_token({"user_id":user.id})
    return {"access_token": token, "token_type": "bearer"}


@USERS.post("/register" )
def create_user(user_details:schemas.UserCreate,db=Depends(get_db)):
    password=auth.password_hash(user_details.password_hash)
    user_details.password_hash=password
    user=models.User(**user_details.model_dump())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@USERS.post("/update")
def update_info(user_data:schemas.Update,user_id:int=Depends(oath2.get_current_user),db=Depends(get_db)):
    user=db.query(models.User).filter(user_id == models.User.id).first()
    
    # if user_data.password:
    #     user.password_hash=auth.password_hash(user_data.password)
    # if user_data.password:
    #     user.username=user_data.username
    # if user_data.password:
    user.email=user_data.email
    
    db.commit()
    db.refresh(user)
    return user


    
# @USERS.post("/admin/roles/{user_id}",response_model=schemas.UserOut)
# def user_roleset(user_id:int,user_role:schemas.UserRoles,db=Depends(get_db),admin_id:int=Depends(oath2.get_current_user)):
#     admin=db.query(models.User).filter(models.User.id==admin_id).first()
#     user=db.query(models.User).filter(models.User.id==user_id).first()

#     if admin.roles != "admin":
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Out Of Reach")
#     if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No Informations")
#     user.roles =user_role.roles
#     print(user)
#     return user
# @USERS.get("/admin/users")
# def all_users(db=Depends(get_db),user_id:int=Depends(oath2.get_current_user)):
#     admin=db.query(models.User).filter(models.User.id == user_id and models.User.roles =="admin").first()
#     if not admin:
#         raise HTTPException(status_code=status.HTTP_423_LOCKED,detail="Contact Admin For Access")
#     users=db.query(models.User).all()
#     return users

# @USERS.get("/admin/delete/{user_id}")
# def delete_user(user_id:int,db=Depends(get_db),active_user_id:int=Depends(oath2.get_current_user)):
#     admin=db.query(models.User).filter(models.User.id == active_user_id and models.User.roles =="admin").first()
#     if not admin:
#         raise HTTPException(status_code=status.HTTP_423_LOCKED,detail="Contact Admin For Access")
#     user=db.query(models.User).filter(models.User.id == user_id).first()
#     db.delete(user)
#     db.commit()
#     return user