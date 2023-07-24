from .views import router as lol_router
from .profile import router as lol_profile_router
from .statistic import router as lol_statistic_router

lol_router.include_router(lol_profile_router)
lol_router.include_router(lol_statistic_router)