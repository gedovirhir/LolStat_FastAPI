from fastapi import APIRouter

from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html

router = APIRouter(prefix='/swagger')


@router.get("/doc", include_in_schema=False)
async def get_documentation():
    return get_swagger_ui_html(openapi_url="/openapi.json", title="API documentation")

@router.get("/redoc", include_in_schema=False)
async def redoc():
    return get_redoc_html(openapi_url="/openapi.json", title="API documentation")