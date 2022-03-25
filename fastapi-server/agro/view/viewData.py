from fastapi import routing, Request
from fastapi.responses import Response
from fastapi.templating import Jinja2Templates

from agro.dependencies import db, src_lang, target_langs

router = routing.APIRouter(
    prefix="/view",
    tags=["View farmer Data"]
)

template = Jinja2Templates("agro/templates")
users = db["users"]

@router.get("/")
def view_farmer_data(request: Request, lang: str = "en"):
    if lang in target_langs or lang == src_lang:
        query = list(users.find({},{"_id":0,"phone":1, lang: 1}))
        for user in query:
            info = user.pop(lang)
            user.update(info)
        
        context={"request": request, "users": query, "lang": lang}
        # return query
        return template.TemplateResponse("view.html", context=context)
    else:
        return Response(status_code=404,content="Invalid language")
