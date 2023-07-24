from .views import router, jwt_router

router.include_router(jwt_router)