import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

import django

django.setup()

from fastapi import FastAPI

from authentication.api import router as authentication_router
from categories.api import router as categories_router
from tasks.api import router as tasks_router


app = FastAPI(
    title='KaksFlow API',
    description='API para gerenciamento de tarefas.',
    version='1.0.0'
)

app.include_router(authentication_router)
app.include_router(categories_router)
app.include_router(tasks_router)