import csv
from io import StringIO

from fastapi import routing, Request, File, UploadFile
from fastapi.responses import Response
from fastapi.templating import Jinja2Templates

from agro.dependencies import db, src_lang, r, target_langs, tc

router = routing.APIRouter(
    prefix="/upload",
    tags=["Upload"]
)

template = Jinja2Templates("agro/templates")
users = db["users"]

@router.get("/")
def render_upload_farmers_data_page(request: Request):
    '''
    Render upload page
    '''
    return template.TemplateResponse("upload.html", context={"request": request})


@router.post("/upload_csv")
async def upload_farmer_data(file: UploadFile = File(...)):
    if file.filename.split(".")[-1].casefold == "csv" or file.content_type == "text/csv":
        data = await file.read()
        buffer = StringIO(data.decode())
        file = csv.DictReader(buffer)
        lines = []
        # s = time.perf_counter()
        count, proc = 0, 0

        for line in file:
            count += 1
            try:
                translate_store_row(line)
                proc += 1
            except Exception as e:
                print(e)
        # print("elasped", time.perf_counter() - s)
        return Response(status_code=200, content=f"Processed {proc}/{count} rows.")
        # return Response(status_code=200,content="CSV uploaded successfully")
    else:
        return Response(status_code=422, content="Invalid file type!! Please upload a CSV file")


def translate_store_row(row: dict):
    phone = row.pop("phone_number")
    temp_doc = {"_id": phone, "phone": phone, "en": row}
    if any(row.values()):
        for target_lang in target_langs:
            # Get any cached translations if exists
            cached_tr = r.mget([ i+":"+target_lang for i in row.values()])

            # Map the cached text to the field names
            tr_maps = dict(zip(row.keys(), cached_tr))

            if not all(tr_maps.values()):
                '''
                Translate texts not in cache
                '''

                # Create dict of column_name and text not in cache
                uncached_txt_maps = { k:row[k] for k,v in zip(row.keys(), cached_tr) if not v}

                # translate the strings
                result = tc.translate(
                    list(uncached_txt_maps.values()), # list of uncached texts 
                    target_language=target_lang, 
                    source_language=src_lang, 
                    format_="text"
                    )
                uncached_txt_maps = dict(zip(uncached_txt_maps.keys(), [ i["translatedText"] for i in result]))
                tr_maps.update(uncached_txt_maps)
                
                # Cache recently translated texts
                uncached_txt_maps = { i["input"]+":"+target_lang : i["translatedText"] for i in result}
                r.mset(uncached_txt_maps)
            else:
                # All texts found in cache
                pass

            temp_doc[target_lang] = tr_maps
        users.insert_one(temp_doc)
        return True
    else:
        return False