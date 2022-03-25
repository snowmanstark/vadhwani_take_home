from fastapi import routing, Request
from fastapi.responses import Response

from agro.dependencies import db, src_lang, target_langs

router = routing.APIRouter(
    prefix="/view",
    tags=["View farmer Data"]
)

users = db["users"]

@router.get("/")
def view_farmer_data(lang: str, request: Request):
    if lang in target_langs or lang == src_lang:
        query = list(users.find({},{"_id":0,"phone":1, lang: 1}))
        for user in query:
            info = user.pop(lang)
            user.update(info)
        return query
    else:
        return Response(status_code=404,content="Invalid language")

